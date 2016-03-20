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
});