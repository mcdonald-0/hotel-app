from django.core.validators import RegexValidator

from django.contrib.auth.models import PermissionsMixin, BaseUserManager, AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.db import models

from helpers.models import TrackingModel

from phonenumber_field.modelfields import PhoneNumberField


class AccountManager(BaseUserManager):

    def create_user(self, email, username=None, password=None):
        if not email:
            raise ValueError('Users must have an email address!')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, TrackingModel):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with this username already exists."),
        },
    )
    email = models.EmailField(_('email address'), unique=True,
                              error_messages={
                                  'unique': _("A user with this email already exists."),
                              },
                              )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_admin = models.BooleanField(
        _('admin status'),
        default=False,
        help_text=_('Designates whether the user is an admin.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    email_verified = models.BooleanField(
        _('email_verified'),
        default=False,
        help_text=_(
            "Designates whether this user's email is verified."
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login = models.DateTimeField(_('last login'), auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def is_email_verified(self):
        return self.email_verified

    def has_module_perms(self, app_label):
        return True


class Guest(TrackingModel):
    user = models.OneToOneField(User, related_name="guest", on_delete=models.CASCADE, null=True)
    email = models.EmailField(_('email address'), null=True, unique=True, error_messages={'unique': _("A user with this email already exists.")})
    phone_number = PhoneNumberField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    next_of_kin_number = PhoneNumberField(unique=True, null=False, blank=False)

    def __str__(self):
        return f'{ self.first_name } { self.last_name }'
