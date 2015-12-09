/*
 * Controller for login form
 */
angular.module('flocs.user',[])
.controller('loginCtrl',['$scope','$location', '$log', '$state', 'userDao',
	function($scope,$location, $log, $state ,userDao){
        $scope.loginForm = {};
        $scope.model = {
            username: undefined,
            password: undefined
        };
        $scope.user = {username: undefined};
        userDao.loggedIn().then(function(response){
            $scope.user = {username:response.data.username};
        });
		function login(){
			var username = $scope.model.username;
			var passwd = $scope.model.password;
            userDao.login(username, passwd)
                .then(function(response){
			        if (response.data.loggedIn  == 1){
                        $scope.errormsg = "";
                        $state.go($state.current, {}, {reload: true}); 
        			}else{
                        $log.log(response.data.msg);
                        $scope.errormsg = "Zadali jste špatné údaje!";
			        }
                });

		}
        function logout(){
            userDao.logout().then(function(response){
                $state.go($state.current, {}, {reload: true}); 
            });
        }
    $scope.login = login;
    $scope.logout = logout;
}]);

