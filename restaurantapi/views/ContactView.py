from rest_framework import viewsets, filters, generics
from ..models import Owner, Contact, UserProfile
from ..serializers import OwnerSerializer, ClientSerializer, ProfileSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'phone_number']

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'phone_number']

    def get_queryset(self):
        queryset = super().get_queryset()
        owner = self.request.user.profile.owner
        if owner:
            queryset = queryset.filter(owner=owner)
        return queryset

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