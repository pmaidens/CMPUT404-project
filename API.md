###Endpoint: /api/author/###
    Available Methods: GET
    This end point lists all the authors on the server.
    To add an author you have to register on the site.

      GET Response objects properties:
          id -  guid of the author
          host - the host server that the author resides on
          displayname - the username of the author and the name that will be displayed for an author
          url - the host url that points to the author
          friends - a list of the author's approved friends
          first_name - the first name of an author
          last_name - the last name of an author
          email - the email of an author
          bio - the bio of an author

### Endpoint: /api/author/{AUTHOR_ID}/###
    Available Methods: GET, PUT
    This end point gets the specific author that has the AUTHOR_ID.
    Use this endpoint to view a specific author and to update author information.

      GET Response object properties:
          id - guid of the author
          host - the host server that the author resides on
          displayname - the username of the author and the name that will be displayed for an author
          url - the host url that points to the author
          friends - a list of the author's approved friends
          github - the author's github url
          first_name - the first name of an author
          last_name - the last name of an author
          email - the email of an author
          bio - the bio of an author

      PUT Request object properties:
          github (string) - the author's github url
          first_name (string) - the first name of an author
          last_name (string) - the last name of an author
          email (string) - the email of an author
          bio (string) - the bio of an author

###Endpoint: /api/posts/###
    Available Methods: GET, POST
    This endpoint lists the posts that are currently available to the authenticated user.
    You can also create a new post for the current user.

      GET Response objects properties:
          count (Posts) - number of posts
          query - the current query
          size - the size of the page
          title - the title of the post
          source - the last place this post was
          origin - the original url of the post
          description - the description of the post
          contentType - content type of the post
          content - the text of the post
          author - the author object that wrote the post
          categories - a list of categories that the post belongs to
          count - the number of comments that this post has
          comments - the list of comments of a post
          published - the date the post was created
          id - the guid of the post
          visibility - the visibility level of this post

      POST Request objects properties:
          title (string) - the title of the post
          source (string) - the last place this post was
          origin (string) - the original url of the post
          description (string) - the description of the post
          contentType (string) - (text/plain or text/markdown) content type of the post
          content (string) - the text of the post
          author (UUID) - (Required, takes in AUTHOR_ID) the author id that wrote the post
          categories (string array) - (list of strings) a list of categories that the post belongs to
          visibility (string) - (PUBLIC, FOAF, FRIENDS, PRIVATE, SERVERONLY) the visibility level of this post

###Endpoint: /api/posts/{POST_ID}/###
    Available Methods: GET, PUT, DELETE
    This endpoint gets the specific post with the POST_ID.
    You can also update the post and delete it.

      GET Response object properties:
          title - the title of the post
          source - the last place this post was
          origin - the original url of the post
          description - the description of the post
          contentType - content type of the post
          content - the text of the post
          author - the author object that wrote the post
          categories - a list of categories that the post belongs to
          count - the number of comments that this post has
          comments - the list of comments of a post
          published - the date the post was created
          id - the guid of the post
          visibility - the visibility level of this post

      PUT Request object properties:
          title (string) - the title of the post
          source (string) - the last place this post was
          origin (string) - the original url of the post
          description (string) - the description of the post
          contentType (string) - (text/plain or text/markdown) content type of the post
          content (string) - the text of the post
          author (UUID) - (Required, takes in AUTHOR_ID) the author object that wrote the post
          categories (string array) - (list of strings) a list of categories that the post belongs to
          visibility (string) - (PUBLIC, FOAF, FRIENDS, PRIVATE, SERVERONLY) the visibility level of this post

###Endpoint: /api/posts/{POST_ID}/comments/###
    Available Methods: GET, POST
    This endpoint lists the the comments for the current post (post with the id POST_ID).
    You can also post new comments for the corresponding post.

      GET Response objects properties:
          count - number of comments
          query - the current query
          size - the size of the page
          author - the author object that wrote the comment
          comment - the text of the comment
          pubDate - the date that the comment was created
          guid - the guid of the comment

      POST Request object properties:
          author (UUID) - (Required, takes in AUTHOR_ID) the author id that wrote the comment
          comment (string) - the text of the comment
          post (UUID) - (Required, takes in POST_ID) the post id that the comment belongs to

###Endpoint: /api/posts/{POST_ID}/comments/{COMMENT_ID}/###
    Available Methods: GET
    This endpoint gets the specific comment corresponding to the COMMENT_ID and POST_ID.

      GET Response object properties:
          author - the author object that wrote the comment
          comment - the text of the comment
          pubDate - the date that the comment was created
          guid - the guid of the comment

###Endpoint: /api/friends/###
    Available Methods: GET
    This endpoint lists any friends that each author has.

      GET Response object properties:
          query - the current query
          authors - the list of friends the current author has

###Endpoint: /api/friends/<author-id>###
    Available Methods: GET, POST
    This endpoint lists any friends that an author has.

      GET Response object properties:
       	  query - the current query
          authors - the list of friends the given author has

      POST Request object properties:
          query - the current query
          author - the id of the author in question
          authors - an array of Author ID's - to bechecked against 
                    the author in question to determine friendship

      POST Response object properties:
          query - the current query
          author - the id of the author in question
          authors - and array of Author ID's, all of which are friends
          with the author in question, and were present on the requested 
          list

###Endpoint: /api/friend/{AUTHOR_ID}/posts/###
    Available Methods: GET
    Gets all posts made by {AUTHOR_ID}
      GET Response properties:
          title - the title of the post
          source - the last place this post was
          origin - the original url of the post
          description - the description of the post
          contentType - content type of the post
          content - the text of the post
          categories - a list of categories that the post belongs to
          count - number of posts
          comments - the list of comments of a post
          published - the date the post was created
          id - the guid of the post
          visibility - the visibility level of this post

###Endpoint: /api/friend/{AUTHOR_ID1}/{AUTHOR_ID2}/###
    Available Methods: GET
    Used to determine the friendship of two authors,
    specified in the URL

      GET Response properties:
          query - the current query
          authors - array of author id's, specifies both
                    authors involved
          friends - a boolean, True if friends, False otherwise

###Endpoint: /api/friendrequest/###
    Available Methods: POST
    This endpoint is used to send a friendrequest to a local
    or remote author.

      POST Request object properties:
          query - the current query
          author - an object with the following properties:
                    * id - the author id
                    * host - the author host
                    * displayName - the author's display name
    
         friend - an object with the following properties:
                   * id - the friend's author id
                   * host - the friend's host
                   * displayName - the friend's display name
                   * url - the url where the friend is located

      POST Response object properties:
         Posting will manipulate the database, but not return any
         serialized data. A response of success will be returned
         on a successful request, otherwise the response will be
         an error message

###Endpoint: /api/addfollower/###
    Available Methods: POST
    When a friend request is made to a remote author, post
    here to add to the local author's followers field

      POST Request object properties:
          query - the current query

          author - an object with the following properties:
                    * id - the author id
                    * host - the author host
                    * displayName - the author's display name
    
          friend - an object with the following properties:
                   * id - the friend's author id
                   * host - the friend's host
                   * displayName - the friend's display name
                   * url - the url where the friend is located

      POST Response object properties:
         Posting will manipulate the database, but not return any
         serialized data. A response of success will be returned
         on a successful request, otherwise the response will be
         an error message

###Endpoint: /rest-auth/login/###
    Available Methods: POST
    This endpoint is to login and authenticate with the server.
    The endpoint will return an authentication token after successful login.
    You will not be able to login if your account has not been approved by an admin.

      POST Request object properties:
            username - the username of the user
            password - the password of the user

###Endpoint: /rest-auth/registration/###
    Available Methods: POST
    This endpoint is to register a user. After user creation the admin will have to approve the account before you can access the site.

      POST Request object properties:
            username - (Required) the username of the user
            email - the email of the user
            password1 - (Required) the password of the user
            password2 - (Required) the password again to verify
