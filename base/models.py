from django.db import models

#Stock Model
class Stock(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

#Order Model
class Order(models.Model):
    BUY = 'buy'
    SELL = 'sell'
    ORDER_TYPE_CHOICES = [
        (BUY, 'Buy'),
        (SELL, 'Sell'),
    ]

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_type = models.CharField(max_length=4, choices=ORDER_TYPE_CHOICES, default='BUY')

    def total_value(self):
        return self.stock.price * self.quantity
