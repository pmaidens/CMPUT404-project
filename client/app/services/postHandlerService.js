"use strict";

angular.module("myApp.services.postHandler", [
    "ngRoute",
    "myApp.services.urlHandler",
    "myApp.services.authenticationHandler",
    "myApp.services.authorHandler",
    "myApp.services.nodeHandler"
])
.service("postHandler", function($q,$http,$route, urlHandler, authenticationHandler, authorHandler, nodeHandler) {
    this.posts = [];
    this.getPosts = function (authorId, nodeURL) {
        return $q(function(resolve) {
            var relativeURL;
            var results = {
                data: []
            };
            if(authorId) {
                relativeURL = "author/" + authorId + "/posts/";
                nodeHandler.sendTo(nodeURL, "get", relativeURL).then(function (result) {
                    console.log(result);
                    resolve(result);
                });
            } else {
                // relativeURL = "author/posts/";
                relativeURL = "posts/";
                nodeHandler.sendToAll("get", relativeURL/*, undefined, {
                    url: "https://mighty-cliffs-82717.herokuapp.com/api/",
                    relativeURL: relativeURL + "?id=" + authenticationHandler.user.id
                }*/).then(function (result) {
                    result.forEach(function (r) {
                        r.data.posts.forEach(function (post) {
                            results.data.push(post);
                        });
                    });
                    resolve(results);
                });
            }
        }.bind(this));
    };

    this.getPost = function (nodeURL, postId) {
        return nodeHandler.sendTo(nodeURL, "get", "posts/" + postId + "/");
    };

    this.deletePost = function(id) {
        $http.defaults.headers.common.Authorization = authenticationHandler.token;
        return $http.delete(urlHandler.serviceURL() + "api/posts/"+id+"/").then(function(){
            $route.reload();
        },function(err){
            console.log(err);
        });
    };

    this.createPost = function(post) {
        //TODO change the url to the proper url
        $http.defaults.headers.common.Authorization = authenticationHandler.token;
        return $http.post(urlHandler.serviceURL() + "api/posts/",post);

    };

    this.commentPost = function(comment, parentPostId, sourceURL){

        return nodeHandler.sendTo(sourceURL, "post", "posts/" + parentPostId + "/comments/", comment);
    };

    this.updatePost = function (post) {
        var putParameters = {
            title: post.title,
            source: post.source,
            origin: post.origin,
            description: post.description,
            contentType: post.contentType,
            content: post.content,
            author: post.author.id,
            categories: post.categories,
            visibility: post.visibility
        };
        $http.defaults.headers.common.Authorization = authenticationHandler.token;
        return $http.put(urlHandler.serviceURL() + "api/posts/"+post.id + "/", putParameters);
    };
});
