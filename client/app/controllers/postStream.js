"use strict";

angular.module("myApp.postStream", ["ngRoute", "myApp.services.postHandler"])

.config(["$routeProvider", function($routeProvider) {
    $routeProvider.when("/stream", {
        templateUrl: "partials/postStream.html",
        controller: "PostStreamController"
    });
}])

.controller("PostStreamController", function($scope, postHandler) {
	$scope.posts = [];
	postHandler.getPosts().then(function(result) {
		$scope.posts = result.posts;
	});

	$scope.deletePost = function(post) {
		post.disabled = true;
		postHandler.deletePost(post.id).then(function(result) {
			$scope.posts = result.posts;
		});
	};
});
