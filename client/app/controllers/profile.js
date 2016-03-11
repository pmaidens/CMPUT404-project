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
        $scope.author = result.data;
    });
});
