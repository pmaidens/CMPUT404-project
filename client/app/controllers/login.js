"use strict";

angular.module("myApp.login", ["ngRoute", "myApp.services.authenticationHandler"])

.config(["$routeProvider", function($routeProvider) {
    $routeProvider.when("/login", {
        templateUrl: "partials/login.html",
        controller: "LoginController"
    });
}])

.controller("LoginController", function($scope, $location, authenticationHandler) {
    $scope.submit = function() {
    	authenticationHandler.login($scope.username, $scope.password).then(function() {
    		$location.url("/");
    	});
    };
});
