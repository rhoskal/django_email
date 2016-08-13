from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.signals import user_logged_in
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

class BaseUserManager(models.Manager):
    @classmethod
    def normalize_email(cls, email):
        email = email or ''

        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name.lower(), domain_part.lower()])
        return email

    def get_by_natural_key(self, email):
        return self.get(**{self.model.USERNAME_FIELD: email})

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have a valid email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class Client(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    account_locked = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    failed_login_attempts = models.PositiveIntegerField(null=True, default=0, editable=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['first_name', 'last_name']

    USERNAME_FIELD = 'email'

    def clean(self):
        super(Client, self).clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_full_name(self):
        full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name.strip()

    def get_email(self):
        return self.email

    def get_short_name(self):
        return self.first_name

    def natural_key(self):
        return (self.get_email(), )

def update_last_login(sender, user, **kwargs):
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])

user_logged_in.connect(update_last_login)
