import io
import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status

from apps.courses.models import Course, Lecture
from common.enums import UserRole


pytestmark = pytest.mark.django_db
User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def teacher(db):
    return User.objects.create_user(
        email="teacher@example.com",
        password="pass12345",
        role=UserRole.TEACHER.value,
        first_name="T",
        last_name="One",
    )


@pytest.fixture
def other_teacher(db):
    return User.objects.create_user(
        email="teacher2@example.com",
        password="pass12345",
        role=UserRole.TEACHER.value,
        first_name="T2",
        last_name="Two",
    )


@pytest.fixture
def student(db):
    return User.objects.create_user(
        email="student@example.com",
        password="pass12345",
        role=UserRole.STUDENT.value,
        first_name="S",
        last_name="One",
    )


def auth(client: APIClient, user: User) -> APIClient:
    client.force_authenticate(user)
    return client


def test_create_course_and_list_counts(api_client, teacher, student):
    # Create course
    create_resp = auth(api_client, teacher).post(
        "/api/courses/",
        {"name": "C1", "description": "Desc"},
        format="json",
    )
    assert create_resp.status_code in (status.HTTP_201_CREATED, status.HTTP_200_OK)

    # List with counts
    list_resp = auth(api_client, teacher).get("/api/courses/?page=1&page_size=10")
    assert list_resp.status_code == status.HTTP_200_OK
    assert list_resp.data["results"][0]["teacher_count"] >= 1
    assert list_resp.data["results"][0]["student_count"] >= 1


def test_course_update_permissions(api_client, teacher, other_teacher):
    c = Course.objects.create(name="C2", description="D", primary_owner=teacher)
    c.teachers.add(teacher)

    # Non-owner cannot patch
    resp_forbidden = auth(api_client, other_teacher).patch(
        f"/api/courses/{c.id}/", {"description": "Hack"}, format="json"
    )
    assert resp_forbidden.status_code == status.HTTP_403_FORBIDDEN

    # Owner can patch
    resp_ok = auth(api_client, teacher).patch(
        f"/api/courses/{c.id}/", {"description": "Updated"}, format="json"
    )
    assert resp_ok.status_code == status.HTTP_200_OK
    assert resp_ok.data["description"] == "Updated"


def test_lecture_crud_with_file_upload(api_client, teacher):
    # Setup course
    c = Course.objects.create(name="C3", description="D", primary_owner=teacher)
    c.teachers.add(teacher)

    # Create lecture with file (multipart)
    file_bytes = b"fake-pdf"
    uploaded = SimpleUploadedFile("slides.pdf", file_bytes, content_type="application/pdf")
    create_resp = auth(api_client, teacher).post(
        f"/api/courses/{c.id}/lectures/",
        {"topic": "L1", "presentation": uploaded},
        format="multipart",
    )
    assert create_resp.status_code in (status.HTTP_201_CREATED, status.HTTP_200_OK)
    # Some implementations may not return the object; fetch from list
    list_after_create = auth(api_client, teacher).get(f"/api/courses/{c.id}/lectures/?page=1&page_size=10")
    assert list_after_create.status_code == status.HTTP_200_OK
    assert list_after_create.data["count"] >= 1
    lecture_id = list_after_create.data["results"][0]["id"]

    # List lectures
    list_resp = auth(api_client, teacher).get(f"/api/courses/{c.id}/lectures/?page=1&page_size=10")
    assert list_resp.status_code == status.HTTP_200_OK
    assert list_resp.data["count"] >= 1

    # Patch lecture topic
    patch_resp = auth(api_client, teacher).patch(
        f"/api/courses/{c.id}/lectures/{lecture_id}/",
        {"topic": "L1-updated"},
        format="json",
    )
    assert patch_resp.status_code == status.HTTP_200_OK
    assert patch_resp.data["topic"] == "L1-updated"

    # Delete lecture
    del_resp = auth(api_client, teacher).delete(f"/api/courses/{c.id}/lectures/{lecture_id}/")
    assert del_resp.status_code == status.HTTP_204_NO_CONTENT


