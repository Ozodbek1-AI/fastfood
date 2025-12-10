from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, AllowAny
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta

from .models import CourierProfile, Delivery, DeliveryHistory
from .serializers import (
    CourierRegistrationSerializer,
    CourierProfileSerializer,
    CourierStatusUpdateSerializer,
    DeliveryListSerializer,
    DeliveryDetailSerializer,
    DeliveryStatusUpdateSerializer,
    CourierStatsSerializer,
)
from .permissions import IsCourier, IsApprovedCourier, IsDeliveryCourier


class CourierRegistrationView(generics.CreateAPIView):
    """Courier ro'yxatdan o'tish"""
    serializer_class = CourierRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            'message': 'Muvaffaqiyatli ro\'yxatdan o\'tdingiz. Tez orada profilingiz tekshiriladi.',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_201_CREATED)


class CourierProfileViewSet(viewsets.ModelViewSet):
    """Courier profil boshqaruvi"""
    serializer_class = CourierProfileSerializer
    permission_classes = [AllowAny, IsCourier]

    def get_queryset(self):
        # Faqat o'z profilini ko'rish
        return CourierProfile.objects.filter(user=self.request.user)

    def get_object(self):
        return self.request.user.courier_profile

    @action(detail=False, methods=['get'])
    def me(self, request):
        """O'z profilini ko'rish"""
        profile = request.user.courier_profile
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['patch'])
    def update_status(self, request):
        """Online/Offline qilish"""
        profile = request.user.courier_profile
        serializer = CourierStatusUpdateSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Courier statistikasi"""
        profile = request.user.courier_profile
        deliveries = profile.user.deliveries.all()

        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        # Statistika hisoblash
        total_deliveries = deliveries.filter(status='delivered').count()
        completed_today = deliveries.filter(status='delivered', delivered_at__date=today).count()
        completed_this_week = deliveries.filter(status='delivered', delivered_at__date__gte=week_ago).count()
        completed_this_month = deliveries.filter(status='delivered', delivered_at__date__gte=month_ago).count()

        # Jami daromad
        total_earnings = deliveries.filter(status='delivered').aggregate(
            total=Sum('delivery_fee')
        )['total'] or 0

        # O'rtacha yetkazib berish vaqti
        completed = deliveries.filter(
            status='delivered',
            picked_up_at__isnull=False,
            delivered_at__isnull=False
        )

        avg_time = timedelta(0)
        if completed.exists():
            times = []
            for d in completed:
                if d.picked_up_at and d.delivered_at:
                    times.append(d.delivered_at - d.picked_up_at)
            if times:
                avg_time = sum(times, timedelta(0)) / len(times)

        # Success rate
        total_assigned = deliveries.filter(
            status__in=['assigned', 'picked_up', 'on_the_way', 'delivered', 'cancelled']
        ).count()
        success_rate = (total_deliveries / total_assigned * 100) if total_assigned > 0 else 0

        stats = {
            'total_deliveries': total_deliveries,
            'completed_today': completed_today,
            'completed_this_week': completed_this_week,
            'completed_this_month': completed_this_month,
            'total_earnings': total_earnings,
            'average_delivery_time': avg_time,
            'success_rate': round(success_rate, 2)
        }

        serializer = CourierStatsSerializer(stats)
        return Response(serializer.data)


class DeliveryViewSet(viewsets.ModelViewSet):
    """Yetkazib berish boshqaruvi"""
    permission_classes = [AllowAny, IsApprovedCourier]

    def get_serializer_class(self):
        if self.action == 'list':
            return DeliveryListSerializer
        elif self.action in ['update_status', 'partial_update']:
            return DeliveryStatusUpdateSerializer
        return DeliveryDetailSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Delivery.objects.select_related('order', 'courier').all()

        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    @action(detail=False, methods=['get'])
    def available(self, request):
        """Mavjud buyurtmalar (tayinlanmagan)"""
        deliveries = Delivery.objects.filter(
            status='pending',
            courier__isnull=True
        ).select_related('order', 'order__user')

        serializer = DeliveryListSerializer(deliveries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_deliveries(self, request):
        """Mening buyurtmalarim"""
        deliveries = Delivery.objects.filter(
            courier=request.user
        ).exclude(status='delivered').select_related('order', 'order__user')

        serializer = DeliveryListSerializer(deliveries, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Yakunlangan buyurtmalar"""
        deliveries = Delivery.objects.filter(
            courier=request.user,
            status='delivered'
        ).select_related('order', 'order__user').order_by('-delivered_at')

        serializer = DeliveryListSerializer(deliveries, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """Buyurtmani qabul qilish"""
        delivery = self.get_object()

        if delivery.courier is not None:
            return Response(
                {'error': 'Bu buyurtma allaqachon qabul qilingan'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if delivery.status != 'pending':
            return Response(
                {'error': 'Bu buyurtmani qabul qilish mumkin emas'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Courier ni tayinlash
        delivery.courier = request.user
        delivery.status = 'assigned'
        delivery.assigned_at = timezone.now()
        delivery.save()

        # Tarixga yozish
        DeliveryHistory.objects.create(
            delivery=delivery,
            status='assigned',
            note='Courier buyurtmani qabul qildi'
        )

        serializer = DeliveryDetailSerializer(delivery)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[AllowAny, IsDeliveryCourier])
    def update_status(self, request, pk=None):
        """Status yangilash"""
        delivery = self.get_object()
        serializer = DeliveryStatusUpdateSerializer(delivery, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Status yangilandi',
            'delivery': DeliveryDetailSerializer(delivery).data
        })

    @action(detail=True, methods=['post'], permission_classes=[AllowAny, IsDeliveryCourier])
    def cancel(self, request, pk=None):
        """Buyurtmani bekor qilish"""
        delivery = self.get_object()

        if delivery.status == 'delivered':
            return Response(
                {'error': 'Yetkazib berilgan buyurtmani bekor qilish mumkin emas'},
                status=status.HTTP_400_BAD_REQUEST
            )

        reason = request.data.get('reason', '')

        delivery.status = 'cancelled'
        delivery.courier = None
        delivery.save()

        DeliveryHistory.objects.create(
            delivery=delivery,
            status='cancelled',
            note=f'Bekor qilindi: {reason}'
        )

        return Response({'message': 'Buyurtma bekor qilindi'})

