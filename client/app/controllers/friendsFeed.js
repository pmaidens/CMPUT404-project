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

    $scope.makeFriendReq = function(){
        var friend = {
            "id":$scope.user.id,
            "host":$scope.user.host,
            "displayName": $scope.user.displayname,
            "url":$scope.user.url
        };

        authorHandler.postFriendRequest(friend).then(function() {alert("Friend Request Sent")}, function() {alert("uh-oh, something went wrong")});
    }

   

});