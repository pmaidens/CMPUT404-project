"use strict";

angular.module("myApp.postStream", ["ngRoute", "myApp.services.postHandler"])

.config(["$routeProvider", function($routeProvider) {
    $routeProvider.when("/stream", {
        templateUrl: "partials/postStream.html",
        controller: "PostStreamController"
    });
}])

.controller("PostStreamController", function($scope, $http, postHandler) {
    var targetAuthorId;
    $scope.user = {id: "7a0465c9-b89e-4f3b-a6e7-4e35de32bd64"};
    $scope.posts = [];
    //TODO change to author.github
    $scope.git_username = "sjpartri";  // This will have to be changed "hard-coded for now"

    // If something else tells us what authorId to use, then
    // we know that we should load the posts of that user.
    // Otherwise, we should just load all the posts the current
    // signed in user can see.
    if($scope.postStream && $scope.postStream.authorId) {
        targetAuthorId = {id: $scope.postStream.authorId};
    }
    postHandler.getPosts(targetAuthorId).then(function(result) {
        $scope.posts = result.data;
		//result[1] for example has these fields:
		/*
			(title', 'source', 'origin', 'description', 'contentType',
              'content', 'author', 'categories', 'visibility')
			access them like result[1].title
		*/
		//console.log(result.data);
	//in $scope.posts we have to add our friend's posts as well.
	/*

	 */
        loadGit();
    });

    // Make a http call to the github api to get all user information
    // associated with the git_username

    var loadGit = function () {
	//change $scope.git_username to the author's github user name
	/*
	  $http.get('http://localhost:8000/api/author'+$scope.postStream.authorId+'/').then(function(authData){
	  var githubUserName = authData.github.split('/')[2];
	  //i dunno if this works but i think it should
	  $scope.git_username = githubuserName;
	  });
	 */
        $http.get("https://api.github.com/users/"+$scope.git_username)
            .success(function(gitdata) {
                $scope.gitUserData = gitdata;
                loadEvents();
            });
    };
    // Http call for github repos (not too sure what Abram means by "activity")
    // ** May need to make additional calls

    var loadEvents = function () {
        $http.get("https://api.github.com/users/"+$scope.git_username+"/events")
            .success(function(event_data){
                $scope.eventData = event_data;
             
                $scope.allPost = $scope.posts.concat($scope.eventData);
                //console.log($scope.allPost);
            });
    };

    $scope.deletePost = function(post) {
        post.disabled = true;
        postHandler.deletePost(post.id).then(function(result) {
			//postHandlerService should reload the page


        });
    };

    $scope.editPost = function (post) {
        post.editMode = true;
    };

    $scope.submitPost = function (post) {
        postHandler.updatePost(post);
        post.editMode = false;
    };

//localhost/api/posts/{postid}/comments

//POST : author id, comment, postid
    $scope.AddComment = function (post, comments) {
        postHandler.commentPost({
            author: "7a0465c9-b89e-4f3b-a6e7-4e35de32bd64",
            comment: comments,
            post: post.id
        });
    };
});
