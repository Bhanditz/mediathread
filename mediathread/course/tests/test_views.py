import analytics
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from courseaffils.models import Course
from django.test.utils import override_settings
from mock import MagicMock, patch
from mediathread.course.models import CourseInformation

mock_analytics = MagicMock(spec=analytics)


@patch("analytics.identify", mock_analytics)
@patch("analytics.track", mock_analytics)
class CourseCreateTest(TestCase):
    fixtures = ['unittest_sample_course.json', 'registration_data.json', 'user_profiles.json']

    def setUp(self):
        self.client.login(username="test_instructor", password="test")
        self.user = User.objects.get(username="test_instructor")

    def test_create_first_course(self):
        self.user.groups.clear()
        response = self.client.post(reverse("course_create"), {
            'title': "Sample course #1",
            'organization': "Test organization",
            'student_amount': '10',
            'term': 1,
            'year': 2013
        })
        self.assertRedirects(response, '/')
        self.assertTrue(Course.objects.filter(title="Sample course #1").exists())
        course = Course.objects.get(title="Sample course #1")
        self.assertTrue("test_instructor" in course.faculty_group.user_set.values_list('username', flat=True))
        self.assertTrue("test_instructor" in course.user_set.values_list('username', flat=True))
        self.assertEquals(2013, course.info.year)
        self.assertEquals(1, course.info.term)

    def test_missing_form_fields(self):
        self.user.groups.clear()
        response = self.client.post(reverse("course_create"), {
            'title': "",
            'organization': "",
            'student_amount': '10'
        })
        self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertFormError(response, 'form', 'organization', 'This field is required.')

    def test_show_call_to_action_when_no_courses_left(self):
        """
        Show a call to action for upgrading to a bigger plan when they have no courses left
        """
        ci = CourseInformation.objects.create(title="test", organization_name="test_org", student_amount=10)
        ci.add_member(self.user, faculty=True)
        response = self.client.get(reverse("course_create"))
        self.assertContains(response, "You've used your available courses on this plan")
        self.assertContains(response, "<h1>Courses limit reached!</h1>")

    def test_dont_show_call_to_action_when_no_course_is_created(self):
        """
        Don't show a call to action for inviting more students when user has more than 1 invite left
        """
        self.user.groups.clear()
        response = self.client.get(reverse("course_create"))
        self.assertContains(response, "form", status_code=200)
        self.assertNotContains(response, "You've used your available courses on this plan")
        self.assertNotContains(response, "<h1>Courses limit reached!</h1>")


class MemberListTest(TestCase):
    fixtures = ['unittest_sample_course.json', 'registration_data.json', 'user_profiles.json']

    def setUp(self):
        self.client.login(username="test_instructor", password="test")

    def test_list_of_all_class_members(self):
        response = self.client.get(reverse('member_list'))
        self.assertContains(response, '<td>Instructor</td>', count=2, html=True)
        self.assertContains(response, '<td>Student</td>', count=4, html=True)
        self.assertContains(response, 'Resend Invite', count=2)
        self.assertContains(response, 'Promote', count=4)


class PromoteStudentTest(TestCase):
    fixtures = ['unittest_sample_course.json', 'user_profiles.json']

    @patch("analytics.identify", mock_analytics)
    def test_promote_student(self):
        self.client.login(username="test_instructor", password="test")
        user = User.objects.get(id=3)
        course = Course.objects.get(id=1)
        self.assertFalse(user in course.faculty_group.user_set.all())
        response = self.client.post(reverse("promote_student"), {
            'user_id': 3
        }, follow=True)
        self.assertTrue(user in course.faculty_group.user_set.all())
        self.assertRedirects(response, reverse('member_list'))
        self.assertContains(response, "Successfully promoted")

    def test_promote_student_without_permissions(self):
        self.client.login(username="test_student_two", password="test")
        user = User.objects.get(id=3)
        course = Course.objects.get(id=1)
        self.assertFalse(user in course.faculty_group.user_set.all())
        response = self.client.post(reverse("promote_student"), {
            'user_id': 3
        }, follow=True)
        self.assertFalse(user in course.faculty_group.user_set.all())
        self.assertRedirects(response, reverse('member_list'))
        self.assertContains(response, "You must be an instructor in this course to do that")


class ResendInviteTest(TestCase):
    fixtures = ['unittest_sample_course.json', 'registration_data.json', 'user_profiles.json']

    def setUp(self):
        self.client.login(username="test_instructor", password="test")

    def test_resend_invite_to_nonactive_user(self):
        response = self.client.post(reverse("resend_invite"), {
            'user_id': 3
        }, follow=True)
        user = User.objects.get(id=3)
        self.assertEqual(len(mail.outbox), 1)
        self.assertRedirects(response, reverse('member_list'))
        self.assertContains(response, "successfully sent the activation email to {0}".format(user.email))

    def test_resend_invite_to_active_user(self):
        response = self.client.post(reverse("resend_invite"), {
            'user_id': 4
        }, follow=True)
        self.assertEqual(len(mail.outbox), 0)
        self.assertRedirects(response, reverse('member_list'))
        self.assertContains(response, "User already activated his account.")


class RemoveStudentTest(TestCase):
    fixtures = ['unittest_sample_course.json', 'registration_data.json', 'user_profiles.json']

    def test_remove_student(self):
        self.client.login(username="test_instructor", password="test")

        course = Course.objects.get(id=1)
        self.assertEquals(course.user_set.count(), 6)
        response = self.client.post(reverse("remove_student"), {
            'user_id': 3
        }, follow=True)
        user = User.objects.get(id=3)
        self.assertFalse(user in course.group.user_set.all())
        self.assertEquals(course.user_set.count(), 5)
        self.assertRedirects(response, reverse('member_list'))
        self.assertContains(response, "Successfully removed {0}".format(user.email))

    def test_remove_student_without_permissions(self):
        self.client.login(username="test_student_one", password="test")
        course = Course.objects.get(id=1)
        self.assertEquals(course.user_set.count(), 6)
        response = self.client.post(reverse("remove_student"), {
            'user_id': 4
        }, follow=True)
        user = User.objects.get(id=4)
        self.assertTrue(user in course.group.user_set.all())
        self.assertEquals(course.user_set.count(), 6)
        self.assertRedirects(response, reverse('member_list'))
        self.assertContains(response, "You must be an instructor in this course to do that")


class DemoteFacultyTest(TestCase):
    fixtures = ['unittest_sample_course.json', 'registration_data.json', 'user_profiles.json']

    def test_demote_faculty(self):
        self.client.login(username="test_instructor", password="test")

        course = Course.objects.get(id=1)
        self.assertEquals(course.faculty_group.user_set.count(), 2)
        response = self.client.post(reverse("demote_faculty"), {
            'user_id': 10
        }, follow=True)
        user = User.objects.get(id=10)
        self.assertFalse(user in course.faculty_group.user_set.all())
        self.assertEquals(course.faculty_group.user_set.count(), 1)
        self.assertRedirects(response, reverse('member_list'))
        self.assertContains(response, "Successfully demoted {0}".format(user.email))

    def test_demote_faculty_without_permissions(self):
        self.client.login(username="test_student_one", password="test")
        course = Course.objects.get(id=1)
        self.assertEquals(course.faculty_group.user_set.count(), 2)
        response = self.client.post(reverse("demote_faculty"), {
            'user_id': 10
        }, follow=True)
        user = User.objects.get(id=10)
        self.assertTrue(user in course.faculty_group.user_set.all())
        self.assertEquals(course.faculty_group.user_set.count(), 2)
        self.assertRedirects(response, reverse('member_list'))
        self.assertContains(response, "You must be an instructor in this course to do that")


class NoCoursesTest(TestCase):
    fixtures = ['unittest_sample_course.json', 'user_profiles.json']

    def setUp(self):
        self.user = User.objects.create_user(username="test_test", email="test@something.com", password="test")
        self.client.login(username="test_test", password="test")

    def test_new_user_sees_choice_screen(self):
        """
        New user should see the choice screen where they can choose between creating
        their own course or joining the sample one.
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'courseaffils/no_courses.html')

    @override_settings(SAMPLE_COURSE_ID=1)
    def test_join_sample_course(self):
        """
        New user can join the sample course and be taken to the course homepage
        """
        course = Course.objects.get(id=1)
        response = self.client.get(reverse("join_sample_course"), follow=True)
        self.assertTrue(self.user in course.group.user_set.all())
        self.assertTemplateUsed(response, 'homepage.html')
        self.assertContains(response, 'Sample Course')
