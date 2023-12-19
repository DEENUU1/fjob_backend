from django.urls import path

from .views import (
    StatisticsDayView,
    StatisticsMonthView,
    StatisticsYearView,
    StatisticsAggregatedView,
    ModelTypeListView,
)

urlpatterns = [
    path('day/<int:year>/<int:month>/<int:day>/', StatisticsDayView.as_view(), name='statistics-day'),
    path('month/<int:year>/<int:month>/', StatisticsMonthView.as_view(), name='statistics-month'),
    path('year/<int:year>/', StatisticsYearView.as_view(), name='statistics-year'),
    path('aggregated/<str:scale>/', StatisticsAggregatedView.as_view(), name='statistics-aggregated'),
    path('model/', ModelTypeListView.as_view(), name='model-type-list'),
]
