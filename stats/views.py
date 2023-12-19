from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth, TruncYear
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Statistics
from .serializers import StatisticsSerializer


class StatisticsDayView(APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request, year, month, day, model_type=None):
        queryset = Statistics.objects.filter(
            created_at__year=year, created_at__month=month, created_at__day=day
        ).filter(model_type=model_type) if model_type else Statistics.objects.filter(
            created_at__year=year, created_at__month=month, created_at__day=day
        )
        serializer = StatisticsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StatisticsMonthView(APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request, year, month, model_type=None):
        queryset = Statistics.objects.filter(
            created_at__year=year, created_at__month=month
        ).filter(model_type=model_type) if model_type else Statistics.objects.filter(
            created_at__year=year, created_at__month=month
        )
        serializer = StatisticsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StatisticsYearView(APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request, year, model_type=None):
        queryset = Statistics.objects.filter(
            created_at__year=year
        ).filter(model_type=model_type) if model_type else Statistics.objects.filter(
            created_at__year=year
        )
        serializer = StatisticsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StatisticsAggregatedView(APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request, scale, model_type=None):
        if scale == 'day':
            queryset = Statistics.objects.annotate(date=TruncDay('created_at')).values('date').annotate(
                count=Count('id')).filter(model_type=model_type) if model_type else Statistics.objects.annotate(
                date=TruncDay('created_at')).values('date').annotate(count=Count('id'))
        elif scale == 'month':
            queryset = Statistics.objects.annotate(date=TruncMonth('created_at')).values('date').annotate(
                count=Count('id')).filter(model_type=model_type) if model_type else Statistics.objects.annotate(
                date=TruncMonth('created_at')).values('date').annotate(count=Count('id'))
        elif scale == 'year':
            queryset = Statistics.objects.annotate(date=TruncYear('created_at')).values('date').annotate(
                count=Count('id')).filter(model_type=model_type) if model_type else Statistics.objects.annotate(
                date=TruncYear('created_at')).values('date').annotate(count=Count('id'))
        else:
            return Response(
                {
                    "error": "Invalid scale. Supported scales are 'day', 'month', and 'year'."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = StatisticsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ModelTypeListView(APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request):
        queryset = Statistics.objects.values('model_type').distinct()
        serializer = StatisticsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
