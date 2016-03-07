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
    $scope.user = {id: "46c07967-b790-4d6f-baf0-44a7b1a6cb45"}
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
        loadGit();
    });

    // Make a http call to the github api to get all user information
    // associated with the git_username

    var loadGit = function () {
    $http.get("https://api.github.com/users/"+$scope.git_username)
        .success(function(gitdata) {
            $scope.gitUserData = gitdata;
            loadRepos();
        });
    }
    // Http call for github repos (not too sure what Abram means by "activity")
    // ** May need to make additional calls

    var loadRepos = function () {
    $http.get($scope.gitUserData.repos_url)
        .success(function(repo_data){
                $scope.repoData = repo_data;

                $scope.allPost = $scope.posts.concat($scope.repoData);
    });
    }

    $scope.deletePost = function(post) {
        post.disabled = true;
        postHandler.deletePost(post.id).then(function(result) {
			//postHandlerService should reload the page
			

        });
    };
    $scope.editPost = function(post){

	postHandler.editPost(post);

    };
});
