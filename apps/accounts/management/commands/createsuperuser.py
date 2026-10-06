# ---------------------------------------------------------------------------
# FRAGILITY WARNING
#
# This command monkey-patches Django's field.null attribute at runtime to
# force the built-in createsuperuser command to prompt for phone_number.
# It relies on Django's internal implementation of the prompt logic.
#
# If a future Django version changes how createsuperuser decides which
# fields to prompt for, this command may silently stop prompting for
# phone_number, or crash. If that happens, the fix is to either:
#   1. Revert phone_number to null=False on the User model, or
#   2. Rewrite this command as a full standalone implementation
#
# This is documented technical debt. It was a deliberate trade-off.
# ---------------------------------------------------------------------------

"""
Custom createsuperuser command.

Django's built-in command does not prompt for fields that are
nullable at the model level. Our phone_number is nullable so that
multiple users can have NULL (per our design decision C2), but we
still want to prompt humans for it when creating a superuser.

This command subclasses Django's built-in command and forces
phone_number into the list of prompted fields.

The command name must remain 'createsuperuser' for Django to use
this instead of the built-in one.
"""
from django.contrib.auth.management.commands.createsuperuser import (
    Command as BaseCommand,
)
from django.core import exceptions
from django.core.management.base import CommandError


class Command(BaseCommand):
    # Force these fields to be treated as required for prompting.
    # Django's createsuperuser checks each field in REQUIRED_FIELDS;
    # if the field is nullable, it normally skips the prompt.
    # We override that logic by marking the field as non-null during
    # the prompt check.
    def get_required_fields(self):
        required_fields = super().get_required_fields()
        # Ensure phone_number is always in the list
        if 'phone_number' not in required_fields:
            required_fields.append('phone_number')
        return required_fields

    def add_arguments(self, parser):
        super().add_arguments(parser)

    def handle(self, *args, **options):
        # Temporarily mark phone_number as non-nullable so Django's
        # prompt logic asks for it. We restore it after the prompt
        # so nothing else in the process is affected.
        UserModel = self.UserModel
        phone_field = UserModel._meta.get_field('phone_number')
        original_null = phone_field.null
        phone_field.null = False

        try:
            return super().handle(*args, **options)
        except Exception as exc:
            raise CommandError(str(exc))
        finally:
            phone_field.null = original_null