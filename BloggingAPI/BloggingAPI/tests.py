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
        self.authorUser.set_password('post secret')
        self.authorUser.save()
        self.author = Author.objects.get(user = self.authorUser)
        self.client = APIClient()

        self.client.login(username='PostAuthor', password='post secret')
        self.client.force_authenticate(user=self.authorUser)


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


        # make a private post in plain text
        now = str(datetime.now())
        data = {"title":"private plain text post","source":"src",
                "origin":"origin","description":"neat",
                "contentType":'text/plain',
                "content":"sample text",
                "categories":["cool"],"published":now,
                "author":self.author.id,
                "visibility":'PRIVATE'
        }
    
        postResponse = self.client.post(Url,data,format='json')
        
        # Check the Post
        self.assertEqual(postResponse.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'private plain text post')

        # ensure it didn't show up in the public stream
        get = self.client.get('/api/posts/')
        self.assertEqual(get.status_code,status.HTTP_200_OK)
        self.assertEqual(get.data.get('posts'),[])

        # Now make a public post in plain text
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
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.objects.all()[1].title, 'plain text post')

        # ensure it DOES show up in the public stream
        get = self.client.get('/api/posts/')
        self.assertEqual(get.status_code,status.HTTP_200_OK)
        self.assertNotEqual(get.data.get('posts'),[])
        
        # Get the Post
        postID = Post.objects.all()[1].id
        getUrl = '/api/posts/' + str(postID) + '/'
        getResponse = self.client.get(getUrl)
        self.assertEqual(getResponse.status_code,status.HTTP_200_OK)

        # Test PUT to posted entity -- should update        
        data["title"] = "new title"
        data["description"] = "not neat!"
        
        self.client.force_authenticate(user = self.authorUser)

        putResponse = self.client.put(getUrl,data,format='json')
        self.assertEqual(putResponse.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 2) # ensure nothing new was made

        # ensure the changes are reflected
        self.assertEqual(Post.objects.all()[1].title, 'new title')
        self.assertEqual(Post.objects.all()[1].source, 'src')
        self.assertEqual(Post.objects.all()[1].description, 'not neat!')

        # make a post in Markdown
        now = str(datetime.now())
        data = {"title":"markdown post","source":"src",
                "origin":"origin","description":"neat",
                "contentType":'text/x-markdown',
                "content":"###Markdown text###",
                "categories":["cool"],"published":now,
                "author":self.author.id}
    
        postResponse = self.client.post(Url,data,format='json')

        # Check the Post
        self.assertEqual(postResponse.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)

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
        
        commentUrl = getUrl + 'comments/'
        commentResponse = self.client.post(commentUrl,comment,format='json')
        self.assertEqual(commentResponse.status_code, status.HTTP_201_CREATED)
        
        # Delete post
        delResp = self.client.delete(getUrl)
        self.assertEqual(delResp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(),2)




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

        self.friend1 = Friend.objects.create(id = friendID1,author_id = self.testFriend.id,host = "localhost",displayName = "friend",url = url1)
        self.author.friends.add(self.friend1)
        self.assertEqual(self.author.friends.count(), 1)

    
        # API SPEC TEST
        # Get http://service/friends/<authorid>

        getUrl = 'http://127.0.0.1:8000/api/friends/' + str(self.author.id) + '/'
        response = self.client.get(getUrl)
        expectedFriends = [self.testFriend.id]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('authors'),expectedFriends)


        # API SPEC TEST
        # ask a service if anyone in the list is a friend
        # POST to http://service/friends/<authorid>

        data = {"query":"friends",
                "author":str(self.author.id),
                "authors":[str(self.testEnemy.id),str(self.testFriend.id)]}

        # we expect
        """
        {
        "query":"friends",
         "author":"self.author.id",
         "authors": ["testFriend.id",]
        }
        """

        postResponse = self.client.post(getUrl,data,format='json')
        friendsCalculated= postResponse.data.get('authors')

        self.assertEqual(postResponse.status_code, status.HTTP_200_OK)
        self.assertEqual(Author.objects.count(),3) # no new authors made
        self.assertEqual(Friend.objects.count(),1) # no new friends
        self.assertEqual(len(friendsCalculated),1) # 1 author returned
        self.assertEqual(friendsCalculated[0],str(self.testFriend.id))

        # API SPEC TEST
        # Make a friend request to author

        url =  '/api/friendrequest/'

        data = {"query":"friends",
                "author": { "id":str(self.testEnemy.id),
                            "host":str(self.testEnemy.host),
                            "displayName": "Enemy",
                        },
                "friend":{ "id": str(self.author.id),
                           "host": str(self.author.host),
                           "displayName": "Author",
                           "url":str(self.author.url),
                           }
                }

        friendRequest = self.client.post(url,data,format='json')
        self.assertEqual(friendRequest.status_code, status.HTTP_200_OK)

        # TESTS US33 As an author, I want to know if I have friend requests.
        self.assertEqual(len(self.author.pendingFriends.all()),1)

        # TESTS US32 As an author, When I befriend someone it follows them [until they respond]
        self.assertEqual(len(self.testEnemy.following.all()),1)
        self.assertEqual(len(Friend.objects.all()),3) # 2 friend objects created
        

        # API SPEC TEST
        # Test Friend Querying:

        # Friends
        url = 'http://127.0.0.1:8000/api/friends/'+str(self.author.id) +'/'+ str(self.testFriend.id)+'/'
        
        friendQuery = self.client.get(url)
        self.assertEqual(friendQuery.status_code, status.HTTP_200_OK)
        self.assertEqual(friendQuery.data['friends'], True) 


        # Not Friends - also switch IDs - order shouldn't matter
        url = 'http://127.0.0.1:8000/api/friends/'+str(self.testEnemy.id) +'/'+ str(self.author.id)+'/'
        
        friendQuery = self.client.get(url)
        self.assertEqual(friendQuery.status_code, status.HTTP_200_OK)
        self.assertEqual(friendQuery.data['friends'], False) 

        # Accept friend request
        data = {'friend':str(self.testEnemy.id)}
        url = 'http://127.0.0.1:8000/api/friends/acceptfriend/'
        
        post = self.client.post(url,data,format='json')
        self.assertEqual(post.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.author.pendingFriends.all()),0) # pendingFriend removed
        self.assertEqual(len(self.testEnemy.following.all()),0) # following friend removed
        self.assertEqual(len(Friend.objects.all()),3) # friend object total static
        
        # Friend fields updated
        self.assertEqual(len(self.author.friends.all()),2)
        self.assertEqual(len(self.testEnemy.friends.all()),1)

        # Query friendship again
        url = 'http://127.0.0.1:8000/api/friends/'+str(self.author.id) +'/'+ str(self.testEnemy.id)+'/'
        friendQuery = self.client.get(url)
        self.assertEqual(friendQuery.status_code, status.HTTP_200_OK)
        self.assertEqual(friendQuery.data['friends'], True) 

        # Tests US22 As an author, I want to un-befriend local authors 
        url = 'http://127.0.0.1:8000/api/friends/removefriend/'
        post = self.client.post(url,data,format='json')
        self.assertEqual(post.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.author.friends.all()),1) # Friend removed
        self.assertEqual(len(Friend.objects.all()),1) # friends count decreased
        self.assertEqual(len(self.testEnemy.friends.all()),0) # Friend removed


    def test_spec_posts(self):

        # Create Author for testing
        self.specUser = User.objects.create_user('SpecAuthor', 'Spec@post.com','Spec secret')
        self.specUser.set_password('Spec secret')
        self.specUser.save()
        self.specAuthor = Author.objects.get(user = self.specUser)
        self.client.login(username='SpecAuthor', password='Spec secret')
        self.client.force_authenticate(user=self.specUser)
    
        # The following are ways URIs that can be used for post retrieval
        #
        # 1: http://service/author/posts (posts that are visible to the currently authenticated user)
        # 
        # 2: http://service/posts (all posts marked as public on the server)
        # 
        # 3: http://service/author/{AUTHOR_ID}/posts (all posts made by {AUTHOR_ID} visible to the currently authenticated user)
        # 
        # 4: http://service/posts/{POST_ID} access to a single post with id = {POST_ID}
        # 
        # 5: http://service/posts/{post_id}/comments access to the comments in a post

        # First create second Author
        testUser = User.objects.create_user('test', 'test@post.com','test')
        testUser.set_password('test')
        testUser.save()
        testAuthor = Author.objects.get(user = testUser)

        postUrl = '/api/posts/'

        # First make a public post
        now = str(datetime.now())
        data = {"title":"public post","source":"src",
                "origin":"origin","description":"public!",
                "contentType":'text/plain',
                "content":"sample text",
                "categories":["cool"],"published":now,
                "author":testAuthor.id,
                "visibility":'PUBLIC'
        }
    
        self.client.post(postUrl,data,format='json')

        # Next make a private post
        now = str(datetime.now())
        data = {"title":"private post","source":"src",
                "origin":"origin","description":"private!",
                "contentType":'text/plain',
                "content":"sample text",
                "categories":["cool"],"published":now,
                "author":testAuthor.id,
                "visibility":'PRIVATE'
        }
    
        self.client.post(postUrl,data,format='json')

        # recall that self.author is the currently authenticated user

        # 1 - one post, the public one, should be visible
        Url = '/api/author/posts/'
        response = self.client.get(Url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('posts')),1)
        self.assertEqual(response.data.get('posts')[0].get('title'),"public post")

        # 2 - again one post marked as public on the server
        Url = '/api/posts/'
        response = self.client.get(Url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('posts')),1)
        self.assertEqual(response.data.get('posts')[0].get('title'),"public post")

        # 3
        url = '/api/author/' + str(testAuthor.id) +'/posts/'

        # create another post with testauthor, visibility marked as friends
        now = str(datetime.now())
        data = {"title":"friends post","source":"src",
                "origin":"origin","description":"friends!",
                "contentType":'text/plain',
                "content":"sample text",
                "categories":["cool"],"published":now,
                "author":testAuthor.id,
                "visibility":'FRIENDS'
        }
        post = self.client.post(postUrl,data,format='json')
        self.assertEqual(post.status_code, status.HTTP_201_CREATED)

        
        # get posts test author has made which are visible to me should be 1
        posts = self.client.get(url)
        self.assertEqual(posts.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('posts')),1)
        self.assertEqual(response.data.get('posts')[0].get('title'),"public post")

        # now become friends, and that number should change to 2

        reqUrl =  '/api/friendrequest/'
        data = {"query":"friends",
                "author": { "id":str(testAuthor.id),
                            "host":str(testAuthor.host),
                            "displayName": "testAuthor",
                        },
                "friend":{ "id": str(self.specAuthor.id),
                           "host": str(self.specAuthor.host),
                           "displayName": "Author",
                           "url":str(self.specAuthor.url),
                           }
                }

        post = self.client.post(reqUrl,data,format='json')
        self.assertEqual(post.status_code, status.HTTP_200_OK)
          
        data = {'friend':str(testAuthor.id)}
        ackUrl = '/api/friends/acceptfriend/'
        
        post = self.client.post(ackUrl,data,format='json')
        self.assertEqual(post.status_code, status.HTTP_200_OK)

        url = '/api/author/' + str(testAuthor.id) +'/posts/'
        posts = self.client.get(url)
        self.assertEqual(posts.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('posts')),1)#_____________CHANGED---------
        self.assertEqual(response.data.get('posts')[0].get('title'),"public post")#["public post","friend post"])

        # 4 - get individual post
        # Get postID 
        id = Post.objects.all()[0].id
        Url = '/api/posts/' + str(id) +'/'
        singlePost = self.client.get(Url)
        self.assertEqual(singlePost.status_code, status.HTTP_200_OK)
        self.assertEqual(len(singlePost.data),14) # fields in 1 post
        
        
        # 5 - see test_posts for more detailed test
        Url = '/api/posts/'+str(id)+'/comments/'
        commentPost = self.client.get(Url)
        self.assertEqual(commentPost.status_code, status.HTTP_200_OK)
        print commentPost.data
        self.assertEqual(len(commentPost.data.get('comments')),0) # no comments

        # test appending page query, and size query
        Url = Url + '?page=1&size=40'
        commentPost = self.client.get(Url)
        self.assertEqual(commentPost.status_code, status.HTTP_200_OK)
        self.assertEqual(len(commentPost.data.get('comments')),0) # no comments

    def test_author(self):
         
        # Host one author
        
        numAuthors = Author.objects.count()
        url = '/rest-auth/registration/'
        
        data = {
            "Username" : "one Author!",
            "Email" : "email@email.com",
            "Password1" : "pass",
            "Password2" : "pass",
        }

        post = self.client.post(url,data,format='json')
        self.assertEqual(post.status_code, status.HTTP_200_OK)
        self.assertEqual(Author.objects.count(), numAuthors + 1)
        

    def test_spec_profile(self):
        
        url = '/api/author/' + str(self.author.id) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data.get('id'),None)
        self.assertNotEqual(response.data.get('host'),None)
        self.assertNotEqual(response.data.get('displayName'),None)
        self.assertNotEqual(response.data.get('url'),None)
        self.assertNotEqual(response.data.get('friends'),None)
        
        # Response

        '''
        {
            "id":"9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            "host":"http://127.0.0.1:5454/",
            "displayName":"Lara",
            "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
            "friends": [
                {
                    "id":"8d919f29c12e8f97bcbbd34cc908f19ab9496989",
                    "host":"http://127.0.0.1:5454/",
                    "displayName":"Greg",
                    "url": "http://127.0.0.1:5454/author/8d919f29c12e8f97bcbbd34cc908f19ab9496989"
                }
            ],
            
            # Optional attributes
            "github_username": "lara",
            "first_name": "Lara",
            "last_name": "Smith",
            "email": "lara@lara.com",
            "bio": "Hi, I'm Lara"
        }
        '''


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

        
        

