from rest_framework import generics, validators
from ..models import * 
from ..serializers import *


# Create your views here.

class OwnerList(generics.ListCreateAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
class OwnerDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class ContactList(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ClientSerializer
    def get_queryset(self):
        ownerId = self.request.ownerId
        if ownerId is None or ownerId == '':
            raise validators.ValidationError({'ownerId': 'This field is required.'})
        return super().get_queryset().filter(owner_id=ownerId)

class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ClientSerializer
    
    def perform_update(self, serializer):
        ownerId = self.request.ownerId
        if self.get_object().ownerId == ownerId:
            raise validators.ValidationError({'ownerId': 'This field is required.'})
        return super().perform_update(serializer)