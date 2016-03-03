"use strict";

angular.module("myApp.postWriter", ["ngRoute", "myApp.services.postHandler"])

.config(["$routeProvider", function($routeProvider) {
    $routeProvider.when("/write", {
        templateUrl: "partials/postWriter.html",
        controller: "PostWriterController"
    });
}])

.controller("PostWriterController", function($scope, $http, postHandler) {

    function separateCategories(inputValue) {
        return inputValue.split(",").map(function (category) {
            return category.trim();
        }).filter(function (category) {
            return !!category;
        });
    }

    $scope.SubmitPost = function () {
        // TODO: Change this object to whatever it needs to be
        postHandler.createPost({
            author: 123,
            title: $scope.title || "",
            description: $scope.description || "",
            contentType: $scope.contentType,
            categories: separateCategories($scope.categories || ""),
            visibility: $scope.visibility,
            content: $scope.content || ""
        });
        // $http({
        //     method: "POST",
        //     url: "base/server/url/authors/123/posts",
        //     data: {
        //         author: 123,
        //         title: $scope.title || "",
        //         description: $scope.description || "",
        //         contentType: $scope.contentType,
        //         categories: separateCategories($scope.categories || ""),
        //         visibility: $scope.visibility,
        //         content: $scope.content || ""
        //     }
        // });
    };

    $scope.visibility = $scope.visibility || "PUBLIC";
    $scope.contentType = $scope.contentType || "plain";
});
