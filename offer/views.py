from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import (
    WorkType,
    EmploymentType,
    Experience,
    Salary,
    JobOffer
)
from .serializers import (
    WorkTypeSerializer,
    EmploymentTypeSerializer,

)


class WorkTypeView(ViewSet):

    def list(self, request):
        work_types = WorkType.objects.all()
        serializer = WorkTypeSerializer(work_types, many=True)
        return Response(serializer.data)


class EmploymentTypeView(ViewSet):

    def list(self, request):
        employment_types = EmploymentType.objects.all()
        serializer = EmploymentTypeSerializer(employment_types, many=True)
        return Response(serializer.data)
