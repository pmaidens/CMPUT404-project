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
    $scope.isFollowing = false;
    $scope.hasFollowers = false;
    $scope.friends = $scope.user.friends;
    console.log($scope.friends.length!=0);

    authorHandler.getAllAuthors().then(function(result) {


        $scope.authors = result.data;
     
    });

    authorHandler.getFollowers($scope.user.id).then(function(result){

        $scope.followers = result.data[0].friendrequests;
	console.log($scope.followers);
	if($scope.followers.length){
	
	    $scope.hasFollowers = true;
	    
	}


    });

    authorHandler.getFollowing($scope.user.id).then(function(result){

        $scope.friendsSOON = result.data[0].following;
	if($scope.friendsSOON.length){

	    $scope.isFollowing = true;
	}
	

    
    });



    $scope.makeFriendReq = function(author){
        var friend = {
            "id": author.id,
            "host":author.host,
            "displayName": author.displayname,
            "url": author.url
        };

        authorHandler.postFriendRequest(friend).then(function() {alert("Friend Request Sent")}, function() {alert("uh-oh, something went wrong")});
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

