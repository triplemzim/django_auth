from django.db import models
import uuid
from django.utils import timezone
from django.contrib.auth.models import User



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
    depot = models.ForeignKey(Depot, null=False, blank=False, on_delete=models.CASCADE, related_name='customer')

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)

    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    code = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    category_id = models.CharField(max_length=100, blank=True, null=True)
    category_name = models.CharField(max_length=100, blank=True, null=True)
    subcategory = models.ForeignKey(Subcategory, null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    size = models.CharField(max_length=100, null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.code


class Balance(models.Model):

    TRANSACTION_CHOICES = (
        ('Debit', 'Debit'),
        ('Credit', 'Credit')
    )
    PAYMENT_CHOICES = (
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('MobileWallet', 'MobileWallet'),
        ('Bank', 'Bank')
    )

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='balance')
    transaction_id = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_time = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=10, default='Debit', choices=TRANSACTION_CHOICES)
    payment_method = models.CharField(max_length=20, default='Cash', choices=PAYMENT_CHOICES)
    entry_user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    invoice = models.ForeignKey('Invoice', on_delete=models.SET_NULL, null=True, blank=True, related_name='balance')



    def __str__(self):
        return f"{self.category} for {self.customer}" 


class Stock(models.Model):
    id = models.BigAutoField(primary_key=True)
    depot = models.ForeignKey(Depot, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'
        constraints = [
            models.UniqueConstraint(
                fields=['depot', 'product'],
                name='unique for stock'
            )
        ]

    def __str__(self):
        return str(self.product.name) + '-' + str(self.depot.name)



class Invoice(models.Model):
    PAYMENT_STATUS = (
        ("Full", "Full"),
        ("Partial", "Partial"),
        ("Due", "Due")
    )
    PAYMENT_CHOICES = (
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('MobileWallet', 'MobileWallet'),
        ('Bank', 'Bank')
    )

    invoice_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    invoice_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="Partial")
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='Cash')
    custom_invoice_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Invoice #{self.custom_invoice_id}"
    

class LineItem(models.Model):
    line_item_id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='lineitem', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Line Item #{self.line_item_id} in Invoice #{self.invoice}"

        



