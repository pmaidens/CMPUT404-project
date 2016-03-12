"use strict";

angular.module("myApp.login", ["ngRoute", "myApp.services.authenticationHandler"])

.config(["$routeProvider", function($routeProvider) {
    $routeProvider.when("/login", {
        templateUrl: "partials/login.html",
        controller: "LoginController"
    });
}])

.controller("LoginController", function($scope, $location, authenticationHandler) {
 
    $scope.register = function () {
        authenticationHandler.register({
            username: $scope.username,
            password1: $scope.password1,
            password2: $scope.password2,
            email: $scope.email
        });
    };
});
