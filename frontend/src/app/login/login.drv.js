/*
 * Directive for login formular
 */
angular.module('flocs.user')
.directive('loginForm', function(){
	return{
		restrict:'EA',
		template:
		    '<div>'	+
			'<form ng-submit="send()" ng-controller="loginCtrl">' +
			'<input type="text" placeholder="Username" /><br/>' +
			'<input type="password" placeholder="Password"/><br/>' +
			'<input type="submit" value="LogIn" />' +
			'<a href="/register">Create profile</a><br/>' +
			'</form>' +
			'</div>'
	};
});
