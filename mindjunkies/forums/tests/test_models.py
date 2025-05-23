import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django import forms
from django.utils.text import slugify
from django.core.exceptions import ValidationError

from mindjunkies.courses.models import Course, Module, CourseCategory
from mindjunkies.lecture.models import Lecture, LecturePDF, LectureVideo
from mindjunkies.lecture.forms import LectureForm, LecturePDFForm, LectureVideoForm, ModuleForm

User = get_user_model()


@pytest.mark.django_db
class TestLectureForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="teacher",
            password="password",
            email="teacher@example.com",
        )
        self.category = CourseCategory.objects.create(
            name="Test Category",
            slug="test-category",
        )
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_introduction="A short intro",
            course_description="Detailed description",
            teacher=self.user,
            level="beginner",
            category=self.category,
            course_image="course_images/test_image.jpg",  # Mock CloudinaryField
        )
        self.module = Module.objects.create(
            title="Test Module",
            order=1,
            course=self.course,
        )

    
    def test_invalid_form_missing_title(self):
        """Test invalid LectureForm with missing title"""
        data = {
            "description": "Lecture description",
            "learning_objective": "Learn something",
            "order": 1,
        }
        form = LectureForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_invalid_form_negative_order(self):
        """Test invalid LectureForm with negative order"""
        data = {
            "title": "Test Lecture",
            "description": "Lecture description",
            "learning_objective": "Learn something",
            "order": -1,
        }
        form = LectureForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("order", form.errors)

    def test_unique_order_per_module(self):
        """Test unique order per module validation"""
        Lecture.objects.create(
            course=self.course,
            module=self.module,
            title="Existing Lecture",
            slug="existing-lecture",
            order=1,
        )
        data = {
            "title": "Test Lecture",
            "description": "Lecture description",
            "learning_objective": "Learn something",
            "order": 1,  # Conflicts with existing lecture
        }
        form = LectureForm(data=data)
        self.assertTrue(form.is_valid())  # Form validates, but save raises ValidationError
        lecture = form.save(commit=False)
        lecture.course = self.course
        lecture.module = self.module
        with self.assertRaises(ValidationError) as cm:
            lecture.save()
        self.assertIn("Order 1 already exists in this module", str(cm.exception))


@pytest.mark.django_db
class TestLecturePDFForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="teacher",
            password="password",
            email="teacher@example.com",
        )
        self.category = CourseCategory.objects.create(
            name="Test Category",
            slug="test-category",
        )
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_introduction="A short intro",
            course_description="Detailed description",
            teacher=self.user,
            level="beginner",
            category=self.category,
            course_image="course_images/test_image.jpg",
        )
        self.module = Module.objects.create(
            title="Test Module",
            order=1,
            course=self.course,
        )
        self.lecture = Lecture.objects.create(
            course=self.course,
            module=self.module,
            title="Test Lecture",
            slug="test-lecture",
            order=1,
        )

    def test_valid_form(self):
        """Test valid LecturePDFForm data"""
        pdf_content = b"%PDF-1.4 fake PDF content"
        pdf_file = SimpleUploadedFile("test.pdf", pdf_content, content_type="application/pdf")
        data = {"pdf_title": "Test PDF"}
        files = {"pdf_file": pdf_file}
        form = LecturePDFForm(data=data, files=files)
        self.assertTrue(form.is_valid())
        pdf = form.save(commit=False)
        pdf.lecture = self.lecture
        pdf.save()
        self.assertEqual(pdf.pdf_title, "Test PDF")
        self.assertEqual(pdf.lecture, self.lecture)
        self.assertTrue(pdf.pdf_file.name.startswith("lecture_pdfs/test"))

    def test_valid_form_with_lecture(self):
        """Test LecturePDFForm save with lecture parameter"""
        pdf_content = b"%PDF-1.4 fake PDF content"
        pdf_file = SimpleUploadedFile("test.pdf", pdf_content, content_type="application/pdf")
        data = {"pdf_title": "Test PDF"}
        files = {"pdf_file": pdf_file}
        form = LecturePDFForm(data=data, files=files)
        self.assertTrue(form.is_valid())
        pdf = form.save(lecture=self.lecture)
        self.assertEqual(pdf.pdf_title, "Test PDF")
        self.assertEqual(pdf.lecture, self.lecture)
        self.assertTrue(pdf.pdf_file.name.startswith("lecture_pdfs/test"))

    def test_invalid_pdf_extension(self):
        """Test invalid PDF extension"""
        txt_file = SimpleUploadedFile("test.txt", b"Text content", content_type="text/plain")
        data = {"pdf_title": "Test PDF"}
        files = {"pdf_file": txt_file}
        form = LecturePDFForm(data=data, files=files)
        self.assertFalse(form.is_valid())
        self.assertIn("pdf_file", form.errors)
        self.assertEqual(form.errors["pdf_file"], ["Only PDF files are allowed."])

    def test_invalid_pdf_size(self):
        """Test oversized PDF file"""
        large_content = b"%PDF-1.4 " + b"0" * (6 * 1024 * 1024)  # 6MB
        pdf_file = SimpleUploadedFile("large.pdf", large_content, content_type="application/pdf")
        data = {"pdf_title": "Test PDF"}
        files = {"pdf_file": pdf_file}
        form = LecturePDFForm(data=data, files=files)
        self.assertFalse(form.is_valid())
        self.assertIn("pdf_file", form.errors)
        self.assertEqual(form.errors["pdf_file"], ["File size must be less than 5MB."])

    
@pytest.mark.django_db
class TestLectureVideoForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="teacher",
            password="password",
            email="teacher@example.com",
        )
        self.category = CourseCategory.objects.create(
            name="Test Category",
            slug="test-category",
        )
        self.course = Course.objects.create(
            title="Test Course",
            slug="test-course",
            short_introduction="A short intro",
            course_description="Detailed description",
            teacher=self.user,
            level="beginner",
            category=self.category,
            course_image="course_images/test_image.jpg",
            preview_video="videos/test_preview.mp4",
        )
        self.module = Module.objects.create(
            title="Test Module",
            order=1,
            course=self.course,
        )
        self.lecture = Lecture.objects.create(
            course=self.course,
            module=self.module,
            title="Test Lecture",
            slug="test-lecture",
            order=1,
        )


