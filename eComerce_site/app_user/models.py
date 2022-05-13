from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.forms import IntegerField
from django.utils.translation import gettext_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class AltBaseUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("the Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(
        gettext_lazy('staff status'),
        default=False,
        help_text = gettext_lazy('Designates whether the user can log in this site')
    )
    is_active = models.BooleanField(
        gettext_lazy('active'),
        default=True,
        help_text = gettext_lazy('Designates whether this should be treated as active. unselect instead of deleting account.')
    )

    user_types = [
        ('Buyer', 'Buyer'),
        ('Vendor', 'Vendor'),
    ]
    account_type = models.CharField(
        max_length=64,
        choices=user_types,
        default='Buyer',
        help_text= gettext_lazy("Vendors has their own shops/Buyers can buy products.")
    )

    USERNAME_FIELD = 'email'
    object = AltBaseUserManager()

    def __str__(self) -> str:
        return self.email
    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userProfile")
    username = models.CharField(max_length=264, blank=True)
    full_name = models.CharField(max_length=264, blank=True)
    address = models.TextField(max_length=500, blank=True)
    city = models.CharField(max_length=50, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    coupons_bronze = models.IntegerField(default=0)
    coupons_gold = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.username + "'s profile"

    def is_fully_filled(self):
        field_names = [f.name for f in self._meta.get_fields()]

        for field_name in field_names:
            value = getattr(self, field_name)
            if value is None or value=="":
                print("-------------------------false returned for ", value)
                return False
        print("----------------True returned")
        return True

@receiver(post_save, sender=User)
def userProfileCreate(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
@receiver(post_save, sender=User)
def saveUserProfile(sender, instance, **kwargs):
    instance.userProfile.save()