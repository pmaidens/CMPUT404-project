"use strict";

angular.module("myApp.services.postHandler", [
    "ngRoute",
    "myApp.services.urlHandler",
    "myApp.services.authenticationHandler",
    "myApp.services.authorHandler"
])
.service("postHandler", function($q,$http,$route, urlHandler, authenticationHandler, authorHandler) {
    this.posts = [];
    this.getPosts = function (authorId) {
        //TODO change the url to the proper url
        /*if(authorId) {
            var url = urlHandler.serviceURL() + "api/author/" + (authorId || "") + "/posts/";
        } else {
            var url = urlHandler.serviceURL() + "api/posts/" + (authorId || "") + "/";//eslint-disable-line no-unused-vars
        }
        $http.defaults.headers.common.Authorization = authenticationHandler.token;
        return $http.get(url, {author: authorId});*/

        return $q(function(resolve, reject) {
            if(authorId) {
                var url = urlHandler.serviceURL() + "api/author/" + (authorId ? authorId + "/posts/" : "");
            } else {
                var url = urlHandler.serviceURL() + "api/posts/" + (authorId ? authorId + "/" : "");//eslint-disable-line no-unused-vars
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
        $http.defaults.headers.common.Authorization = authenticationHandler.token;
        return $http.post(urlToPostTo, post);

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
        }
        $http.defaults.headers.common.Authorization = authenticationHandler.token;
        return $http.put(urlHandler.serviceURL() + "api/posts/"+post.id + "/", putParameters);
    };

    var STUBgetPosts = {
        "query": "posts",
        "count": 105,
        "size": 50,
        "next": "http://service/author/posts?page=3",
        "previous": "http://service/author/posts?page=1",
        "posts":[
            {
                "title":"A post title about a post about web dev",
                "source":"http://lastplaceigotthisfrom.com/post/yyyyy",
                "origin":"http://whereitcamefrom.com/post/zzzzz",
                "description":"This post discusses stuff -- brief",
                "contentType":"text/plain",
                "content":"Þā wæs on burgum Bēowulf Scyldinga, lēof lēod-cyning, longe þrāge folcum gefrǣge (fæder ellor hwearf, aldor of earde), oð þæt him eft onwōc hēah Healfdene; hēold þenden lifde, gamol and gūð-rēow, glæde Scyldingas. Þǣm fēower bearn forð-gerīmed in worold wōcun, weoroda rǣswan, Heorogār and Hrōðgār and Hālga til; hȳrde ic, þat Elan cwēn Ongenþēowes wæs Heaðoscilfinges heals-gebedde. Þā wæs Hrōðgāre here-spēd gyfen, wīges weorð-mynd, þæt him his wine-māgas georne hȳrdon, oð þæt sēo geogoð gewēox, mago-driht micel. Him on mōd bearn, þæt heal-reced hātan wolde, medo-ærn micel men gewyrcean, þone yldo bearn ǣfre gefrūnon, and þǣr on innan eall gedǣlan geongum and ealdum, swylc him god sealde, būton folc-scare and feorum gumena. Þā ic wīde gefrægn weorc gebannan manigre mǣgðe geond þisne middan-geard, folc-stede frætwan. Him on fyrste gelomp ǣdre mid yldum, þæt hit wearð eal gearo, heal-ærna mǣst; scōp him Heort naman, sē þe his wordes geweald wīde hæfde. Hē bēot ne ālēh, bēagas dǣlde, sinc æt symle. Sele hlīfade hēah and horn-gēap: heaðo-wylma bād, lāðan līges; ne wæs hit lenge þā gēn þæt se ecg-hete āðum-swerian 85 æfter wæl-nīðe wæcnan scolde. Þā se ellen-gǣst earfoðlīce þrāge geþolode, sē þe in þȳstrum bād, þæt hē dōgora gehwām drēam gehȳrde hlūdne in healle; þǣr wæs hearpan swēg, swutol sang scopes. Sægde sē þe cūðe frum-sceaft fīra feorran reccan",
                "author":{
                    "id":"de305d54-75b4-431b-adb2-eb6b9e546013",
                    "host":"http://127.0.0.1:5454/",
                    "displayName":"Lara Croft",
                    "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                    "github": "http://github.com/laracroft"
                },
                "categories":["web","tutorial"],
                "count": 1023,
                "size": 50,
                "next": "http://service/posts/{post_id}/comments",
                "comments":[
                    {
                        "author":{
                            "id":"de305d54-75b4-431b-adb2-eb6b9e546013",
                            "host":"http://127.0.0.1:5454/",
                            "displayName":"Greg Johnson",
                            "url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
                            "github": "http://github.com/gjohnson"
                        },
                        "comment":"Sick Olde English",
                        "contentType":"text/x-markdown",
                        "published":"2015-03-09T13:07:04+00:00",
                        "id":"de305d54-75b4-431b-adb2-eb6b9e546013"
                    }
                ],
                "published":"2015-03-09T13:07:04+00:00",
                "id":"de305d54-75b4-431b-adb2-eb6b9e546013",
                "visibility":"PUBLIC"
            }
        ]
    };
});
