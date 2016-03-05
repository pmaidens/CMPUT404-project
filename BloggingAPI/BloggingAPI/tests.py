import uuid
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Author

class AuthorTestCase(TestCase):
    def setUp(self):
        self.id1 = uuid.uuid4()
        self.testUser = User.objects.create_user(username='test', email='test@test.com', password='top_secret')

        Author.objects.create(user = self.testUser, id = self.id1,host='hostname',url='www.example.com',github= 'www.github.com',bio='test bio')

    def test_author_attribues(self):
        """Ensure correct storage and usage of database"""
        test = Author.objects.get(id=self.id1)

        self.assertEqual(test.user.username,'test')
        self.assertEqual(test.user.email,'test@test.com')

        self.assertEqual(test.user, self.testUser)
        self.assertEqual(test.url, 'www.example.com')
        self.assertEqual(test.github, 'www.github.com')
        self.assertEqual(test.bio, 'test bio')

    
