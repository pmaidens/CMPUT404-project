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
    "myApp.login",
    "myApp.friendsFeed",
    "ngFileUpload",
    "ngMessages"
]).
config(["$routeProvider", function($routeProvider) {
    $routeProvider.otherwise({redirectTo: "/stream"});
}]).run(["$rootScope", "$location", function($rootscope, $location) {
    $rootscope.$on("$locationChangeStart", function(event) {
        if(!$rootscope.loggedIn && $location.url !== "/login") {
            $location.path("/login");
        }
    });
}]);
