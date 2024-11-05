from rest_framework import viewsets, status 
from rest_framework.response import Response
from .models import Stock, Order
from .serializers import StockSerializer, OrderSerializer


#User Profile and viewing of total invesment
class ProfileViewSet(viewsets.ViewSet):
    def list(self, request):
        total_investment = sum(order.total_value() for order in Order.objects.filter(order_type=Order.BUY))
        return Response({"total_investment": total_investment})
    

# To handle request for stock objects
class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


# To handle buying and selling stockstock orders, and viewing owned stocks
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    #List to show the owned stock
    def list(self, request, *args, **kwargs):
        buy_orders = Order.objects.filter(order_type__iexact='buy')

        # Group the owned stock base on the stock ID
        orders = {}
        for order in buy_orders:
            if order.stock in orders:
                orders[order.stock]['quantity'] += order.quantity
                orders[order.stock]['total_value'] += float(order.stock.price) * order.quantity
            else:
                orders[order.stock] = {
                    'id': order.stock.id, 
                    'stock_name': order.stock.name,
                    'quantity': order.quantity,
                    'total_value': float(order.stock.price) * order.quantity
                }

        # Convert  orders to a list format
        response_data = list(orders.values())
        # Orginize orders by stock ID, for easy viewing
        response_data.sort(key=lambda x: x['id'])

        return Response(response_data, status=status.HTTP_200_OK)

    # To handle creating new buy or sell orders for stocks.
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_type = serializer.validated_data.get('order_type')
        stock = serializer.validated_data.get('stock')
        quantity = serializer.validated_data.get('quantity')
        
        # Sell or Buy Stock
        if order_type == Order.SELL:
            # Check if there are enough buy orders for the stock to sell the requested quantity
            bought_quantity = sum(order.quantity for order in Order.objects.filter(stock=stock, order_type__iexact='buy'))

            if bought_quantity < quantity:
                # Not enough quantity bought to sell
                return Response(
                    {"error": "Not enough stock bought to fulfill the sell order."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Handle sell orders: update the existing buy orders
            existing_buy_orders = Order.objects.filter(stock=stock, order_type__iexact='buy').order_by('id')

            total_sold = quantity
            for order in existing_buy_orders:
                if total_sold <= 0:
                    break

                if order.quantity > total_sold:
                    # Reduce the quantity in the existing order
                    order.quantity -= total_sold
                    order.save()
                    total_sold = 0
                else:
                    # If the order quantity is less than or equal to what's being sold, delete it
                    total_sold -= order.quantity
                    order.delete()

            if total_sold > 0:
                return Response(
                    {"error": "Failed to fulfill the entire sell order."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        elif order_type == Order.BUY:
            # Check for existing buy order for the same stock
            existing_order = Order.objects.filter(stock=stock, order_type__iexact='buy').first()
            if existing_order:
                existing_order.quantity += quantity 
                existing_order.save()
                return Response(OrderSerializer(existing_order).data, status=status.HTTP_200_OK)

        # If no existing order, create a new one
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)