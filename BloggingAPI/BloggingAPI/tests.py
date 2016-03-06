import uuid, json
from django.utils import timezone
from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Author, Friend, Post, Comment
from rest_framework import status
from rest_framework.test import  APITestCase, APIClient

def getObject(request, id):
    obj = MyModel.objects.get(pk=id)
    data = serializers.serialize('json', [obj,])
    struct = json.loads(data)
    data = json.dumps(struct[0])
    return HttpResponse(data, mimetype='application/json')


class restTest(APITestCase):

    def setUp(self):
        self.testUser = User.objects.create_user(username='test', email='test@test.com', password='top_secret')
        self.authID = uuid.uuid4()
        self.authObj = Author.objects.create(user = self.testUser, id = self.authID,host='hostname',url='www.example.com',github= 'www.github.com',bio='test bio')

        self.client = APIClient()
        now = str(datetime.now())
        self.data = {"title":"post","source":"src","origin":"origin","description":"neat","categories":["cool"],"published":now,"author":self.authID}

    def testPost(self):
        self.client.force_authenticate(user = self.testUser)

        postUrl = '/posts/'
        postResponse = self.client.post(postUrl,self.data,format='json')
     
        self.assertEqual(postResponse.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'post')

        postID = Post.objects.get().id

        # Test that we can get what we just Posted
        getUrl = '/posts/' + str(postID) + '/'
        getResponse = self.client.get(getUrl)
        self.assertEqual(getResponse.status_code,status.HTTP_200_OK)

        # Test PUT to posted entity -- should overwrite        
        self.data["title"] = "new title"
        self.data["description"] = "not neat!"

        putResponse = self.client.put(getUrl,self.data,format='json')
        self.assertEqual(putResponse.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1) # ensure nothing new was made

        # ensure the changes are reflected
        self.assertEqual(Post.objects.get().title, 'new title')
        self.assertEqual(Post.objects.get().source, 'src')
        self.assertEqual(Post.objects.get().description, 'not neat!')


        
        #----We currently don't allow posting to created entities
        # updatePostResponse = self.client.post(getUrl,self.data,format='json')
        # print updatePostResponse.data
        # # and test again
        # self.assertEqual(updatePostResponse.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Post.objects.count(), 1)
        # self.assertEqual(Post.objects.get().title, 'post')
        

        
        


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
        self.commentID1 = uuid.uuid4()
        self.commentID2 = uuid.uuid4()
        self.authorID = uuid.uuid4()

        self.testUser = User.objects.create_user(username='author', email='author@test.com', password='top_secret!!')
        self.testAuthor = Author.objects.create(user = self.testUser, id = self.authorID,host='hostname',url='www.example.com',github= 'www.github.com',bio='test bio')

        Comment.objects.create(id = self.commentID1, author = self.testAuthor, contentType = 'text/plain', comment = 'nice comment!')
        Comment.objects.create(id = self.commentID2, author = self.testAuthor, contentType = 'text/markdown', comment = '###nice comment!###')
        
    def test_comment_attributes(self):
        test_plainText = Comment.objects.get(id = self.commentID1)
        test_markdown =  Comment.objects.get(id = self.commentID2)

        self.assertEqual(test_plainText.id, self.commentID1)
        self.assertEqual(test_plainText.author, self.testAuthor)
        self.assertEqual(test_plainText.contentType, 'text/plain')
        self.assertEqual(test_plainText.comment, 'nice comment!')
        
        self.assertEqual(test_markdown.contentType, 'text/markdown')


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

        self.sampleDesc = "Post about my day"
        self.date = datetime.now()
        

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
                            description = self.sampleDesc,contentType = "text/plain", title = "myday", 
                            content = "I had a good day",date_created = self.date, categories = "DayPosts",
                            visibility = visibility_choices[0][0], comments = self.testComment1)

        Post.objects.create(id = id2, author = self.testAuthor, source = "source1", origin = "origin1",
                            description = "Post about my day",contentType = "text/plain", title = "myday", 
                            content = "I had a good day",date_created = self.date, categories = "DayPosts",
                            visibility = visibility_choices[1][1], comments = self.testComment2)

        Post.objects.create(id = id3, author = self.testAuthor, source = "source1", origin = "origin1",
                            description = "Post about my day",contentType = "text/plain", title = "myday", 
                            content = "I had a good day",date_created = self.date, categories = "DayPosts",
                            visibility = visibility_choices[2][2], comments = self.testComment1)

        Post.objects.create(id = id4, author = self.testAuthor, source = "source1", origin = "origin1",
                            description = "Post about my day",contentType = "text/plain", title = "myday", 
                            content = "I had a good day",date_created = self.date, categories = "DayPosts",
                            visibility = visibility_choices[3][3], comments = self.testComment2)

        Post.objects.create(id = id5, author = self.testAuthor, source = "source1", origin = "origin1",
                            description = "Post about my day",contentType = "text/plain", title = "myday", 
                            content = "I had a good day",date_created = self.date, categories = "DayPosts",
                            visibility = visibility_choices[4][4], comments = self.testComment1)

        def test_post_attributes(self):
            test = Post.objects.get(id = self.id1)

            self.assertEqual(test.id,self.id1)
            self.assertEqual(test.author,self.testAuthor)
            self.assertEqual(test.source,"source1")
            self.assertEqual(test.origin,"origin1")
            self.assertEqual(test.description,self.sampleDesc)
            self.assertEqual(test.contentType,"text/plain")
            self.assertEqual(test.title,"myday")
            self.assertEqual(test.content,"I had a good day")
            self.assertEqual(test.date_created,self.date)
            self.assertEqual(test.categories,"DayPosts")
            self.assertEqual(test.visibilities,visibility_choices[0][0])
            self.assertEqual(test.comments,self.testComment1)
            

        #Will have more to test here soon

        def test_Public(self):
            test = Post.objects.get(id = self.id1)
            self.assertEqual(test.visibilities,visibility_choice[0][0])

        def test_FOAF(self):
            test = Post.objects.get(id = self.id2)
            self.assertEqual(test.visibilities,visibility_choice[1][1])

        
        def test_Friends(self):
            test = Post.objects.get(id = self.id3)
            self.assertEqual(test.visibilities,visibility_choice[2][2])
            

            
        def test_Private(self):
            test = Post.objects.get(id = self.id4)
            self.assertEqual(test.visibilities,visibility_choice[3][3])

            
        def test_Server_Only(self):
            test = Post.objects.get(id = self.id5)
            self.assertEqual(test.visibilities,visibility_choice[4][4])
            
          

  


            
