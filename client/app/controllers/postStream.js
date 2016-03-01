"use strict";

angular.module("myApp.postStream", ["ngRoute", "myApp.services.postFetch"])

.config(["$routeProvider", function($routeProvider) {
    $routeProvider.when("/stream", {
        templateUrl: "partials/postStream.html",
        controller: "PostStreamController"
    });
}])

.controller("PostStreamController", function($scope, postFetch) {
	$scope.posts = [];
	postFetch.getPosts().then(function(result) {
		$scope.posts = result.posts;
	})
});
