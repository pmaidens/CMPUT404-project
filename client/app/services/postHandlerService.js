"use strict";

angular.module("myApp.services.postHandler", [
    "ngRoute",
    "myApp.services.urlHandler",
    "myApp.services.authenticationHandler",
    "myApp.services.authorHandler"
])
.service("postHandler", function($q,$http,$route, urlHandler, authenticationHandler, authorHandler) {
    var nodes = [
        {
            "url":"http://floating-sands-69681.herokuapp.com/api/",
            "username":"c404",
            "password":"asdf"
        },{
            "url":"http://cmput404-team4b.herokuapp.com/api/",
            "username": "team6",
            "password":"team6"
        }
    ];

    this.posts = [];
    this.getPosts = function (authorId) {
        return $q(function(resolve, reject) {
            var url;
            if(authorId) {
                url = urlHandler.serviceURL() + "api/author/" + (authorId ? authorId + "/posts/" : "");
            } else {
                url = urlHandler.serviceURL() + "api/posts/" + (authorId ? authorId + "/" : "");//eslint-disable-line no-unused-vars
            }
            $http.defaults.headers.common.Authorization = authenticationHandler.token;
            $http.get(url, {author: authorId}).then(function(result) {
                if(result.data instanceof Array) {
                    authorHandler.getAuthor(authorId).then(function(authorResult) {
                        var author = authorResult.data;
                        result.data.forEach(function(post) {
                            post.author = {
                                id: author.id,
                                host: author.host,
                                displayname: author.displayname,
                                url: author.url,
                                github: author.github
                            };
                        });
                        resolve(result);
                    });
                } else {
                    resolve(result);
                }
            }.bind(this), function(err){
                console.log(err);
                reject(err);
            });
        }.bind(this));
    };
    this.deletePost = function(id) {
        //TODO change the url to the proper url
        //make sure you have the slash at the end
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

    this.commentPost = function(post,urlToPostTo){
        console.log(post);
        console.log("HI" + urlToPostTo);
        var urlToCheck = urlToPostTo.split("/");
        console.log(urlToCheck);
        if(urlToCheck[0] !="http:"){
            urlToCheck.unshift( "http:/" );
        }

        var realUrlToCheck = urlToCheck.join("/");
        console.log(realUrlToCheck);
        var encoded ="";

        var nodes = [
            {
                "url":"http://cmput404-team-4b.herokuapp.com/",
                "username": "team6",
                "password":"team6"
            }
        ];
        nodes.forEach(function(node){

            if (urlToCheck[2] == "cmput404-team-4b.herokuapp.com"){


                encoded = window.btoa(node.username + ":" + node.password);


                $http.defaults.headers.common.Authorization = "Basic " +  encoded;

            }else{

                $http.defaults.headers.common.Authorization = authenticationHandler.token;
            }

        });
        //$http.defaults.headers.common.Authorization = authenticationHandler.token;

        //TODO check  url root against nodes and then grab the username and password encode it then send it over.
        //var
        return $http(
            {
                method:"POST",
                url:realUrlToCheck,
                //url:"http://project-c404.rhcloud.com/api/posts/8e4f11cf-8e3f-4468-9a53-8835a1dd65ac/comments/",
                data:post
            }
        );
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
