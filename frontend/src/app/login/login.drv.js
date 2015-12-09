/*
 * Directive for login formular
 */
angular.module('flocs.user')
.directive('loginForm', function(){
	return{
		restrict:'EA',
		templateUrl: 'login/login.tpl.html'
	};
});
