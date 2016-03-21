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

.controller("FriendsFeedController", function($scope, $http, $location, $q, authenticationHandler, urlHandler, authorHandler) {
	$scope.potentialFriends = [];
	$scope.user = authenticationHandler.user;

    authorHandler.getAllAuthors().then(function(result) {

        $scope.potentialFriends = result.data;
        var followers = $scope.getfollowers();

        $q.all([followers, getRefresh($scope.user)]).then(function(){
            filteredStuff($scope.potentialFriends,$scope.followers,$scope.user,$scope.user.friends)
        })
        //var friends = getfriends($scope potentialFriends);
     
    });

    $scope.getfollowers = function(){

    return authorHandler.getFollowers($scope.user.id).then(function(result){

        $scope.followers = result.data[0].friendrequests;

        });

 

    };  

    var getRefresh = function(user){
        return authorHandler.getAuthor(user.id).then(function(result){
            $scope.followers = result.data.friendrequests;
            $scope.friends = result.data.friends;
        });
    }; 
    
    var filteredStuff = function(potentialFriends, followers, user, friends){

     $scope.filteredPotentialFriends = potentialFriends.filter(function(filteredPotentialFriends){
            console.log(filteredPotentialFriends.id);
            return (!followers.some(function(follower){
                return filteredPotentialFriends.id === follower.author_id;
            })
            && !friends.some(function(friend){
                return filteredPotentialFriends.id === friend.author_id;
            })&& filteredPotentialFriends.id !== user.id);
        
            });
    };

    authorHandler.getFollowing($scope.user.id).then(function(result){

        $scope.friendsSOON = result.data;

    
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

