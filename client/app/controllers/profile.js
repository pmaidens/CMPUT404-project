"use strict";

angular.module("myApp.profile", [
    "ngRoute",
    "myApp.directives.postStream",
    "myApp.services.authorHandler"
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

.controller("Profile", function($scope, $routeParams, authorHandler) {
    $scope.author = {};
    $scope.postStream = {authorId: $routeParams.authorId};
    $scope.editing = false;

    $scope.clickEdit = function () {
        $scope.editing = !$scope.editing;
    };

    $scope.submitAuthor = function () {
        $scope.editing = !$scope.editing;
    };

    authorHandler.getAuthor($routeParams.authorId).then(function (result) {
        $scope.author = result;
    });
});
