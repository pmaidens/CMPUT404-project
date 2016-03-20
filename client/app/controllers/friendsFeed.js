"use strict";

angular.module("myApp.friendsFeed", [
    "ngRoute",
    "myApp.services.authenticationHandler",
    "myApp.services.urlHandler",
    "myApp.services.authorHandler"
])

.config(["$routeProvider", function($routeProvider) {
    $routeProvider.when("/friendsFeed", {
        templateUrl: "partials/friendsFeed.html",
        controller: "FriendsFeedController"
    });
}])

.controller("FriendsFeedController", function($scope, $http, $location, authenticationHandler, urlHandler, authorHandler) {
	$scope.authors = [];
	$scope.user = authenticationHandler.user;

    authorHandler.getAllAuthors().then(function(result) {


        $scope.authors = result.data;
     
    });


    
    $scope.getFollowers = function(){
	
	authorHandler.getFollowers($scope.user.id).then(function(result){

	    $scope.followers = result.data;

	});

    };
    $scope.getFollowing = function(){
	
	authorHandler.getFollowing($scope.user.id).then(function(result){

	    $scope.friendsSOON = result.data;

	
	});

    };


    $scope.unfriend = function(friend){

	authorHandler.unfriend(friend).then(function(result){

	    //success!


	});

    };
    
    $scope.unfollow = function(following){

	authorHandler.unfollow(following).then(function(result){

	    //success!

	});

    };

    $scope.acceptFriend = function(follower){
	
	authorHandler.acceptFriend(follower).then(function(result){

	
	});

    };

    





});
