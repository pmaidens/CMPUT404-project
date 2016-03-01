"use strict";

angular.module("myApp.view1", ["ngRoute"])

.config(["$routeProvider", function($routeProvider) {
    $routeProvider.when("/view1", {
        templateUrl: "view1/view1.html",
        controller: "View1Ctrl"
    });
}])

.controller("View1Ctrl", function($scope, $http) {
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
