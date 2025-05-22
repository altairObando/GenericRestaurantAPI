from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Q
from datetime import datetime
from ..models import Orders, OrderDetails, OrderTaxes, Tax
from ..serializers import OrdersSerializer, OrderDetailsSerializer
from datetime import datetime
from GenericRestaurantAPI.utils import evaluate_formula
from django.forms.models import model_to_dict
class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing restaurant orders.
    
    Provides CRUD operations and additional actions for order management.
    Handles order details, status changes, and financial calculations.
    """
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['order_number', 'customer__name', 'waiter__username']
    ordering_fields = ['created_at', 'order_status', 'id']
    def perform_create(self, serializer):
        """
        Crea una nueva orden y asigna los impuestos obligatorios del restaurante.
        
        Args:
            serializer: Serializer de la orden
            
        Efectos:
            - Asigna el mesero actual como creador de la orden
            - Agrega los impuestos obligatorios del restaurante
            - Inicializa los montos de impuestos en cero
        """
        order = serializer.save(waiter=self.request.user)
        
        # Obtener impuestos obligatorios del restaurante
        restaurant_taxes = Tax.objects.filter(
            restaurant=order.location.restaurant,
            mandatory=True,
            is_active=True
        ).filter(
           Q(valid_to__isnull=True) | Q(valid_to__gte=datetime.now().date())
        )
        
        # Crear OrderTaxes para cada impuesto obligatorio
        for tax in restaurant_taxes:
            OrderTaxes.objects.create(
                tax=tax,
                order=order,
                amount=0  # El monto se calculará cuando se actualice el total
            )
        
        # Actualizar el total de la orden para calcular los impuestos
        self.update_total_order(order.id)

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
        """
        Retrieve all details for a specific order.        
        Args:
            request: HTTP request object
            pk (int): Primary key of the order            
        Returns:
            Response: List of order details with their items and quantities
        """
        order = self.get_object()
        details = order.OrderDetails_set.all()
        serializer = OrderDetailsSerializer(details, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_detail(self, request, pk=None):
        """
        Add a new item detail to an existing order.
        
        Args:
            request: HTTP request object containing item details
            pk (int): Primary key of the order
            
        Returns:
            Response: Created order detail data or validation errors
            
        Triggers:
            - Order total recalculation after adding item
        """
        order = self.get_object()
        serializer = OrderDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order=order)
            self.update_total_order(order.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_detail(self, request, pk=None):
        """
        Update an existing order detail.
        
        Args:
            request: HTTP request object with updated detail data
            pk (int): Primary key of the order
            
        Required Parameters:
            - detail_id: ID of the order detail to update            
        Returns:
            Response: Updated detail data or error message
            
        Triggers:
            - Order total recalculation after update
        """
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
        """
        Remove a detail from an order.
        
        Args:
            request: HTTP request object
            pk (int): Primary key of the order
            
        Query Parameters:
            - detail_id: ID of the order detail to remove
            
        Returns:
            Response: Deletion confirmation with removed item details
            
        Triggers:
            - Order total recalculation after deletion
        """
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
        """
        Update the status of an order.
        
        Args:
            request: HTTP request object
            pk (int): Primary key of the order
            
        Required Parameters:
            - status: New status (RESERVED, ACTIVE, DELIVERED, CANCELLED, PAID)
            
        Returns:
            Response: Status update confirmation or error message
        """
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status in ['RESERVED', 'ACTIVE', 'DELIVERED', 'CANCELLED', 'PAID']:
            order.order_status = new_status
            order.save()
            return Response({'status': 'Order status updated'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def by_status(self, request):
        """
        Retrieve orders filtered by status.
        
        Query Parameters:
            - status: Order status to filter by (default: PENDING)
            
        Returns:
            Response: List of orders with the specified status
        """
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
        """
        Retrieve order history excluding active orders.
        
        Query Parameters:
            - date: Filter by specific date (format: YYYY-MM-DD)
            
        Returns:
            Response: List of historical orders
        """
        orders = self.get_queryset().exclude(order_status__exact='ACTIVE')
        date_filter = request.query_params.get('date')
        if date_filter:
            date_filter = datetime.strptime(date_filter, '%Y-%m-%d').date()
            orders = orders.filter(created_at__date=date_filter)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign_table(self, request, pk=None):
        """
        Assign a table number to an order.
        
        Args:
            request: HTTP request object
            pk (int): Primary key of the order
            
        Required Parameters:
            - table_number: Number of the table to assign
            
        Returns:
            Response: Assignment confirmation or error message
        """
        order = self.get_object()
        table_number = request.data.get('table_number')
        if table_number:
            order.table_number = table_number
            order.save()
            return Response({'status': 'Table assigned successfully'})
        return Response({'error': 'Table number is required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def daily_summary(self, request):
        """
        Generate a summary of orders for the current day.
        
        Query Parameters:
            - waiterId: Filter by specific waiter
            - restaurantId: Filter by specific restaurant
            
        Returns:
            Response: Daily summary including:
                - Total orders
                - Completed orders
                - Total sales
                - Applied filters
        """
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

    def update_total_order(self, order_id):
        """
        Update the total amount for an order.        
        Args:
            order_id (int): ID of the order to update
        Calculates:
            - Subtotal from order details
            - Total including taxes
        Raises:
            ValueError: If order not found or calculation error occurs
        """
        try:
            order = Orders.objects.get(id=order_id)
            total_details = order.OrderDetails_set.aggregate(total=Sum('total'))
            order.subtotal = total_details['total'] or 0            
            # Calculate taxes - Optimized query
            orderTaxes = OrderTaxes.objects.select_related('tax').filter(order=order)
            if orderTaxes:
                for item in orderTaxes:
                    tax_amount = 0
                    if item.tax.percentage is not None and float(item.tax.percentage) > 0:
                        tax_amount = (item.tax.percentage * order.subtotal / 100)
                    elif item.tax.formula is not None and len(item.tax.formula) > 0:
                        tax_amount = evaluate_formula(item.tax.formula, { "order": model_to_dict(order),"details": [model_to_dict(detail) for detail in order.OrderDetails_set.all()]})                   
                    # Actualizar el monto del impuesto
                    OrderTaxes.objects.filter(id=item.id).update(amount=tax_amount)                
                # Recalcular el total de impuestos
                order.taxes = orderTaxes.aggregate(total=Sum('amount'))['total']            
            order.total = order.subtotal + (order.taxes or 0)
            order.save()
            
        except Orders.DoesNotExist:
            raise ValueError(f"Order with id {order_id} not found")
        except Exception as e:
            raise ValueError(f"Error updating order total: {str(e)}")
    