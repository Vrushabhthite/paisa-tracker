from django.conf import settings
from django.db import models
from django.utils import timezone

TYPES = [("INCOME", "Income (salary/aamdani)"), ("EXPENSE", "Expense (kharcha)"),
         ("RECEIVED", "Kisi ne diya (received)"), ("LENT", "Maine kisi ko diya (udhaar)"),
         ("REPAID", "Udhaar wapas mila"), ("SAVING", "Saving (bachat)")]
ADD = ["INCOME", "RECEIVED", "REPAID"]    # balance badhata hai
SUB = ["EXPENSE", "LENT", "SAVING"]       # balance ghatata hai

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=60, blank=True, help_text="Food, Rent, Travel...")
    person = models.CharField(max_length=80, blank=True, help_text="Kisne diya / kisko diya")
    date = models.DateField(default=timezone.localdate)
    note = models.CharField(max_length=200, blank=True)
    class Meta:
        ordering = ["-date", "-id"]

class Budget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.DateField()  # first day of month
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    class Meta:
        unique_together = ("user", "month")
