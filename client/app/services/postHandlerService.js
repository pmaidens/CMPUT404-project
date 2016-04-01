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
        // var urlToCheck = urlToPostTo.split("/");
        // if(urlToCheck[0] !="http:"){
        //     urlToCheck.unshift( "http:/" );
        // }
        // var realUrlToCheck = urlToCheck.join("/");
        // console.log(realUrlToCheck);
        // var encoded ="";
        // var nodes = nodeHandler.nodes;
        // nodes.forEach(function(node){
        //     if (urlToCheck[2] == "cmput404-team-4b.herokuapp.com"){
        //         encoded = window.btoa(node.username + ":" + node.password);
        //         $http.defaults.headers.common.Authorization = "Basic " +  encoded;
        //     }else{
        //         $http.defaults.headers.common.Authorization = authenticationHandler.token;
        //     }
        // });
        // //$http.defaults.headers.common.Authorization = authenticationHandler.token;
        //
        // //TODO check  url root against nodes and then grab the username and password encode it then send it over.
        // //var
        // return $http(
        //     {
        //         method:"POST",
        //         url:realUrlToCheck,
        //         //url:"http://project-c404.rhcloud.com/api/posts/8e4f11cf-8e3f-4468-9a53-8835a1dd65ac/comments/",
        //         data:post
        //     }
        // );
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
