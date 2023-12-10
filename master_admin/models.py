from django.db import models

# Create your models here.


class BranchAdminInfo(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=20)
    address = models.CharField(max_length=10000)
    DateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.firstName} {self.lastName} {self.id}"


class BranchInfo(models.Model):
    branchName = models.CharField(max_length=1000)
    locationAddress = models.CharField(max_length=10000)
    branchAdmin = models.ForeignKey(BranchAdminInfo, on_delete=models.CASCADE)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=10)
    country = models.CharField(max_length=200)
    DateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.branchName} {self.id}"
