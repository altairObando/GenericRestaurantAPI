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
    ordering_fields = ['created_at', 'order_status', 'id']

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
        details = order.OrderDetails_set.all()
        serializer = OrderDetailsSerializer(details, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_detail(self, request, pk=None):
        order = self.get_object()
        serializer = OrderDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order=order)
            self.update_total_order(order.id)
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
                self.update_total_order(order.id)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except OrderDetails.DoesNotExist:
            return Response({'error': 'Detail not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['delete'])
    def remove_detail(self, request, pk=None):
        try:
            detail_id = request.query_params.get('detail_id')
            if not detail_id:
                return Response(
                    {'error': 'Detail ID is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            order = self.get_object()
            detail = OrderDetails.objects.get(id=detail_id, order_id=pk)
            
            # Save information before deletion for response
            detail_info = {
                'id': detail.id,
                'item_name': detail.item.name if detail.item else None,
                'quantity': detail.quantity,
                'item_price': detail.item_price,  # Cambiado de price a item_price
                'total': detail.total  # Agregado total para más información
            }
            
            detail.delete()
            self.update_total_order(pk)
            return Response({
                'message': 'Order detail successfully deleted',
                'deleted_item': detail_info,
                'order_id': pk
            }, status=status.HTTP_200_OK)
            
        except OrderDetails.DoesNotExist:
            return Response({
                'error': 'Order detail not found',
                'detail': f'Detail with ID {detail_id} not found for order {pk}'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': 'Error deleting order detail',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status in ['RESERVED', 'ACTIVE', 'DELIVERED', 'CANCELLED', 'PAID']:
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
    @action(detail=False, methods=['get'])
    def history(self,request):
        orders = self.get_queryset().filter(order_status!='ACTIVE')
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

        # Filtro opcional por mesero
        waiter_id = request.query_params.get('waiterId')
        if waiter_id:
            orders = orders.filter(waiter_id=waiter_id)

        # Filtro opcional por restaurante
        restaurant_id = request.query_params.get('restaurantId')
        if restaurant_id:
            orders = orders.filter(location__restaurant_id=restaurant_id)

        total_orders = orders.count()
        completed_orders = orders.filter(order_status='PAID').count()
        total_sales = orders.filter(order_status='PAID').aggregate(total=Sum('total'))

        return Response({
            'total_orders': total_orders,
            'completed_orders': completed_orders,
            'total_sales': total_sales['total'] or 0,
            'date': today,
            'filters_applied': {
                'waiter_id': waiter_id if waiter_id else None,
                'restaurant_id': restaurant_id if restaurant_id else None
            }
        })

    def update_total_order(self, orderId):
        try:
            order = Orders.objects.get(id=order_id)
            total_details = order.OrderDetails_set.aggregate(total=Sum('total'))
            order.subtotal = total_details['total'] or 0
            order.total = order.subtotal + (order.taxes or 0)
            order.save()
        except Orders.DoesNotExist:
            raise ValueError(f"Order with id {order_id} not found")
        except Exception as e:
            raise ValueError(f"Error updating order total: {str(e)}")
    
