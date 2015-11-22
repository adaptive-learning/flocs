/*
 * Controller for login form
 */
angular.module('flocs.user',[])
.controller('loginCtrl',['$scope','$location', '$log','userDao',
	function($scope,$location, $log,userDao){
        userDao.loggedIn().then(function(response){
            $scope.user = response.data.username;
        });
		function send(){
			var username = $scope['username'];
            $log.log($scope['username']);
			var passwd = $scope['password'];
            userDao.login(username, passwd)
                .then(function(response){
                    $log.log(response);
			        if (response.data.loggedIn  == 1){
				        $location.url(".");
        			}else{
                        $log.log(response.data.msg);
		        		$location.url("/403.html");
			        }
                });

		}
    $scope.send = send;
}]);

