"use strict";

angular.module("myApp.profile", ["ngRoute", "myApp.services.postHandler"])

.config(["$routeProvider", function($routeProvider) {
    $routeProvider.when("/profile", {
        templateUrl: "partials/profile.html",
        controller: "Profile"
    });
}])

.controller("Profile", function($scope, postHandler) {
    postHandler.getPosts();
});
