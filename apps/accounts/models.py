from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    """
    Custom user model for the gym management system.

    Every person who logs in is a User. Role-specific data lives in
    profile models in their own apps (MemberProfile, TrainerProfile).
    """

    # Django's createsuperuser command will prompt for these fields.
    # The custom createsuperuser command in this app extends that
    # behavior to also prompt for phone_number.
    REQUIRED_FIELDS = ['email', 'phone_number']

    class Role(models.TextChoices):
        OWNER = 'owner', 'Owner'
        RECEPTIONIST = 'receptionist', 'Receptionist'
        TRAINER = 'trainer', 'Trainer'
        MEMBER = 'member', 'Member'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.MEMBER,
        help_text='Determines which dashboard and permissions this user has.',
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        help_text='Kenyan format, e.g. 0712345678 or +254712345678. Required in forms.',
    )

    objects = UserManager()

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_role_display()})'

    @property
    def is_member(self):
        return self.role == self.Role.MEMBER

    @property
    def is_trainer(self):
        return self.role == self.Role.TRAINER

    @property
    def is_receptionist(self):
        return self.role == self.Role.RECEPTIONIST

    @property
    def is_owner(self):
        return self.role == self.Role.OWNER