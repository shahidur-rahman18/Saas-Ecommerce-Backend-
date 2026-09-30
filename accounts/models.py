from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom User Manager
    সাধারণ ইউজার এবং সুপার-এডমিন তৈরির বিজনেস লজিক হ্যান্ডেল করে।
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('ইমেইল ঠিকানা অবশ্যই প্রদান করতে হবে।'))
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.Role.SUPER_ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser-এর জন্য is_staff=True হতে হবে।'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser-এর জন্য is_superuser=True হতে হবে।'))

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model
    প্ল্যাটফর্মের সেন্ট্রাল ইউজার যা Shared (Public) Schema-তে জমা থাকবে।
    """
    class Role(models.TextChoices):
        SUPER_ADMIN = 'SUPER_ADMIN', _('Super Admin')
        MERCHANT = 'MERCHANT', _('Merchant/Store Owner')
        STAFF = 'STAFF', _('Store Staff/Employee')
        CUSTOMER = 'CUSTOMER', _('End Customer')

    email = models.EmailField(_('email address'), unique=True, db_index=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=20, blank=True, null=True)
    
    role = models.CharField(
        max_length=20, 
        choices=Role.choices, 
        default=Role.CUSTOMER,
        help_text=_('ইউজারের রোল বা পারমিশন লেভেল')
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.role})"