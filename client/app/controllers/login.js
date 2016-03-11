"use strict";

angular.module("myApp.login", ["ngRoute", "myApp.services.authenticationHandler"])

.config(["$routeProvider", function($routeProvider) {
    $routeProvider.when("/login", {
        templateUrl: "partials/login.html",
        controller: "LoginController"
    });
}])

.controller("LoginController", function($scope, $location, authenticationHandler) {
    $scope.login = function() {
        authenticationHandler.login($scope.username, $scope.password).then(function() {
            console.log("sup?");
            $location.url("/");
        },function(err){
            console.log(err);
        });
    };
    $scope.register = function () {
        authenticationHandler.register({
            username: $scope.username,
            password: $scope.password,
            email: $scope.email
        });
    };
});
