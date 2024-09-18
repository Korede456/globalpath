from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", CustomUser.Role.ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# Custom User model
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()  # Assign the custom manager

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        EMPLOYER = "EMPLOYER", "Employer"
        JOBSEEKER = "JOBSEEKER", "Jobseeker"

    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


# Employer Manager
class EmployerManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=CustomUser.Role.EMPLOYER)


# Employer Model (Proxy)
class Employer(CustomUser):
    base_role = CustomUser.Role.EMPLOYER
    objects = EmployerManager()

    class Meta:
        proxy = True
        verbose_name = "Employer"
        verbose_name_plural = "Employers"

    def welcome(self):
        return "Only for employers"


# Employer Profile
class EmployerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=50, null=False)
    company_name = models.CharField(max_length=50, null=False)
    company_web_address = models.URLField(max_length=50, null=False)


# Jobseeker Manager
class JobseekerManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(role=CustomUser.Role.JOBSEEKER)


# Jobseeker Model (Proxy)
class Jobseeker(CustomUser):
    base_role = CustomUser.Role.JOBSEEKER
    objects = JobseekerManager()

    class Meta:
        proxy = True
        verbose_name = "Jobseeker"
        verbose_name_plural = "Jobseekers"

    def welcome(self):
        return "Only for job seekers"


# Signals to create profiles and add users to groups
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
     if created:
        if instance.role == CustomUser.Role.EMPLOYER:
            EmployerProfile.objects.create(user=instance)
            group = Group.objects.get(name="Employers")
            instance.groups.add(group)
        elif instance.role == CustomUser.Role.JOBSEEKER:
            group = Group.objects.get(name="Jobseekers")
            instance.groups.add(group)
