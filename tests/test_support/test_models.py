import pytest
from support.models import Contact, Report
from tests.test_company.test_models import user_data
from offer.models import JobOffer


@pytest.mark.django_db
def test_create_contact_success():
    contact = Contact.objects.create(
        subject="Test",
        message="Test test",
        email="test@example.com",
    )
    assert contact.subject == "Test"
    assert contact.message == "Test test"
    assert contact.email == "test@example.com"
    assert contact.reviewed == False
    assert contact.is_new == True
    assert contact.is_expired == False


@pytest.mark.django_db
def test_create_report_success(user_data):
    joboffer = JobOffer.objects.create(
        title="Test",
    )
    report = Report.objects.create(
        user=user_data,
        offer=joboffer,
        description="dasdasda",
    )
    assert report.user == user_data
    assert report.offer == joboffer
    assert report.description == "dasdasda"
    assert report.is_new == True
