"use strict";

angular.module("myApp.postStream", ["ngRoute", "myApp.services.postHandler"])

.config(["$routeProvider", function($routeProvider) {
    $routeProvider.when("/stream", {
        templateUrl: "partials/postStream.html",
        controller: "PostStreamController"
    });
}])

.controller("PostStreamController", function($scope, postHandler) {
    var targetAuthorId;
    $scope.user = {id: "de305d54-75b4-431b-adb2-eb6b9e546013"};
    $scope.posts = [];

    // If something else tells us what authorId to use, then
    // we know that we should load the posts of that user.
    // Otherwise, we should just load all the posts the current
    // signed in user can see.
    if($scope.postStream && $scope.postStream.authorId) {
        targetAuthorId = {id: $scope.postStream.authorId};
    }
    postHandler.getPosts(targetAuthorId).then(function(result) {
        $scope.posts = result.posts;
    });

    $scope.deletePost = function(post) {
        post.disabled = true;
        postHandler.deletePost(post.id).then(function(result) {
            $scope.posts = result.posts;
        });
    };
});
