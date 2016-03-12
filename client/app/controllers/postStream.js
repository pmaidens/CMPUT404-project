"use strict";

angular.module("myApp.postStream", [
    "ngRoute",
    "myApp.services.postHandler",
    "myApp.services.authenticationHandler"
])

.config(["$routeProvider", function($routeProvider) {
    $routeProvider.when("/stream", {
        templateUrl: "partials/postStream.html",
        controller: "PostStreamController"
    });
}])

.controller("PostStreamController", function($scope, $http, postHandler, authenticationHandler) {
    var targetAuthorId;
    $scope.user = authenticationHandler.user;
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


        $scope.posts = result.data.posts;
	console.log(result.data.posts);

	//in $scope.posts we have to add our friend's posts as well.
	/*
	var url = 'localhost:8000/api/friends/' + targetAuthorId + '/';
	$http.get(url).then(function(friendData){

	var friends = friendData.authors;

	for(var i = 0 ; i< friends.length; i++){

	var url2 = 'localhost:8000/api/author/' + friends[i] + '/posts/';
	
	$http.get(url2).then(function(postData){

	$scope.posts += postData.data.posts;

	

	});
	

	}


	});


	 */

        loadGit();
    });

    // Make a http call to the github api to get all user information
    // associated with the git_username

    var loadGit = function () {
	//change $scope.git_username to the author's github user name
	

	var gitHubURL = $scope.user.github;
	console.log($scope.user);
	$scope.git_username = gitHubURL.substring(gitHubURL.lastIndexOf('/')+1)


	console.log(authenticationHandler.token);
        $http({method: 'GET', url:"https://api.github.com/users/"+$scope.git_username , headers:{'Authorization':undefined}}).success(function(gitdata){


	        $scope.gitUserData = gitdata;
                loadEvents();


	});

    };
    // Http call for github repos (not too sure what Abram means by "activity")
    // ** May need to make additional calls

    var loadEvents = function () {
        $http({method:'GET', url: "https://api.github.com/users/"+$scope.git_username+"/events" , headers:{'Authorization':undefined}})
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
            author: authenticationHandler.user.id,
            comment: comments,
            post: post.id
        });
        comments = null;
    };
});
