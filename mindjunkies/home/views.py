from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_http_methods

from mindjunkies.courses.models import Course, CourseCategory, CourseTeacher, Enrollment


@require_http_methods(["GET"])
def home(request):
    featured_course = Course.objects.all()
    course_categories = CourseCategory.objects.filter(parent__isnull=True)
    context = {
        "course_list": featured_course,
        "categories": course_categories,
    }
    enrolled_classes = []
    teacher_classes = []
    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(student=request.user, status="active")
        enrolled_classes = [ec.course for ec in enrolled]
        teaching = CourseTeacher.objects.filter(teacher=request.user)
        teacher_classes = [ec.course for ec in teaching]
        context["enrolled_classes"] = enrolled_classes
        context["teacher_classes"] = teacher_classes

    return render(request, "home/index.html", context)


@require_http_methods(["GET"])
def search_results(request):
    query = request.GET.get("search", "")
    highlighted_courses = []
    if query and query != "":
        courses = Course.objects.filter(title__icontains=query)
        for course in courses:
            highlighted_title = course.title.replace(query, f"<mark>{query}</mark>")
            highlighted_courses.append(
                {"course": course, "highlighted_title": mark_safe(highlighted_title)}
            )
    else:
        highlighted_courses = []
    return render(
        request,
        "home/search_results.html",
        {"courses": highlighted_courses, "query": query},
    )
