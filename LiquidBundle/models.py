from django.contrib.auth.models import User
from django.db import models


VALIDITY = [
    ('Daily', 'Daily'), ('7 Days', '7 Days'), ('30 Days', '30 Days'),
    ('Non Expiry', 'Non Expiry')
]


class LiquidDataPackage(models.Model):
    identifier = models.IntegerField(default=0)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    validity = models.CharField(max_length=255, choices=VALIDITY)

    def __str__(self):
        return self.name


class CompletedTransaction(models.Model):
    date_time_created = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=255)
    amount = models.FloatField()


class SavedTransaction(models.Model):
    first_name = models.CharField(max_length=255, default='N/A')
    last_name = models.CharField(max_length=255, default='N/A')
    datetime_created = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField()
    reference_number = models.CharField(max_length=255)
    request_reference = models.CharField(max_length=255)
    product_id = models.IntegerField()
    session_uuid = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    date_time_created = models.DateTimeField(auto_now_add=True)


class Agent(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ServiceCompany(models.Model):
    """
    A company providing the service that is being bought online.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    website = models.URLField()
    image = models.ImageField(upload_to='CompanyImages')
    dpo_company_token = models.CharField(max_length=255)
    active_status = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Service Companies'
