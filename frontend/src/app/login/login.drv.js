/*
 * Directive for login formular
 */
angular.module('flocs.user')
.directive('loginForm', function(){
	return{
		restrict:'EA',
		template:
		    '<div ng-app="flocs.user">'	+
            '<div ng-if="!user">' +
            'user: {{user}}' +
			'<form ng-submit="send()" ng-controller="loginCtrl">' +
			'<input type="text" ng-model="username" placeholder="Username" /><br/>' +
			'<input type="password" ng-model="password" placeholder="Password"/><br/>' +
			'<input type="submit" value="LogIn" />' +
			'<a href="/register">Create profile</a><br/>' +
			'</form>' +
            '</div>' +
            '<div ng-if="user">' +
            'user: {{user}}' +
            '</div>' +
			'</div>'
	};
});
