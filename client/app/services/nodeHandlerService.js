"use strict";

angular.module("myApp.services.nodeHandler", [
    "myApp.services.urlHandler",
    "myApp.services.authenticationHandler"
])
.service("nodeHandler", function($q, $http, urlHandler, authenticationHandler) {

    $http.defaults.headers.common.Authorization = authenticationHandler.token;
    this.nodesRequest = $http.get(urlHandler.apiURL() + "nodes/");

    this.sendToAll = function (httpVerb, relativeURL, requestParameters, specialCases) {
        return $q(function (resolve, reject) {
            this.nodesRequest.then(function (result) {
                var nodes = result.data;
                var allRequest = [];

                allRequest.push(this.sendTo(urlHandler.serviceURL(), httpVerb, relativeURL, requestParameters));

                nodes.forEach(function (node) {
                    var currentRelativeURL = relativeURL;
                    specialCases.forEach(function (specialCase) {
                        if (specialCase && specialCase.url === node.url) {
                            if (specialCase.relativeURL) {
                                currentRelativeURL = specialCase.relativeURL;
                            }
                        }
                    });
                    allRequest.push(this.sendTo(node.url, httpVerb, currentRelativeURL, requestParameters));
                }.bind(this));

                $q.all(allRequest).then(function (results) {
                    resolve(results);
                }, function (err) {
                    reject(err);
                });
            }.bind(this));
        }.bind(this));
    };

    this.sendTo = function (nodeURL, httpVerb, relativeURL, requestParameters) {
        return $q(function (resolve, reject) {
            this.nodesRequest.then(function (result) {
                var nodes = result.data;
                var node;
                if(urlHandler.apiURL().includes(nodeURL)) {
                    $http.defaults.headers.common.Authorization = authenticationHandler.token;
                    $http[httpVerb](urlHandler.apiURL() + relativeURL, requestParameters).then(function (result) {
                        resolve(result);
                    });
                } else {
                    var isRemoteNode = nodes.some(function (element) {
                        if (element.url.includes(nodeURL)) {
                            node = element;
                            return true; // break
                        }
                    });

                    if(isRemoteNode) {
                        $http.defaults.headers.common.Authorization = authenticationHandler.generateToken(node.username, node.password);
                        $http[httpVerb](node.url + relativeURL, requestParameters).then(function (result) {
                            resolve(result);
                        });
                    } else {
                        reject(new Error("Node URL not known"));
                    }
                }
            }.bind(this));
        }.bind(this));
    };
});
