from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Level(models.Model):
    level = models.CharField(max_length=50)
    
    def __str__(self):
        return self.level
    
    class Meta:
        verbose_name_plural = '1.Level Akses'


class HakAkses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name_plural = '4.Hak Akses'


class StatusAbsen(models.Model):
    status = models.CharField(max_length=50)    
    
    def __str__(self):
        return self.status
    
    class Meta:
        verbose_name_plural = '2.Status Absen'        


class Karyawan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama
    
    class Meta:
        verbose_name_plural = '3.Karyawan'       


class Absensi(models.Model):
    karyawan = models.ForeignKey(Karyawan, on_delete=models.CASCADE)
    status = models.ForeignKey(StatusAbsen, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __int__(self):
        return self.karyawan
    
    class Meta:
        verbose_name_plural = 'Absensi'