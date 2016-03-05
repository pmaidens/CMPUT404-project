import uuid, datetime
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Author, Friend, Post, Comment


class AuthorTestCase(TestCase):

    def setUp(self):
        self.id1 = uuid.uuid4()
        self.testUser = User.objects.create_user(username='test', email='test@test.com', password='top_secret')
        self.authObj = Author.objects.create(user = self.testUser, id = self.id1,host='hostname',url='www.example.com',github= 'www.github.com',bio='test bio')

    def test_author_attribues(self):
        """Ensure correct storage and usage of database"""
        test = Author.objects.get(id=self.id1)

        self.assertEqual(test.user.username,'test')
        self.assertEqual(test.user.email,'test@test.com')

        self.assertEqual(test.user, self.testUser)
        self.assertEqual(test.url, 'www.example.com')
        self.assertEqual(test.github, 'www.github.com')
        self.assertEqual(test.bio, 'test bio')


    def test_create_functionality(self):
        """test the get_or_create functionality of the author model"""
        result = Author.create_user_profile(self.authObj,self.authObj.user,True)
        self.assertEqual(result,None)

class friendTestCase(TestCase):

    def setUp(self):

        self.friendID = uuid.uuid4()
        Friend.objects.create(id = self.friendID, host = "host", display_name = "Loose Lips Tony", url = "http://127.0.0.1:8000")

    def test_friend_attributes(self):
        """Test the friend atttributes"""

        test = Friend.objects.get(id=self.friendID)
        dispName = u"Loose Lips Tony"

        self.assertEqual(test.id,self.friendID)
        self.assertEqual(test.host,"host")
        self.assertEqual(test.display_name,dispName)
        self.assertEqual(test.url,"http://127.0.0.1:8000")


class commentTestCase(TestCase):

    def setUp(self):
        self.commentID = uuid.uuid4()
        self.authorID = uuid.uuid4()

        self.testUser = User.objects.create_user(username='author', email='author@test.com', password='top_secret!!')
        self.testAuthor = Author.objects.create(user = self.testUser, id = self.authorID,host='hostname',url='www.example.com',github= 'www.github.com',bio='test bio')

        Comment.objects.create(id = self.commentID, author = self.testAuthor, contentType = 'text/plain', comment = 'nice comment!')
        
    def test_comment_attributes(self):
        test = Comment.objects.get(id = self.commentID)

        self.assertEqual(test.id, self.commentID)
        self.assertEqual(test.author, self.testAuthor)
        self.assertEqual(test.contentType, 'text/plain')
        self.assertEqual(test.comment, 'nice comment!')


class PostTestCase(TestCase):

    def setUp(self):
        self.authorID = uuid.uuid4()
        self.commentAuthorID = uuid.uuid4()

        self.commentID1 = uuid.uuid4()
        self.commentID2 = uuid.uuid4()

        self.id1 = uuid.uuid4()
        self.id2 = uuid.uuid4()
        self.id3 = uuid.uuid4()
        self.id4 = uuid.uuid4()
        self.id5 = uuid.uuid4()

        visibility_choices = (
            ('PUBLIC', 'PUBLIC'),
            ('FOAF', 'FOAF'),
            ('FRIENDS', 'FRIENDS'),
            ('PRIVATE', 'PRIVATE'),
            ('SERVERONLY', 'SERVERONLY'),
        )

        self.testUser = User.objects.create_user(username='author', email='author@test.com', password='top_secret!')
        self.testAuthor = Author.objects.create(user = self.testUser, id = self.authorID,host='hostname',url='www.example.com',github= 'www.github.com',bio='test bio')

        self.commentUser = User.objects.create_user(username='comment', email='comment@test.com', password='comment!')
        self.commentAuthor = Author.objects.create(user = self.commentUser, id = self.commentAuthorID,host='hostname',url='www.example.com',github= 'www.github.com',bio='test bio')


        self.testComment1 = Comment.objects.create(id = commentID1, author = self.testAuthor, contentType = 'text/plain', comment = 'nice comment!')
        self.testComment2 = Comment.objects.create(id = commentID2, author = self.commentAuthor, contentType = 'text/plain', comment = 'I like this!')

        Post.objects.create(id = id1, author = self.testAuthor, source = "source1", origin = "origin1",
                            description = "Post about my day",contentType = "text/plain", title = "myday", 
                            content = "I had a good day",date_created = datetime.now(), categories = "DayPosts",
                            visibility = visibility_choices[0][0], comments = self.testComment1)
