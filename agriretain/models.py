
from django.db import models

class Customer(models.Model):
    customerID = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=10)
    SeniorCitizen = models.BooleanField(null=True)
    Partner = models.BooleanField()
    Dependents = models.BooleanField()
    tenure = models.IntegerField()
    PhoneService = models.BooleanField()
    MultipleLines = models.CharField(max_length=50,null=True)
    InternetService = models.CharField(max_length=50,null=True)
    OnlineSecurity = models.CharField(max_length=50,null=True)
    OnlineBackup = models.CharField(max_length=50,null=True)
    DeviceProtection = models.CharField(max_length=50,null=True)
    TechSupport = models.CharField(max_length=50,null=True)
    StreamingTV = models.CharField(max_length=50,null=True)
    StreamingMovies = models.CharField(max_length=50,null=True)
    Contract = models.CharField(max_length=50, null=True)
    PaperlessBilling = models.BooleanField()
    PaymentMethod = models.CharField(max_length=100,null=True)
    MonthlyCharges = models.FloatField()
    TotalCharges = models.FloatField()
    Churn = models.BooleanField()

    def __str__(self):
        return self.customerID

