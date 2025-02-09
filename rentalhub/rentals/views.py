from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Equipment, Rental
from .serializers import EquipmentSerializer, RentalSerializer

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def available_items(self, request):
        """Endpoint zwracający dostępny sprzęt"""
        available = Equipment.objects.filter(available=True)
        serializer = self.get_serializer(available, many=True)
        return Response(serializer.data)

class RentalViewSet(viewsets.ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Automatyczne przypisanie użytkownika do wypożyczenia"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def user_rentals(self, request):
        """Endpoint zwracający wypożyczenia użytkownika"""
        rentals = Rental.objects.filter(user=request.user)
        serializer = self.get_serializer(rentals, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def rentals_summary(self, request):
        """Endpoint dla admina – zwraca liczbę wypożyczeń na sprzęt"""
        summary = Rental.objects.values('equipment__name').annotate(total=Count('id'))
        return Response(summary)

from django.shortcuts import render
import requests

def equipment_list(request):
    response = requests.get('http://127.0.0.1:8000/api/equipment/')
    equipment = response.json()  # Pobiera dane z API
    return render(request, 'rentals/equipment_list.html', {'equipment_list': equipment})
