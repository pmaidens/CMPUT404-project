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
    //console.log($scope.user);
    $scope.posts = [];
    $scope.allPost = [];



    var getNodes = function(){

	//CHANGE USERNAME AND PASSWORD TO A REAL ONE.
	//var credentials = window.btoa('username:password');


	//USE THIS IF WE NEED BASIC AUTH TO GET /api/nodes
	$http.defaults.headers.common.Authorization = authenticationHandler.token;
	
	//TODO change the url
	$http.get('http://localhost:8000/api/nodes/' ).then(function(result){

	    console.log(result.data);
	    $scope.nodes = result.data;


	});
    };

    //TODO CHANGE THESE FAKE NODES TO REAL NODES
    //comment this out when $scope.nodes is being set
    var nodes = [{'url':'http://floating-sands-69681.herokuapp.com/api/','username':'c404','password':'asdf'},{'url':'http://cmput404team4b.herokuapp.com/api/' , 'username': 'team6', 'password':'team6' }];
    


    var getNodePosts = function(nodes){
	
	$scope.nodePosts = [];
	var encoded = '';

	for (var i=0; i < nodes.length ; i++){
	    //console.log(nodes);
	    
	    //TODO CHANGE encoded SO THAT IT MATCHES WHAT EACH GROUP WANTS.
	    if (nodes[i].url =='http://cmput404teamb.herokuapp.com/api'){


		encoded = window.btoa('team6@' + nodes[i].username + ':' + nodes[i].password);

	    }
	    else{
		encoded = window.btoa('team6@'+ nodes[i].username + ':' + nodes[i].password);


	    }
	    $http.defaults.headers.common.Authorization = 'Basic ' + encoded; 
	    $http.defaults.useXDomain=true;
	    $http({

		method:'GET',
		url: nodes[i].url+'posts/',
		headers:{
		    

		}
		

	    }).then(function(result){



		//$scope.nodePosts.push(result.data.posts);
		result.data.posts.forEach(function(post){
		    console.log(post);
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
	console.log('YOOO LET ME GRAB MY OWN POSTS');
	$scope.allPost = $scope.allPost.concat(result.data.posts);
        //$scope.posts = result.data.posts || result.data;
	//console.log($scope.posts);
        loadGit();
    });

    // Make a http call to the github api to get all user information
    // associated with the git_username

    var loadGit = function () {
	//change $scope.git_username to the author's github user name
	
	console.log($scope.user.github);
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
	    console.log($scope.allPost);
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
                console.log($scope.allPost);
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
	var urlToComment = post.author.host + 'api/posts/' + post.id + '/comments/';
        postHandler.commentPost({
            //author: authenticationHandler.user,
            comment: comments,
	    //we need to allow different contenttypes for comments
	    contentType: 'text/plain'//,
	   // published: date,
	   //id
        },urlToComment).then(function(){
	    
	    comments = '';
	    
	    //TODO
	    
	    $http.get(urlHandler.serviceURL()+'api/posts/'+post.id+'/').then(function(postData){


		console.log("POST STUFF BELOW");
		console.log(postData);
		post.comments = postData.data.comments;

	    });

	});
    };
});
