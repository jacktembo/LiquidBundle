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
    package = models.ForeignKey(LiquidDataPackage, on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=255, default='Topup')
    lte_number = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.lte_number} - {self.package}"


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


class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    available_balance = models.FloatField(default=0.0)
    minimum_deposit = models.FloatField(default=20.00)

    def __str__(self):
        return f"{self.user} - {self.available_balance}"


class KazangSession(models.Model):
    session_uuid = models.CharField(max_length=255)
    date_time_created = models.DateTimeField(auto_now_add=True)


class PaymentTransaction(models.Model):
    session_uuid = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    amount = models.FloatField()
    reference_number = models.CharField(max_length=255)
