from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import CreateView, FormView, UpdateView

from .forms import CourseForm, CourseTokenForm, RatingForm
from .models import Course, CourseCategory, CourseToken, Enrollment, LastVisitedCourse, Rating


@require_http_methods(["GET"])
def course_list(request: HttpRequest) -> HttpResponse:
    """View to show all courses."""
    courses = Course.objects.all()
    enrolled_classes = []
    teacher_classes = []
    role = None
    if request.user.is_authenticated:
        enrolled = Enrollment.objects.filter(student=request.user)
        enrolled_classes = [ec.course for ec in enrolled]

    print(teacher_classes)

    context = {
        "courses": courses,
        "enrolled_classes": enrolled_classes,
        "teacher_classes": teacher_classes,
        "role": role,
    }
    return render(request, "courses/course_list.html", context)


class CreateCourseView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/create_course.html"

    def get(self, request):
        if CourseToken.objects.filter(user=request.user, status="pending").exists():
            messages.error(
                request,
                "You have a pending course token. Please wait for it to be approved.",
            )
            return redirect(reverse("dashboard"))
        else:
            return super().get(request)

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        form.save()
        messages.success(self.request, "Course saved successfully!")
        return redirect(reverse("create_course_token"))

    def form_invalid(self, form):
        messages.error(
            self.request, f"There was an error processing the form: {form.errors}"
        )
        return self.render_to_response(self.get_context_data(form=form))


class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/create_course.html"
    context_object_name = "course"

    def get_object(self, queryset=None):
        slug = self.request.GET.get("slug")
        return get_object_or_404(Course, slug=slug) if slug else None

    def form_valid(self, form):
        messages.success(self.request, "Course saved successfully!")
        return redirect(reverse("course_details", kwargs={"slug": form.instance.slug}))

    def form_invalid(self, form):
        print("Form errors:", form.errors)  # Log the errors to the console
        messages.error(
            self.request, f"There was an error processing the form: {form.errors}"
        )
        return self.render_to_response(self.get_context_data(form=form))


@require_http_methods(["GET"])
def course_details(request: HttpRequest, slug: str) -> HttpResponse:
    """View to show course details."""
    course = get_object_or_404(Course, slug=slug)
    enrolled = course.enrollments.filter(student=request.user, status="active").exists()
    context = {
        "course_detail": course,
        "accessed": enrolled,
    }
    return render(request, "courses/course_details.html", context)


@login_required
@require_http_methods(["GET"])
def user_course_list(request: HttpRequest) -> HttpResponse:
    courses = (
        Course.objects.filter(enrollments__student=request.user)
        .annotate(
            last_visited_at=models.Subquery(
                LastVisitedCourse.objects.filter(
                    user=request.user, course=models.OuterRef("pk")
                ).values("last_visited")[:1]
            )
        )
        .order_by("-last_visited_at", "title")
    )  # Order by last visited time, then alphabetically

    return render(request, "courses/course_list.html", {"courses": courses})


@require_http_methods(["GET"])
def category_courses(request, slug):
    category = get_object_or_404(CourseCategory, slug=slug)
    sub_categories = category.get_descendants(include_self=True)
    courses = Course.objects.filter(category__in=sub_categories)
    return render(
        request,
        "courses/category_courses.html",
        {"category": category, "courses": courses},
    )


class CreateCourseTokenView(LoginRequiredMixin, FormView):
    template_name = "course_token_form.html"
    form_class = CourseTokenForm

    def form_valid(self, form):
        token = form.save(commit=False)
        token.user = self.request.user  # Automatically assign logged-in user
        token.save()
        messages.success(self.request, "Course token created successfully!")
        return redirect(reverse("home"))  # Redirect to a success page

    def form_invalid(self, form):
        messages.error(self.request, "There was an error processing the form.")
        return self.render_to_response(self.get_context_data(form=form))


class RatingCreateView(CreateView):
    model = Rating
    form_class = RatingForm
    template_name = "courses/rate_course.html"

    def get_initial(self):
        initial = super().get_initial()
        course = get_object_or_404(Course, slug=self.kwargs["course_slug"])
        try:
            rating = Rating.objects.get(student=self.request.user, course=course)
            initial.update({
                "rating": rating.rating,
                "review": rating.review,
            })
        except Rating.DoesNotExist:
            pass
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = get_object_or_404(Course, slug=self.kwargs["course_slug"])
        return context

    def form_valid(self, form):
        course = get_object_or_404(Course, slug=self.kwargs["course_slug"])
        student = self.request.user

        rating, created = Rating.objects.update_or_create(
            student=student,
            course=course,
            defaults={
                "rating": form.cleaned_data["rating"],
                "review": form.cleaned_data["review"],
            },
        )

        course.update_rating()

        return redirect(reverse("course_details", kwargs={"slug": course.slug}))
