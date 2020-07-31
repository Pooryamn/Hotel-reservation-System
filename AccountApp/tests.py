from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import UserRegistrationForm


class SignupTest(TestCase):
    def setUp(self):
        User.objects.create(username="admin")
        self.url = reverse('AccountApp:register')

    def test_email(self):
        wrong_email = 'admin1gmail.com'

        post1 = {'first_name':'test',
                'last_name':'test',
                'email':wrong_email,
                'username':'test',
                'phone':0,
                'national_id':0,
                'password':'123456789',
                'password2':'123456789'}

        response = self.client.post(self.url, post1)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Enter a valid email address.", html=True)

    def test_username(self):
        username = 'admin'

        post1 = {'first_name':'test',
                'last_name':'test',
                'email':'test@gmail.com',
                'username': username,
                'phone':0,
                'national_id':0,
                'password':'123456789',
                'password2':'123456789'}

        response = self.client.post(self.url, post1)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A user with that username already exists.", html=True)

    def test_password(self):
        password = "12345"
        password2 = "123456789"

        post1 = {'first_name':'test',
                'last_name':'test',
                'email': 'test@gmail.com',
                'username':'test',
                'phone':0,
                'national_id':0,
                'password':password,
                'password2':password2}

        response = self.client.post(self.url, post1)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords do not match !", html=True)

    def test_phone(self):
        phone = 916226546332

        post1 = {'first_name':'test',
                'last_name':'test',
                'email': 'test@gmail.com',
                'username':'test',
                'phone':phone,
                'national_id':0,
                'password':'123456789',
                'password2':'123456789'}

        response = self.client.post(self.url, post1)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 
                "Ensure this value has at most 11 characters (it has 12).", html=True)

    def test_correct_confirm_code(self):
        post1 = {'first_name':'test',
                'last_name':'test',
                'email': 'test@gmail.com',
                'username':'test',
                'phone':0,
                'national_id':0,
                'password':'123456789',
                'password2':'123456789'}

        response1 = self.client.post(self.url, post1)
        self.assertEqual(response1.status_code, 200)

        code = self.client.session['MainPass']

        confirm_url = reverse("AccountApp:Confrim_check")
        response2 = self.client.post(confirm_url, {"Confpass": code})
        self.assertEqual(response2.status_code, 302)

        print(User.objects.all())


    def test_wrong_confirm_code(self):
        post1 = {'first_name':'test',
                'last_name':'test',
                'email': 'test@gmail.com',
                'username':'test',
                'phone':0,
                'national_id':0,
                'password':'123456789',
                'password2':'123456789'}

        response1 = self.client.post(self.url, post1)
        self.assertEqual(response1.status_code, 200)

        code = "5s6K94"

        confirm_url = reverse("AccountApp:Confrim_check")
        response2 = self.client.post(confirm_url, {"Confpass": code})
        self.assertEqual(response2.status_code, 200)

        print(User.objects.all())
        
        self.assertContains(response2, 
                "کد تایید شما نادرست است.", html=True)


        # form = UserRegistrationForm(data=post1)
        # self.assertEqual(
        #     form.errors["phone"], ["Ensure this value has at most 11 characters (it has 12)."]
        # )