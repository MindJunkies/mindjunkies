import pytest
from django.urls import reverse
from model_bakery import baker

from mindjunkies.accounts.models import User
from mindjunkies.courses.models import Course, CourseTeacher
from mindjunkies.live_classes.models import LiveClass


# Fixture for creating a user
@pytest.fixture
def user():
    return baker.make(User)


# Fixture for creating a course with a teacher using CourseTeacher
@pytest.fixture
def course(user):
    course = baker.make(Course)
    # Create a CourseTeacher instance linking the user as a teacher to the course
    CourseTeacher.objects.create(course=course, teacher=user)
    return course


# Fixture for creating a live class associated with a course and a teacher
@pytest.fixture
def live_class(course, user):
    return baker.make(LiveClass, course=course, teacher=user)


# Fixture for creating a live class with a specific scheduled time
@pytest.fixture
def live_class_with_scheduled_time(course, user):
    return baker.make(
        LiveClass, course=course, teacher=user, scheduled_at="2025-03-22 10:00:00"
    )


@pytest.mark.django_db
def test_live_class_list_view(client, user, course, live_class):
    # Login the user
    client.force_login(user)

    # Make a request to the LiveClassListView
    url = reverse("list_live_classes", kwargs={"slug": course.slug})
    response = client.get(url)

    # Assert the response is successful
    assert response.status_code == 200
    assert "live_classes" in response.context
    assert live_class in response.context["live_classes"]
    assert response.context["course"] == course
    assert response.context["teacher"] is True


@pytest.mark.django_db
def test_live_class_list_view_no_classes(client, user, course):
    # Login the user
    client.force_login(user)

    # Make a request to the LiveClassListView
    url = reverse("list_live_classes", kwargs={"slug": course.slug})
    response = client.get(url)

    # Assert the response is successful and no live classes are listed
    assert response.status_code == 200
    assert "live_classes" in response.context
    assert len(response.context["live_classes"]) == 0


@pytest.mark.django_db
def test_create_live_class_view(client, user, course):
    # Login the user
    client.force_login(user)

    # Make a request to the CreateLiveClassView
    url = reverse("create_live_class", kwargs={"slug": course.slug})
    response = client.get(url)

    # Assert the response is successful
    assert response.status_code == 200

    # Submit a valid form to create a live class
    data = {
        "topic": "Test Topic",
        "scheduled_at": "2025-03-22 10:00:00",
        "duration": 60,
    }
    response = client.post(url, data)

    # Assert the live class was created and redirect happened
    assert response.status_code == 302  # Redirection after form submission
    assert LiveClass.objects.count() == 1
    assert LiveClass.objects.first().topic == "Test Topic"


@pytest.mark.django_db
def test_join_live_class_view(client, user, live_class):
    # Login the user
    client.force_login(user)

    # Make a request to the JoinLiveClassView
    url = reverse("join_live_class", kwargs={"meeting_id": live_class.meeting_id})
    response = client.get(url)

    # Assert the response is successful and live class is passed to the context
    assert response.status_code == 200
    assert "live_class" in response.context
    assert response.context["live_class"] == live_class
