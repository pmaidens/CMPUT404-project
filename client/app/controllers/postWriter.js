"use strict";

angular.module("myApp.postWriter", ["ngRoute"])

.config(["$routeProvider", function($routeProvider) {
    $routeProvider.when("/write", {
        templateUrl: "partials/postWriter.html",
        controller: "postWriter"
    });
}])

.controller("postWriter", function($scope, $http) {
    $scope.SubmitPost = function () {
        var postContent = $scope.postContent;
        // TODO: Chang this object to whatever it needs to be
        $http({
            method: "POST",
            url: "base/server/url/authors/123/posts",
            data: postContent
        });
    };
});
