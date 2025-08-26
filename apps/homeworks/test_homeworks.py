import pytest
pytestmark = pytest.mark.django_db
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from apps.courses.models import Course, Lecture
from apps.homeworks.models import Homework, HomeworkSubmission, HomeworkGrade
from common.enums import UserRole, ErrorMessages


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


@pytest.fixture
def unenrolled_student(db):
    return User.objects.create_user(
        email="student2@example.com",
        password="pass12345",
        role=UserRole.STUDENT.value,
        first_name="S2",
        last_name="Two",
    )


@pytest.fixture
def course(db, teacher, student, other_teacher):
    c = Course.objects.create(
        name="C1",
        description="Desc",
        primary_owner=teacher,
    )
    c.teachers.add(teacher)
    c.students.add(student)
    return c


@pytest.fixture
def lecture(db, course):
    return Lecture.objects.create(course=course, topic="L1", presentation="p.pdf")


@pytest.fixture
def homework(db, lecture, teacher):
    return Homework.objects.create(
        lecture=lecture,
        title="HW1",
        description="D",
        due_date="2030-01-01T00:00:00Z",
        created_by=teacher,
    )


@pytest.fixture
def submission(db, homework, student):
    return HomeworkSubmission.objects.create(homework=homework, student=student, content="Ans")


def auth(client: APIClient, user: User):
    client.force_authenticate(user)
    return client


def grades_list_url(course_id, lecture_id, homework_id, submission_id):
    return f"/api/courses/{course_id}/lectures/{lecture_id}/homeworks/{homework_id}/submissions/{submission_id}/grades/"


def grade_comments_url(course_id, lecture_id, homework_id, submission_id, grade_id):
    return f"/api/courses/{course_id}/lectures/{lecture_id}/homeworks/{homework_id}/submissions/{submission_id}/grades/{grade_id}/comments/"


def test_unenrolled_student_cannot_list_grades(api_client, unenrolled_student, submission):
    url = grades_list_url(
        submission.homework.lecture.course_id,
        submission.homework.lecture_id,
        submission.homework_id,
        submission.id,
    )
    resp = auth(api_client, unenrolled_student).get(url)
    assert resp.status_code == status.HTTP_403_FORBIDDEN


def test_teacher_can_create_and_list_grade(api_client, teacher, submission):
    list_url = grades_list_url(
        submission.homework.lecture.course_id,
        submission.homework.lecture_id,
        submission.homework_id,
        submission.id,
    )
    create_resp = auth(api_client, teacher).post(list_url, {"grade": 90, "comments": "Nice"}, format="json")
    assert create_resp.status_code in (status.HTTP_201_CREATED, status.HTTP_200_OK)

    list_resp = auth(api_client, teacher).get(list_url)
    assert list_resp.status_code == status.HTTP_200_OK
    assert list_resp.data["count"] == 1


def test_student_owner_can_view_own_grades(api_client, teacher, student, submission):
    # teacher creates grade
    url = grades_list_url(
        submission.homework.lecture.course_id,
        submission.homework.lecture_id,
        submission.homework_id,
        submission.id,
    )
    auth(api_client, teacher).post(url, {"grade": 88, "comments": "Good"}, format="json")

    # owner student can view
    list_resp = auth(api_client, student).get(url)
    assert list_resp.status_code == status.HTTP_200_OK
    assert list_resp.data["count"] == 1


def test_student_cannot_create_grade(api_client, student, submission):
    url = grades_list_url(
        submission.homework.lecture.course_id,
        submission.homework.lecture_id,
        submission.homework_id,
        submission.id,
    )
    resp = auth(api_client, student).post(url, {"grade": 77, "comments": "self"}, format="json")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert ErrorMessages.ONLY_TEACHERS_CAN_GRADE.value in str(resp.data)


def test_unenrolled_student_cannot_create_submission(api_client, unenrolled_student, homework):
    url = f"/api/courses/{homework.lecture.course_id}/lectures/{homework.lecture_id}/homeworks/{homework.id}/submissions/"
    resp = auth(api_client, unenrolled_student).post(url, {"content": "Ans"}, format="json")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert ErrorMessages.STUDENT_NOT_ENROLLED.value in str(resp.data)


# Lecture PATCH tests
def test_teacher_can_patch_lecture_topic(api_client, teacher, lecture):
    url = f"/api/courses/{lecture.course_id}/lectures/{lecture.id}/"
    resp = auth(api_client, teacher).patch(url, {"topic": "Updated Topic"}, format="json")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["topic"] == "Updated Topic"


def test_student_cannot_patch_lecture(api_client, student, lecture):
    url = f"/api/courses/{lecture.course_id}/lectures/{lecture.id}/"
    resp = auth(api_client, student).patch(url, {"topic": "Hack"}, format="json")
    assert resp.status_code == status.HTTP_403_FORBIDDEN


def test_empty_topic_validation_on_patch(api_client, teacher, lecture):
    url = f"/api/courses/{lecture.course_id}/lectures/{lecture.id}/"
    resp = auth(api_client, teacher).patch(url, {"topic": "   "}, format="json")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST


# Submission PATCH tests
def test_student_can_patch_own_submission_content(api_client, student, submission):
    url = f"/api/courses/{submission.homework.lecture.course_id}/lectures/{submission.homework.lecture_id}/homeworks/{submission.homework_id}/submissions/{submission.id}/"
    resp = auth(api_client, student).patch(url, {"content": "New content"}, format="json")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.data["content"] == "New content"


def test_other_student_cannot_patch_submission(api_client, unenrolled_student, submission):
    url = f"/api/courses/{submission.homework.lecture.course_id}/lectures/{submission.homework.lecture_id}/homeworks/{submission.homework_id}/submissions/{submission.id}/"
    resp = auth(api_client, unenrolled_student).patch(url, {"content": "steal"}, format="json")
    assert resp.status_code == status.HTTP_404_NOT_FOUND


def test_empty_content_validation_on_submission_patch(api_client, student, submission):
    url = f"/api/courses/{submission.homework.lecture.course_id}/lectures/{submission.homework.lecture_id}/homeworks/{submission.homework_id}/submissions/{submission.id}/"
    resp = auth(api_client, student).patch(url, {"content": "   "}, format="json")
    assert resp.status_code == status.HTTP_400_BAD_REQUEST

# Create your tests here.
