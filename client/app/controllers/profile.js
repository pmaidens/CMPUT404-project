"use strict";

angular.module("myApp.profile", [
    "ngRoute",
    "myApp.directives.postStream",
    "myApp.services.authorHandler",
    "myApp.services.authenticationHandler"
])

.config(["$routeProvider", function($routeProvider) {
    $routeProvider.when("/profile/:authorId", {
        templateUrl: "partials/profile.html",
        controller: "Profile"
    });
    $routeProvider.when("/profile", {
        templateUrl: "partials/profile.html",
        controller: "Profile"
    });
}])

.controller("Profile", function($scope, $routeParams, $route , $window ,authorHandler, authenticationHandler) {
    $scope.author = {};
    $scope.postStream = {authorId: $routeParams.authorId};
    $scope.editing = false;
    $scope.hasFriends = false;
    //TODO: Don't fake this!
    $scope.user = authenticationHandler.user;
    $scope.canAddFriend = function(){

	if ($scope.postStream.authorId && $scope.user.id != $scope.postStream.authorId){

	    return true;
	}

	return false; 

    } 

    $scope.clickEdit = function () {
        if($scope.user.id === $scope.author.id) {
            $scope.editing = !$scope.editing;
        }
    };

    $scope.submitAuthor = function () {
        authorHandler.submitAuthor($scope.author).then(function () {
            $scope.editing = !$scope.editing;
        });
    };

    authorHandler.getAuthor($routeParams.authorId || $scope.user.id).then(function (result) {
        $scope.author = result.data;
	$scope.friends = $scope.author.friends;
	//get friends too
	if ($scope.friends.length){
	    $scope.hasFriends = true;

	}

    });

    $scope.makeFriendReq = function(){
        var friend = {
            "id":$scope.author.id,
            "host":$scope.author.host,
            "displayName": $scope.author.displayname,
            "url":$scope.author.url
        };

        authorHandler.postFriendRequest(friend).then(function() {alert("Friend Request Sent")}, function() {alert("uh-oh, something went wrong")});
    }
    
    $scope.getFollowers = function(){
	
	authorHandler.getFollowers($scope.author.id).then(function(result){

	    //set $scope.followers here

	});

    };
    $scope.getFollowing = function(){
	
	authorHandler.getFollowing().then(function(result){

	    //set $scope.friendsSOON

	
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
	    alert('unfriended!');
	    $window.location.reload();

	});

    };

    $scope.acceptFriend = function(follower){
	
	authorHandler.acceptFriend(follower).then(function(result){
	    alert('friend request accepted!');
	    $window.location.reload();
	
	});

    };

    

});
