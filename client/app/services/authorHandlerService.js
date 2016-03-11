"use strict";

angular.module("myApp.services.authorHandler", ["myApp.services.urlHandler"])
.service("authorHandler", function($q, $http, urlHandler) {
    this.getAuthor = function (authorId) {//eslint-disable-line no-unused-vars
        // return $q(function(resolve/*, reject*/) {
        //     setTimeout(function () {
        //         resolve(STUBgetAuthorId);
        //     }.bind(this), 1000);
        // }.bind(this));
        return $http.get(urlHandler.serviceURL() + "api/author/" + authorId);
    };

    this.submitAuthor = function (author) {
        var putParameters = {
            github: author.github,
            first_name: author.first_name,
            last_name: author.last_name,
            email: author.email,
            bio: author.bio
        };

        return $http.put(urlHandler.serviceURL() + "api/author/" + author.id, putParameters);
    };

    var STUBgetAuthorId = {
        "id":"de305d54-75b4-431b-adb2-eb6b9e546013",
        "host":"http://127.0.0.1:5454/",
        "displayName":"laracroft",
        "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "friends": [],
        "github": "http://github.com/laracroft",
        "first_name": "Lara",
        "last_name": "Croft",
        "email": "lara@croft.com",
        "bio": "An amazing person!"
    };
});
