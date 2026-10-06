from django.contrib.auth.models import UserManager as BaseUserManager
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    """
    Custom manager for the gym User model.

    Enforces the business rule that every user has a phone number,
    and that superusers are always owners.
    """

    use_in_migrations = True

    def _create_user(self, username, email, password, phone_number, role, **extra_fields):
        """
        Internal helper. Validates common fields and creates a user.
        """
        if not username:
            raise ValueError('Username is required.')

        if not phone_number:
            raise ValueError('Phone number is required.')

        if not password:
            raise ValueError('Password is required.')

        email = self.normalize_email(email) if email else ''
        username = self.model.normalize_username(username)

        user = self.model(
            username=username,
            email=email,
            phone_number=phone_number,
            role=role,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, phone_number=None, role=None, **extra_fields):
        """
        Create and save a regular user.
        """
        if role is None:
            role = self.model.Role.MEMBER

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(
            username=username,
            email=email,
            password=password,
            phone_number=phone_number,
            role=role,
            **extra_fields,
        )

    def create_superuser(self, username, email=None, password=None, phone_number=None, **extra_fields):
        """
        Create and save a superuser. Always role=owner, always staff+superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(
            username=username,
            email=email,
            password=password,
            phone_number=phone_number,
            role=self.model.Role.OWNER,
            **extra_fields,
        )