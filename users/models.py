from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, name='', is_customer=False, is_seller=False, is_service_seller=False,):

        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.name = name
        user.is_customer = is_customer
        user.is_seller = is_seller
        user.is_service_seller = is_service_seller
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(verbose_name='Username', max_length=60, unique=True)
    name = models.CharField(verbose_name='name', max_length=60)
    # date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_service_seller = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


# security question model for user to make their account secure
class Security_question(models.Model):
    question = models.CharField(max_length=100, default='Add security question')

    def __str__(self):
        return f'{self.question}'

# security question's answer
class Answer(models.Model):
    user          = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    user_question = models.ForeignKey(Security_question, on_delete=models.CASCADE)
    user_answer   = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.user}||{self.user_question}||{self.user_answer}'

