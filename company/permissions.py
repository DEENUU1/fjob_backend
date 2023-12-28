from rest_framework.permissions import BasePermission
from company.models import Company


class IsCompanyUser(BasePermission):
    message = "You do not have permission to access this resource."

    def has_permission(self, request, view):
        try:
            company = Company.objects.get(user=request.user)
            return company.user == request.user
        except Company.DoesNotExist:
            return False
