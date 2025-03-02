from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import * 
from ..serializers import *

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
        owner = self.request.user.profile.owner
        if owner is None:
            return super().get_queryset()   
        return super().get_queryset().filter(owner=owner)

class ContactDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ClientSerializer

class ProfileView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    def get_queryset(self):
        print(self.request.user)
        return super().get_queryset().filter(user=self.request.user)

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializers = UserSerializer(request.user)
        return Response(serializers.data)