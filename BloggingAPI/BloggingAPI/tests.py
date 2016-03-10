import uuid, json
from django.utils import timezone
from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Author, Friend, Post, Comment
from rest_framework import status
from rest_framework.test import  APITestCase, APIClient

class apiTestPosts(APITestCase):

    def setUp(self):
        self.testUser = User.objects.create_user(username='test', email='test@test.com', password='top_secret')
        self.authID = uuid.uuid4()
        self.authObj = Author.objects.create(user = self.testUser, id = self.authID,host='hostname',url='www.example.com',github= 'www.github.com',bio='test bio')

        self.client = APIClient()

    def test_post_and_put(self):
        now = str(datetime.now())
        data = {"title":"post","source":"src","origin":"origin","description":"neat","categories":["cool"],"published":now,"author":self.authID}

        self.client.force_authenticate(user = self.testUser)
        postUrl = '/api/posts/'

        # Post data
        postResponse = self.client.post(postUrl,data,format='json')
     
        self.assertEqual(postResponse.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'post')

        postID = Post.objects.get().id

        # Test that we can get what we just Posted
        getUrl = '/api/posts/' + str(postID) + '/'
        getResponse = self.client.get(getUrl)
        self.assertEqual(getResponse.status_code,status.HTTP_200_OK)

        # Test PUT to posted entity -- should update        
        data["title"] = "new title"
        data["description"] = "not neat!"

        putResponse = self.client.put(getUrl,data,format='json')
        self.assertEqual(putResponse.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1) # ensure nothing new was made

        # ensure the changes are reflected
        self.assertEqual(Post.objects.get().title, 'new title')
        self.assertEqual(Post.objects.get().source, 'src')
        self.assertEqual(Post.objects.get().description, 'not neat!')

    def testGet(self):
        
        # Test that a get from nothing returns a 404
        randID = str(uuid.uuid4())
        getUrl = '/api/posts/' + randID + '/'
        
        response = self.client.get(getUrl)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Get without a postfixed postID
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO check body contents, post, then run the same tests
        # I.E ensure it can get multiple posts
        

class apiTestFriends(APITestCase):

    def setUp(self):
        self.testUser = User.objects.create_user(username='test', email='test@test.com', password='top_secret')
        self.authID = uuid.uuid4()
        self.authObj = Author.objects.create(user = self.testUser, id = self.authID,host='hostname',url='www.example.com',github= 'www.github.com',bio='test bio')

        self.client = APIClient()

    def testVisibility(self):
        # have an author object in self.authObj
        # and a user object in  self.testUser
        
        # create two authors for the authorObj, one is a friend one isn't
        fID = uuid.uuid4()
        eID = uuid.uuid4()
        friendID1 = uuid.uuid4()
        friendID2 = uuid.uuid4()

        url1 = "http://127.0.0.1:8000/api/authors/" + str(fID) + '/'
        url2 = "http://127.0.0.1:8000/api/authors/" + str(eID) + '/'
        
        
        self.friendUser = User.objects.create_user(username='friend', email='friend@test.com', password='top_secretf')
        self.testAuthor = Author.objects.create(user = self.friendUser, id = fID,host='hostname',url='www.friend.com',github= 'www.github.com',bio='friend bio')

        self.enemyUser = User.objects.create_user(username='enemy', email='enemy@test.com', password='top_secrete')
        self.testAuthor = Author.objects.create(user = self.enemyUser, id = eID,host='hostname',url='www.enemy.com',github= 'www.github.com',bio='friend bio')

        self.friend1 = Friend.objects.create(id = friendID1,author_id = fID,host = "local",display_name = "friend",url = url1)
        self.friend2 = Friend.objects.create(id = friendID2,author_id = eID,host = "local",display_name = "friend",url = url2)

        self.authObj.friends.add(self.friend1)

        # SO querying with friend id 1, logged in as authObj shows friends of friend id1?

        # a reponse if friends or not
        # ask a service http://service/friends/<authorid>

        #responds with:
            #{
             #   "query":"friends",
                # Array of Author UUIDs
              #  "authors":[
               #     "de305d54-75b4-431b-adb2-eb6b9e546013",
                #    "ae345d54-75b4-431b-adb2-fb6b9e547891"
                #],
                # boolean true or false
                #"friends": true
                #}


        getUrl = 'http://127.0.0.1:8000/friends/' + str(self.authID) + '/'
        response = self.client.get(getUrl)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
        url = '127.0.0.1:8000/api/friends/' # this needs to be changed to the openshift URL
        self.id1 = uuid.uuid4()
        self.id2 = uuid.uuid4()
        
        self.friendUser1 = User.objects.create_user(username='friend1', email='friend1@test.com', password='top_secret1')
        self.Author1 = Author.objects.create(user = self.friendUser1, id = self.id1, host='hostname', 
                                             url='http://127.0.0.1:8000/api/friends/.com', github= 'www.github.com',bio='test bio')

        self.friendUser2 = User.objects.create_user(username='friend2', email='friend2@test.com', password='top_secret2')
        self.Author2 = Author.objects.create(user = self.friendUser2, id = self.id2, host='hostname', 
                                             url='www.example.com', github= 'www.github.com',bio='test bio')

        # each friend object will point to the other author (1->2 , 2->1)
        self.friendID = uuid.uuid4()
        Friend.objects.create(id = self.friendID, author_id = self.id1, host = "host", display_name = "Loose Lips Tony", url = "http://127.0.0.1:8000")
        

    def test_friend_attributes(self):
        """Test the friend atttributes"""

        test = Friend.objects.get(id=self.friendID)
        dispName = u"Loose Lips Tony"

        self.assertEqual(test.id,self.friendID)
        self.assertEqual(test.host,"host")
        self.assertEqual(test.display_name,dispName)
        self.assertEqual(test.url,"http://127.0.0.1:8000")
        self.assertEqual(test.author_id,self.id1)


class commentTestCase(TestCase):

    def setUp(self):
        self.commentID1 = uuid.uuid4()
        self.commentID2 = uuid.uuid4()
        self.postID = uuid.uuid4()
        self.authorID = uuid.uuid4()
        self.date = timezone.now()

        self.testUser = User.objects.create_user(username='author', email='author@test.com', password='top_secret!!')
        self.testAuthor = Author.objects.create(user = self.testUser, id = self.authorID,host='hostname',url='www.example.com',github= 'www.github.com',bio='test bio')

        self.testPost = Post.objects.create(id = self.postID, author = self.testAuthor, source = "source1", origin = "origin1",
                            description = "",contentType = "text/plain", title = "myday", 
                            content = "I had a good day",date_created = self.date, categories = ["Day Posts"],
                            visibility = 'PUBLIC')

        Comment.objects.create(id = self.commentID1, post = self.testPost, author = self.testAuthor, contentType = 'text/plain', comment = 'nice comment!')
        Comment.objects.create(id = self.commentID2, post = self.testPost, author = self.testAuthor, contentType = 'text/markdown', comment = '###nice comment!###')
        
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
                            content = "I had a good day",date_created = self.date, categories = ["DayPosts"],
                            visibility = visibility_choices[0][0], comments = self.testComment1)

        Post.objects.create(id = id2, author = self.testAuthor, source = "source1", origin = "origin1",
                            description = "Post about my day",contentType = "text/plain", title = "myday", 
                            content = "I had a good day",date_created = self.date, categories = ["DayPosts"],
                            visibility = visibility_choices[1][1], comments = self.testComment2)

        Post.objects.create(id = id3, author = self.testAuthor, source = "source1", origin = "origin1",
                            description = "Post about my day",contentType = "text/plain", title = "myday", 
                            content = "I had a good day",date_created = self.date, categories = ["DayPosts"],
                            visibility = visibility_choices[2][2], comments = self.testComment1)

        Post.objects.create(id = id4, author = self.testAuthor, source = "source1", origin = "origin1",
                            description = "Post about my day",contentType = "text/plain", title = "myday", 
                            content = "I had a good day",date_created = self.date, categories = ["DayPosts"],
                            visibility = visibility_choices[3][3], comments = self.testComment2)

        Post.objects.create(id = id5, author = self.testAuthor, source = "source1", origin = "origin1",
                            description = "Post about my day",contentType = "text/plain", title = "myday", 
                            content = "I had a good day",date_created = self.date, categories = ["DayPosts"],
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
            
          

  


            
