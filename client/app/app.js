"use strict";

// Declare app level module which depends on views, and components
angular.module("myApp", [
    "ngRoute",
    "btford.markdown",
    "myApp.postWriter",
    "myApp.postStream",
    "myApp.profile",
    "myApp.version",
    "myApp.navbar",
    "myApp.login"
]).
config(["$routeProvider", function($routeProvider) {
    $routeProvider.otherwise({redirectTo: "/stream"});
}]);
