from django.contrib.auth import get_user_model
from django.test import TestCase

### May want to break this test file up by test focus ie test_models.py, test_forms.py, test_views.py it becomes very large.)

# test_models.py
# Create your tests here.
class CustomUserTests(TestCase):

        def test_create_user(self):
            User = get_user_model()
            user = User.objects.create_user(
                username='testjonathan',
                email='test.jonathan@gu.se',
                password='testpass3333'
                )
            self.assertEqual(user.username, 'testjonathan')
            self.assertEqual(user.email, 'test.jonathan@gu.se')
            self.assertTrue(user.is_active)
            self.assertFalse(user.is_staff)
            self.assertFalse(user.is_superuser)

        def test_create_superuser ( self ):
            User = get_user_model ()
            admin_user = User.objects.create_superuser(
                username = 'testsuperadmin',
                email = 'testsuperadmin@gu.se',
                password = 'testpass423'
                )
            self.assertEqual(admin_user.username, 'testsuperadmin')
            self.assertEqual(admin_user.email, 'testsuperadmin@gu.se')
            self.assertTrue(admin_user.is_active)
            self.assertTrue(admin_user.is_staff)
            self.assertTrue(admin_user.is_superuser)

# test_forms.py
# Create your tests here.


# test_views.py
# Create your tests here.
