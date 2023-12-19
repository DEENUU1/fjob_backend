import pytest

from candidate.models import Candidate
from offer.models import JobOffer
from users.models import UserAccount


@pytest.mark.django_db
def test_create_candidate_success():
    user = UserAccount.objects.create(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        password="XXXXXXXX",
    )
    job_offer = JobOffer.objects.create(
        title="Software Engineer",
    )
    candidate = Candidate.objects.create(
        full_name="John Doe",
        email="john@example.com",
        phone="1234567890",
        offer=job_offer,
        resume="path/to/cv.pdf",
        message="Hello",
        user=user,
    )

    assert candidate.full_name == "John Doe"
    assert candidate.email == "john@example.com"
    assert candidate.phone == "1234567890"
    assert candidate.offer == job_offer
    assert candidate.resume == "path/to/cv.pdf"
    assert candidate.message == "Hello"
