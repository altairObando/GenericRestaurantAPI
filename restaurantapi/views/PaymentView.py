from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime
from ..models import PaymentMethod, SplitPayment
from ..serializers import PaymentMethodSerializer, SplitPaymentSerializer

class PaymentMethodViewSet(viewsets.ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=(is_active.lower() == 'true'))
        return queryset

class SplitPaymentViewSet(viewsets.ModelViewSet):
    queryset = SplitPayment.objects.all()
    serializer_class = SplitPaymentSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['order__id', 'payment_method__name', 'reference']
    ordering_fields = ['created_at', 'amount_paid_by_customer']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        owner = user.profile.owner
        
        if owner:
            queryset = queryset.filter(order__location__restaurant__owner=owner)
            
        order_id = self.request.query_params.get('orderId')
        if order_id:
            queryset = queryset.filter(order_id=order_id)
            
        payment_method_id = self.request.query_params.get('paymentMethodId')
        if payment_method_id:
            queryset = queryset.filter(payment_method_id=payment_method_id)
            
        is_refunded = self.request.query_params.get('is_refunded')
        if is_refunded is not None:
            queryset = queryset.filter(is_refunded=(is_refunded.lower() == 'true'))
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        """Mark a payment as refunded"""
        payment = self.get_object()
        if payment.is_refunded:
            return Response({'error': 'Payment already refunded'}, status=status.HTTP_400_BAD_REQUEST)
        
        payment.is_refunded = True
        payment.refunded_at = datetime.now()
        payment.save()
        
        serializer = self.get_serializer(payment)
        return Response(serializer.data)