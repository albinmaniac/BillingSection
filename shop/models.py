from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=30)
    discount = models.IntegerField()

    def __str__(self):
        return self.name


class Phone(models.Model):
    item = models.CharField(max_length=200)
    price = models.FloatField()

    def __str__(self):
        return self.item


class Transaction(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    qty = models.IntegerField()
    

    def get_discounted_total(self):
        total = self.qty * self.phone.price
        discount_amount = total * (self.customer.discount / 100)
        return total - discount_amount
    
    

    def __str__(self):
        return f"{self.customer.name} - {self.phone.item}"
    

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.FloatField()
    discount = models.IntegerField()
    grand_total = models.FloatField()

    def __str__(self):
        return f"Invoice #{self.id} - {self.customer.name}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE)
    qty = models.IntegerField()
    rate = models.FloatField()
    amount = models.FloatField()

    def __str__(self):
        return f"{self.phone.item} × {self.qty}"