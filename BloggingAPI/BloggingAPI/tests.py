import uuid,json
from django.utils import timezone
from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Author, Friend, Post, Comment
from rest_framework import status
from rest_framework.test import  APITestCase, APIClient
from django.test.client import Client

class apiTests(TestCase):
    
    def setUp(self):
        authorUser = User.objects.create_user('PostAuthor', 'post@post.com','post secret')
        self.aID = uuid.uuid4()
        #Fields:
        # User: authorUser
        # id: b5a66332-ada4-4629-bfe7-90600387d696
        # url: example.com/author/b5a66332-ada4-4629-bfe7-90600387d696
        # host: example.com
        # github: None
        # bio: None
        
        self.author = Author.objects.get(user = authorUser)
#Author.objects.create(user = authorUser, id = self.aID, host = 'postHost', url = url, github = github, bio='bio')

        self.client = APIClient()

    def test_POST_post_and_put(self):
        now = str(datetime.now())
        data = {"title":"post","source":"src",
                "origin":"origin","description":"neat",
                "categories":["cool"],"published":now,
                "author":self.author.id}

        #self.client.force_authenticate(user = self.testUser)
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

        #Put not working?
        
        putResponse = self.client.put(getUrl,data,format='json')
        self.assertEqual(putResponse.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1) # ensure nothing new was made

        # ensure the changes are reflected
        self.assertEqual(Post.objects.get().title, 'new title')
        self.assertEqual(Post.objects.get().source, 'src')
        self.assertEqual(Post.objects.get().description, 'not neat!')
        
        
    def test_PostGet(self):
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

    def test_Friend(self):

        # have an author object in self.author
        # and a user object in  self.author.user
        
        # create two authors for the authorObj, one is a friend one isn't

        friendID1 = uuid.uuid4()
        friendID2 = uuid.uuid4()
        
        friendUser = User.objects.create_user(username='friend', email='friend@test.com', password='top_secretf')
        self.testFriend = Author.objects.get(user = friendUser)

        enemyUser = User.objects.create_user(username='enemy', email='enemy@test.com', password='top_secrete')
        self.testEnemy = Author.objects.get(user=enemyUser)

        url1 = "http://127.0.0.1:8000/api/authors/" + str(self.testFriend.id) + '/'
        url2 = "http://127.0.0.1:8000/api/authors/" + str(self.testEnemy.id) + '/'

        self.friend1 = Friend.objects.create(id = friendID1,author_id = self.testFriend.id,host = "localhost",display_name = "friend",url = url1)
        self.friend2 = Friend.objects.create(id = friendID2,author_id = self.testFriend.id,host = "localhost",display_name = "enemy",url = url2)

        self.author.friends.add(self.friend1)

        self.assertEqual(self.author.friends.count(), 1)

    
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


        getUrl = 'http://127.0.0.1:8000/api/friends/' + str(self.author.id) + '/'
        response = self.client.get(getUrl)
        expectedFriends = [self.testFriend.id]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('authors'),expectedFriends)

        #TEST POSTING

        # ask a service if anyone in the list is a friend
        # POST to http://service/friends/<authorid>
        #{
	# "query":"friends",
        #     "author":"<authorid>",
        #     # Array of Author UUIDs
        #     "authors": [
        #         "de305d54-75b4-431b-adb2-eb6b9e546013",
        #         "ae345d54-75b4-431b-adb2-fb6b9e547891",
        #         "...",
	# 	"...",
	# 	"..."
  	# ]
        #     }

        # # responds with
        # {
        # "query":"friends",
        # "author":"9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        # # Array of Author UUIDs who are friends
        #     "authors": [
        #         "de305d54-75b4-431b-adb2-eb6b9e546013",
        #         "ae345d54-75b4-431b-adb2-fb6b9e547891",
        #         "..."
        #     ]
        # }

        data = {"query":"friends",
                "author":str(self.author.id),
                "authors":[str(self.testEnemy.id),str(self.testFriend.id)]}

        #we expect
        #"query":"friends",
        # "author":"author.id",
        # # Array of Author UUIDs who are friends
        #     "authors": [
        #         "testFriend.id",]


        postResponse = self.client.post(getUrl,data,format='json')
        
        friendsCalculated= postResponse.data.get('authors')

        self.assertEqual(postResponse.status_code, status.HTTP_200_OK)
        self.assertEqual(Author.objects.count(),3) # no new authors made
        self.assertEqual(Friend.objects.count(),2) # no new friends
        self.assertEqual(len(friendsCalculated),1)
        self.assertEqual(friendsCalculated[0],str(self.testFriend.id))

        data = {"query":"friendrequest",
                "author": {"id":str(self.author.id),
                           "host":self.author.host,
                           "displayName":"tim",
                           },
                "friend": {
                    "id":str(self.friend2.id),
                    "host":self.friend2.host,
                    "displayName":self.friend2.display_name,
                    "url":self.friend2.url
                    }
                }

        Url='http://127.0.0.1:8000/api/friendrequest/'
        postResponse = self.client.post(Url,data,format='json')
        self.assertEqual(postResponse.status_code, status.HTTP_200_OK)

	# 	"host":"http://127.0.0.1:5454/",
	# 	"displayName":"Greg Johnson"
	# },
	# "friend": {
	#     # UUID
	# 	"id":"de305d54-75b4-431b-adb2-eb6b9e637281",
	# 	"host":"http://127.0.0.1:5454/",
	# 	"displayName":"Lara Croft",
	# 	"url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e"
	# }
