from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    # this model is created to modify the user_auth model so we can use it for authentication and grant permission or authorization based on users's level
    # the "isBranchchAdmin" represents the branch admin while the tas admin will be represented by the default "is_superuser"
    isBranchAdmin = models.BooleanField(default=False)
    isParent = models.BooleanField(default=False)
    isStudent = models.BooleanField(default=False)
    isEmployee = models.BooleanField(default=False)
    isTutor = models.BooleanField(default=False)
    isVerified = models.BooleanField(default=False)


class OTPModel(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=1000)
    DateTime = models.DateTimeField(auto_now_add=True)
