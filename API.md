    Endpoint: /api/author/
    Available Methods: GET
    This end point lists all the authors on the server.
    To add an author you have to register on the site.

      GET Repsonse objects properties:
          id -  guid of the author
          host - the host server that the author resides on
          displayname - the username of the author and the name that will be displayed for an author
          url - the host url that points to the author
          friends - a list of the author's approved friends
          first_name - the first name of an author
          last_name - the last name of an author
          email - the email of an author
          bio - the bio of an author

    Endpoint: /api/author/{AUTHOR_ID}/
    Available Methods: GET, PUT
    This end point gets the specific author that has the AUTHOR_ID.
    Use this endpoint to view a specific author and to update author information.

      GET Repsonse object properties:
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

    Endpoint: /api/posts/
    Available Methods: GET, POST
    This endpoint lists the posts that are currently available to the authenticated user.
    You can also create a new post for the current user.

      GET Repsonse objects properties:
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

    Endpoint: /api/posts/{POST_ID}/
    Available Methods: GET, PUT, DELETE
    This endpoint gets the specific post with the POST_ID.
    You can also update the post and delete it.

      GET Repsonse object properties:
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

    Endpoint: /api/posts/{POST_ID}/comments/
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

    Endpoint: /api/posts/{POST_ID}/comments/{COMMENT_ID}/
    Available Methods: GET
    This endpoint gets the specific comment corresponding to the COMMENT_ID and POST_ID.

      GET Response object properties:
          author - the author object that wrote the comment
          comment - the text of the comment
          pubDate - the date that the comment was created
          guid - the guid of the comment

    Endpoint: /api/friends/
    Available Methods: GET
    This endpoint lists any friends that an author has.

      GET Response object properties:
          query - the current query
          authors - the list of friends the current author has
          friends - boolean specifying if the author is a friend or not
