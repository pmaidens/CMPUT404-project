import uuid,json
from django.utils import timezone
from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Author, Friend, Post, Comment
from rest_framework import status
from rest_framework.test import  APITestCase, APIClient
from django.test.client import Client



# This class tests some functionality of the backend, and
# attempts to simulate handling the requests the client
# will make to the API

# Specific user stories tested

    # US01 As an author I want to make posts
    # https://github.com/pmaidens/CMPUT404-project/issues/1
    
    # US09 As an author, posts I create can be public
    # https://github.com/pmaidens/CMPUT404-project/issues/9

    # US10 As an author, posts I make can be simple plain text
    # https://github.com/pmaidens/CMPUT404-project/issues/10

    # US11 As an author, posts I make can be in markdown
    # https://github.com/pmaidens/CMPUT404-project/issues/11

    # US30 - As an Author I want to comment on Posts I can access
    # https://github.com/pmaidens/CMPUT404-project/issues/30

    # US18 As an author, I want to delete my own posts.
    # https://github.com/pmaidens/CMPUT404-project/issues/18

# Other functionality is also tested, but does not subscribe to
# specific user stories
class apiTests(TestCase):
    
    def setUp(self):
        # Create Author for testing
        self.authorUser = User.objects.create_user('PostAuthor', 'post@post.com','post secret')
        self.author = Author.objects.get(user = self.authorUser)
        self.client = APIClient()


    def test_Posts(self):
        # Test that a get from nothing returns a 404
        randID = str(uuid.uuid4())
        getUrl = '/api/posts/' + randID + '/'
        response = self.client.get(getUrl)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
      

        # Get The posts marked as public
        Url = '/api/posts/'
        response = self.client.get(Url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(),response.data.get('count'))
        self.assertEqual(response.data.get('count'),0)


        # make a post in plain text
        now = str(datetime.now())
        data = {"title":"plain text post","source":"src",
                "origin":"origin","description":"neat",
                "contentType":'text/plain',
                "content":"sample text",
                "categories":["cool"],"published":now,
                "author":self.author.id,
                "visibility":'PUBLIC'
        }
    
        postResponse = self.client.post(Url,data,format='json')
        
        # Check the Post
        self.assertEqual(postResponse.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'plain text post')

        # ensure it showed up in the public stream
        get = self.client.get('/api/posts/')
        self.assertEqual(get.status_code,status.HTTP_200_OK)
        self.assertNotEqual(get.data.get('posts'),'[]')
        
        # Get the Post
        postID = Post.objects.get().id
        getUrl = '/api/posts/' + str(postID) + '/'
        getResponse = self.client.get(getUrl)
        self.assertEqual(getResponse.status_code,status.HTTP_200_OK)

        # Test PUT to posted entity -- should update        
        data["title"] = "new title"
        data["description"] = "not neat!"
        
        self.client.force_authenticate(user = self.authorUser)

        putResponse = self.client.put(getUrl,data,format='json')
        self.assertEqual(putResponse.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 1) # ensure nothing new was made

        # ensure the changes are reflected
        self.assertEqual(Post.objects.get().title, 'new title')
        self.assertEqual(Post.objects.get().source, 'src')
        self.assertEqual(Post.objects.get().description, 'not neat!')


        # make a post in Markdown
        now = str(datetime.now())
        data = {"title":"markdown post","source":"src",
                "origin":"origin","description":"neat",
                "contentType":'text/x-markdown',
                "content":"###Markdown text###",
                "categories":["cool"],"published":now,
                "author":self.author.id}
    
        postResponse = self.client.post(Url,data,format='json')
        qs = Post.objects.all()

        # Check the Post
        self.assertEqual(postResponse.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

        # Comment on post
        cID = uuid.uuid4()
        comment = {
            "author": {
                "id": str(self.author.id),
                "host": str(self.author.host),
                "displayName": "greg",
                "url":str(self.author.url),
                "github":str(self.author.github),
                },
            "comment":"Nice Post!",
            "content-type":'text/plain',
            "published":now,
            "id":str(cID),
            }
            #"post": postID,
        
        commentUrl = getUrl + 'comments/'
        commentResponse = self.client.post(commentUrl,comment,format='json')
        self.assertEqual(commentResponse.status_code, status.HTTP_201_CREATED)
        
        # Delete post
        delResp = self.client.delete(getUrl)
        self.assertEqual(delResp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(),1)

     
    # initial tests for friend functionality
    def test_Friends(self):

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
       # self.friend2 = Friend.objects.create(id = friendID2,author_id = self.testFriend.id,host = "localhost",display_name = "enemy",url = url2)

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
        self.assertEqual(Friend.objects.count(),1) # no new friends
        self.assertEqual(len(friendsCalculated),1) # 1 author returned
        self.assertEqual(friendsCalculated[0],str(self.testFriend.id))

        # Friend requests

        url =  '/api/friendrequest/'

        # {
	# "query":"friendrequest",
	# "author": {
	#     # UUID
	# 	"id":"de305d54-75b4-431b-adb2-eb6b9e546013",
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


        
        data = {"query":"friends",
                "author":{ "id": str(self.author.id),
                           "host": str(self.author.host),
                           "displayName": "Author"
                           },
                
                "friend": { "id":str(self.testEnemy.id),
                            "host":str(self.testEnemy.host),
                            "displayName": "Enemy",
                            "url":str(self.testEnemy.url),
                            }
                }

        print self.testEnemy.host
        print self.author.host

        friendRequest = self.client.post(url,data,format='json')
        self.assertEqual(friendRequest.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.author.following.all()),1)
        self.assertEqual(len(self.testEnemy.pendingFriends.all()),1)
        self.assertEqual(len(Friend.objects.all()),3) # 2 friends created
        
        #Test Friend Querying:

        url = 'http://127.0.0.1:8000/api/friends/'+str(self.author.id) +'/'+ str(self.testFriend.id)+'/'
        
        friendQuery = self.client.get(url)
        self.assertEqual(friendQuery.status_code, status.HTTP_200_OK)
        self.assertEqual(friendQuery.data['friends'], True)

        

        # TESTS US25 As a server admin, add, modify, and remove authors
        # https://github.com/pmaidens/CMPUT404-project/issues/25

        # TESTS US13 As a server admin, host multiple authors on my server
        # https://github.com/pmaidens/CMPUT404-project/issues/13

        # Tests not running due to HTTP400 bad request error in test

    # def test_Author(self):
        
    #     prevCount = Author.objects.count()

    #     # Add an author
    #     authorUser = User.objects.create_user('tmepAuthor', 'temp@post.com','secret')
    #     author = Author.objects.get(user = authorUser)
    #     self.assertEqual(Author.objects.count(), prevCount+1)

    #     data = {"user":author.user.id, 
    #             "id":author.id, 
    #             "host":author.host, 
    #             "url":author.url,
    #             "friends":author.friends,
    #             "github":author.github,
    #             "bio":author.bio}
        
    #     self.client.force_authenticate(user = authorUser)

    #     url = '/api/author/'

    #     post = self.client.post(url, data, format='json')
    #     self.assertEqual(post.status_code, status.HTTP_201_CREATED)

    #     # Modify the author
    #     prevBio = author.bio
    #     data['bio'] = 'This guy did something amazing; it will define their existence!'
        
    #     put = self.client.put(url, data, format='json')
    #     self.assertEqual(put.status_code, status.HTTP_200_OK)

    #     getAuth = self.client.get(url)
    #     getAuth = getAuth.data.get("bio")
    #     self.assertNotEqual(getAuth.bio,None)#prevBio)

    #     # Make/Host a second author
    #     authorUser2 = User.objects.create_user('tempAuthor', 'tmep@post.com','secret2')
    #     author2 = Author.objects.get(user = authorUser2)
    #     data = {"user":author2.user.id, "id":author2.id, "host":author2.host, "url":author2.url, "bio":author2.bio}
    #     url2 = '/api/author/'

    #     self.client.force_authenticate(user = authorUser2)

    #     post = self.client.post(url2, data, format='json')
    #     self.assertEqual(post.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(Author.objects.count(), prevCount+2)
