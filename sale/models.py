from django.db import models
import uuid


class Depot(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=32, blank=False, null=False)
    code = models.CharField(max_length=32, unique=True)
    address = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = 'Depot'
        verbose_name_plural = 'Depots'

    def __str__(self):
        return self.name

class Customer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    code = models.CharField(max_length=32, unique=True, null=False, blank=False)
    address = models.CharField(max_length=200, blank=True, null=True)
    depot = models.ForeignKey(Depot, null=False, blank=False, on_delete=models.CASCADE, related_name='customers')

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    category_id = models.CharField(max_length=100, blank=True, null=True)
    category_name = models.CharField(max_length=100, blank=True, null=True)
    subcategory = models.ForeignKey(Subcategory, null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    size = models.CharField(max_length=100, null=True, blank=True)
    rate = models.FloatField(null=False, blank=True, default=0)

