"use strict";

// Declare app level module which depends on views, and components
angular.module("myApp", [
    "ngRoute",
    "myApp.postWriter",
    "myApp.postStream",
    "myApp.version"
]).
config(["$routeProvider", function($routeProvider) {
    $routeProvider.otherwise({redirectTo: "/stream"});
}]);
