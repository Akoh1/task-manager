angular.module('myApp').controller('myAppCtrl', function ($scope, $http) {

    $http.get('/api/goals/?format=json').then(function (response) {
        $scope.goal = response.data;
    });

    $http.get('/api/users/?format=json').then(function (response) {
        $scope.user = response.data;

    });
    $http.get('/api/status/?format=json').then(function (response) {
        $scope.status = response.data;

    });

    $scope.onDrop = function(data, evt){
        console.log("drop success data:", data);
        console.log("drop success event:", evt);
    };

});

angular.module('myApp').config(function ($routeProvider) {

    $routeProvider.when('/taskurl/', {template : "<form ng-controller='formCtrl'>"  +
    "<p>task:<input type='text' ng-model='myTask' value=''></p>" +
            "<p>user: <select ng-model='myName'><option ng-repeat='user in user' ng-value='user.url'>{{user.username}}</option></select></p> " +
            "<p>status: <select ng-model='myStatus'><option ng-repeat='statu in status' ng-value='statu.url'>{{statu.target}}</option></select></p>" +
            "<input type='submit' value='add task' ng-click='postData()'>" +
        "</form>" })
        .when('/userurl/', {template :
           "<form  ng-controller='formCtrl'>" + "<p>name:<input type='text' ng-model='myUser' value='' required=''></p>" +
            "<input type='submit' value='add user' ng-click='postUser()'>" +
        "</form>"  });
});


angular.module('myApp').controller('formCtrl', function ($scope, $http) {

    $scope.postData = function () {

          $http({
              url : "http://127.0.0.1:8000/api/goals/",
              method: "POST",
              data : {
                task : $scope.myTask,
                target_name : $scope.myStatus,
                user_name : $scope.myName
            },
              headers : {'Content-Type' : 'application/json'}

          }).then(function onSuccess(response) {

              console.log(response);

          }).catch(function onError(error) {
              console.log(error);

          });

    };

    $scope.postUser = function () {

          $http({
              url : "http://127.0.0.1:8000/api/users/",
              method: "POST",

              data : {
                username : $scope.myUser
            },
              headers :  {'Content-Type' : 'application/json', 'Accept':'application/json'}

          }).then(function onSuccess(response) {
              console.log(response);
          }).catch(function onError(error) {
              console.log(error);

          });
    };

});

