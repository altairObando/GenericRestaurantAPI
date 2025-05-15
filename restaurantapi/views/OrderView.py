from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from datetime import datetime
from ..models import Orders, OrderDetails
from ..serializers import OrdersSerializer, OrderDetailsSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['order_number', 'customer__name', 'waiter__username']
    ordering_fields = ['created_at', 'order_status']

    def perform_create(self, serializer):
        serializer.save(waiter=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        restaurant_id = self.request.query_params.get('restaurantId')

        if restaurant_id:
            queryset = queryset.filter(restaurant_id=restaurant_id)
        
        if user.profile.role == 'WAITER':
            queryset = queryset.filter(waiter=user)
            return queryset
        
        owner = user.profile.owner
        if owner:
            queryset = queryset.filter(location__restaurant__owner=owner)
            location_id = self.request.query_params.get('locationId')
            if location_id:
                queryset = queryset.filter(location_id=location_id)
        return queryset

    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        order = self.get_object()
        details = order.orderdetails_set.all()  # Cambiado de orderdetail_set a orderdetails_set
        serializer = OrderDetailsSerializer(details, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_detail(self, request, pk=None):
        order = self.get_object()
        serializer = OrderDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order=order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_detail(self, request, pk=None):
        try:
            detail_id = request.data.get('detail_id')
            detail = OrderDetails.objects.get(id=detail_id, order_id=pk)
            serializer = OrderDetailsSerializer(detail, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except OrderDetails.DoesNotExist:
            return Response({'error': 'Detail not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'])
    def remove_detail(self, request, pk=None):
        try:
            detail_id = request.query_params.get('detail_id')
            detail = OrderDetails.objects.get(id=detail_id, order_id=pk)
            detail.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except OrderDetails.DoesNotExist:
            return Response({'error': 'Detail not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status in ['PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED']:
            order.order_status = new_status
            order.save()
            return Response({'status': 'Order status updated'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_status(self, request):
        status_filter = request.query_params.get('status', 'PENDING')
        orders = self.get_queryset().filter(order_status=status_filter)
        
        # Aplicar paginación
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign_table(self, request, pk=None):
        order = self.get_object()
        table_number = request.data.get('table_number')
        if table_number:
            order.table_number = table_number
            order.save()
            return Response({'status': 'Table assigned successfully'})
        return Response({'error': 'Table number is required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def daily_summary(self, request):
        today = datetime.now().date()
        orders = self.get_queryset().filter(created_at__date=today)
        total_orders = orders.count()
        completed_orders = orders.filter(order_status='COMPLETED').count()
        total_sales = orders.filter(order_status='COMPLETED').aggregate(total=Sum('total_amount'))

        return Response({
            'total_orders': total_orders,
            'completed_orders': completed_orders,
            'total_sales': total_sales['total'] or 0,
            'date': today
        })