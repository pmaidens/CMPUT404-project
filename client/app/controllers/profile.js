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

.controller("Profile", function($scope, $routeParams, authorHandler, authenticationHandler) {
    $scope.author = {};
    $scope.postStream = {authorId: $routeParams.authorId};
    $scope.editing = false;
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
	console.log(result.data);
        $scope.author = result.data;
    });

    $scope.makeFriendReq = function(){
	//friendReq should actually be made in the back end
	var friendReq = {
	    "query":"friendrequest",
	    "author":{
		"id": $scope.user.id,
		"host": $scope.user.host,
		"displayName": $scope.user.displayname,
	    },
	    "friend":{
		"id":$scope.author.id,
		"host":$scope.author.host,
		"displayName": $scope.author.displayname,
		"url":$scope.author.url

	    }

	};

    }

});
