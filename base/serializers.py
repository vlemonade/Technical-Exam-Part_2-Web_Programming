from rest_framework import serializers
from .models import Stock, Order


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'name', 'price']


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'stock', 'quantity', 'order_type', 'total_price'] 

    #to get the total amount of order and sell stock base on the quantity and stock price
    def get_total_price(self, obj):
        stock_price = obj.stock.price 
        return float(stock_price) * obj.quantity 
