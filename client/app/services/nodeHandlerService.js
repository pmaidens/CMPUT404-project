"use strict";

angular.module("myApp.services.nodeHandler", [
    "myApp.services.urlHandler",
    "myApp.services.authenticationHandler"
])
.service("nodeHandler", function($q, $http, urlHandler, authenticationHandler) {
    this.nodes = [
        {
            "url":"https://mighty-cliffs-82717.herokuapp.com/api/",
            "username":"Team6",
            "password":"Team6"
        },
        {
            "url":"http://cmput404-team-4b.herokuapp.com/api/",
            "username": "team6",
            "password": "team6"
        }
    ];

    this.getNodes = function () {
        return this.nodes;
    };

    this.sendToAll = function (httpVerb, relativeURL, requestParameters, specialCase) {
        return $q(function (resolve, reject) {
            var allRequest = [];

            allRequest.push(this.sendTo(urlHandler.serviceURL(), httpVerb, relativeURL, requestParameters));
            this.nodes.forEach(function (node) {
                var currentRelativeURL = relativeURL;
                if (specialCase && specialCase.url === node.url) {
                    if (specialCase.relativeURL) {
                        currentRelativeURL = specialCase.relativeURL;
                    }
                }
                allRequest.push(this.sendTo(node.url, httpVerb, currentRelativeURL, requestParameters));
            }.bind(this));

            $q.all(allRequest).then(function (results) {
                resolve(results);
            }, function (err) {
                reject(err);
            });
        }.bind(this));
    };

    this.sendTo = function (nodeURL, httpVerb, relativeURL, requestParameters) {
        var node;
        if(nodeURL === urlHandler.serviceURL()) {
            $http.defaults.headers.common.Authorization = authenticationHandler.token;
            return $http[httpVerb](urlHandler.apiURL() + relativeURL, requestParameters);
        } else {
            var isRemoteNode = this.nodes.some(function (element) {
                if (element.url === nodeURL) {
                    node = element;
                    return true; // break
                }
            });

            if(isRemoteNode) {
                $http.defaults.headers.common.Authorization = authenticationHandler.generateToken(node.username, node.password);
                return $http[httpVerb](node.url + relativeURL, requestParameters);
            } else {
                throw "Node URL not known";
            }
        }
    };
});
