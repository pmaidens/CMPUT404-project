"use strict";

angular.module("myApp.postStream", [
    "ngRoute",
    "myApp.services.postHandler",
    "myApp.services.authenticationHandler",
    "myApp.services.urlHandler"
])

.config(["$routeProvider", function($routeProvider) {
    $routeProvider.when("/stream", {
        templateUrl: "partials/postStream.html",
        controller: "PostStreamController"
    });
}])

.controller("PostStreamController", function($scope, $http, $location ,postHandler, authenticationHandler, urlHandler) {
    var targetAuthor, targetAuthorId;
    $scope.user = authenticationHandler.user;

    $scope.posts = [];
    $scope.allPost = [];



    var getNodes = function(){

	//CHANGE USERNAME AND PASSWORD TO A REAL ONE.
	//var credentials = window.btoa('username:password');


	//USE THIS IF WE NEED BASIC AUTH TO GET /api/nodes
	$http.defaults.headers.common.Authorization = authenticationHandler.token;
	
	//TODO change the url
	$http.get('http://localhost:8000/api/nodes/' ).then(function(result){

	    $scope.nodes = result.data;


	});
    };

    //TODO CHANGE THESE FAKE NODES TO REAL NODES
    //comment this out when $scope.nodes is being set
    var nodes = [{'url':'http://cmput404-team-4b.herokuapp.com/api/' , 'username': 'team6', 'password':'team6' }];
    


    var getNodePosts = function(nodes){
	
	$scope.nodePosts = [];
	var encoded = '';

	for (var i=0; i < nodes.length ; i++){
	    //console.log(nodes);
	    
	  
		encoded = window.btoa( nodes[i].username + ':' + nodes[i].password);

	    $http.defaults.headers.common.Authorization = 'Basic ' + encoded; 
	    $http.defaults.useXDomain=true;
	    var posts = '';
	    if (nodes[i].url=="http://floating-sands-69681.herokuapp.com/api/"){
		posts = 'posts';
	    }else{
		posts = 'posts/'
	    }
	    $http({

		method:'GET',
		url: nodes[i].url+posts,
		headers:{
		    

		}
		

	    }).then(function(result){

		console.log('i should be here');

		//$scope.nodePosts.push(result.data.posts);
		result.data.posts.forEach(function(post){

		    $scope.nodePosts.push(post)

		});
		

		$scope.nodePosts.forEach(function(post){


		    $scope.allPost.push(post);

		});

		

		
		//console.log($scope.nodePosts);

	    },function(err){
		console.log(err);

	    });
	    

	}

    }
    
    //TODO
    //CHANGE nodes TO $scope.nodes
    getNodes();
    getNodePosts(nodes);
 

    // If something else tells us what authorId to use, then
    // we know that we should load the posts of that user.
    // Otherwise, we should just load all the posts the current
    // signed in user can see.
    if($scope.postStream && $scope.postStream.authorId) {
        targetAuthor = {id: $scope.postStream.authorId};
        targetAuthorId = targetAuthor.id;
    }
    postHandler.getPosts(targetAuthorId).then(function(result) {


    	if($location.url() ==='/profile'){
    	    result.data.posts = result.data.posts.filter(function(post){
        		return post.author.id === authenticationHandler.user.id;
    	    });
    	}

	$scope.allPost = $scope.allPost.concat(result.data.posts);
        //$scope.posts = result.data.posts || result.data;

        loadGit();
    });

    // Make a http call to the github api to get all user information
    // associated with the git_username

    var loadGit = function () {
	//change $scope.git_username to the author's github user name

	var gitHubURL = $scope.user.github;
	

	if(gitHubURL){
        $scope.git_username = gitHubURL.substring(gitHubURL.lastIndexOf('/')+1);
            $http({method: 'GET', url:"https://api.github.com/users/"+$scope.git_username , headers:{'Authorization':undefined}}).success(function(gitdata){


	        $scope.gitUserData = gitdata;
                loadEvents();


	    });
	} else {

            $scope.posts.forEach(function(post){
		
		$scope.allPost.push(post);
		

	    });
	
    }

    };
    // Http call for github repos (not too sure what Abram means by "activity")
    // ** May need to make additional calls

    var loadEvents = function () {
        $http({method:'GET', url: "https://api.github.com/users/"+$scope.git_username+"/events" , headers:{'Authorization':undefined}})
            .success(function(event_data){
                $scope.eventData = event_data;
             
                //$scope.allPost = $scope.posts.concat($scope.eventData);
		$scope.eventData.forEach(function(eventData){

		    $scope.allPost.push(eventData);

		});
                
            });
    };

    $scope.deletePost = function(post) {
        post.disabled = true;
        postHandler.deletePost(post.id).then(function(result) {
			//postHandlerService should reload the page


        });
    };

    $scope.editPost = function (post) {
        post.editMode = true;
    };

    $scope.submitPost = function (post) {
        postHandler.updatePost(post);
        post.editMode = false;
       
    };

    
//localhost/api/posts/{postid}/comments

//POST : author id, comment, postid
    $scope.AddComment = function (post, comments) {
	var date = new Date();

//	var urlToComment = post.author.host + 'api/posts/' + post.id + '/comments/';
	var appendCheck = post.author.host.split('/');
	var toAppend = '';
	if(appendCheck[appendCheck.length-1]!='api'){

	    toAppend = 'api';
	}
	console.log(post.id);
	var urlToComment = post.author.host + toAppend + '/posts/' + post.id + '/comments/';
	console.log(urlToComment);
	var commentAuthor = authenticationHandler.user;
	var DisplayName = commentAuthor.displayname;
	commentAuthor['displayName'] = DisplayName;
        postHandler.commentPost({
            author: commentAuthor,
            comment: comments,
	    //we need to allow different contenttypes for comments
	    contentType: 'text/plain'//,
	   // published: date,
	   //id
        },urlToComment).then(function(){
	    
	    comments = '';
	    
	    //TODO
	    
	    $http.get(urlHandler.serviceURL()+'api/posts/'+post.id+'/').then(function(postData){


		post.comments = postData.data.comments;

	    });

	});
    };
});
