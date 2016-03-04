"use strict";

angular.module("myApp.services.authorHandler", [])
.service("authorHandler", function($q) {
    this.getAuthor = function (authorId) {//eslint-disable-line no-unused-vars
        return $q(function(resolve/*, reject*/) {
            setTimeout(function () {
                resolve(STUBgetAuthorId);
            }.bind(this), 1000);
        }.bind(this));
    };

    var STUBgetAuthorId = {
        "id":"de305d54-75b4-431b-adb2-eb6b9e546013",
        "host":"http://127.0.0.1:5454/",
        "displayName":"Lara Croft",
        "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
        "github": "http://github.com/laracroft"
    };
});
