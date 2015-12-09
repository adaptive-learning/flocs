/**
 * Flocs application module
 */
angular.module('flocs', [
    'templates-app',
    'templates-common',
    'ui.bootstrap',
    'ui.router',
    'flocs.header',
    'flocs.home',
    'flocs.practice',
    'flocs.taskPreview',
    'ngDialog',
    'flocs.user'
])

// routes configuration
.config(['$httpProvider', '$stateProvider', '$locationProvider',
  function($httpProvider, $stateProvider, $locationProvider) {

  // settings for CSRF protection
  // (Django uses different name for CSFR cookie than Angular by default)
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

  /*
  // For any unmatched url, redirect to /404
  $urlRouterProvider.otherwise("/404");
  */

  // States
  $stateProvider
    .state('home', {
      url: '/',
      templateUrl: 'home/home.tpl.html',
      controller: 'homeCtrl'
    })

    .state('task-preview-unset', {
      url: '/task-preview',
      templateUrl: 'task-preview/task-preview.tpl.html',
      controller: 'taskPreviewCtrl'
    })

    .state('task-preview-set', {
      url: '/task-preview/{taskId:int}',
      templateUrl: 'task-preview/task-preview.tpl.html',
      controller: 'taskPreviewCtrl'
    })

    .state('practice', {
      url: '/practice',
      templateUrl: 'practice/practice.tpl.html',
      controller: 'practiceCtrl'
    })

    /*
    .state('login',{
      url: '/login',
      templateUrl: 'login/login.tpl.html',
      controller: 'loginCtrl'
    })

    .state('register',{
      url:'/register',
      templateUrl: 'register/register.tpl.html',
      controller: 'registerCtrl'
    })
    */

    .state('404', {
      url: '*path',
      templateUrl: '404/404.tpl.html'
    });

  // Use URLs without hashes (if the browser supports HTML5 history).
  // Note that we need to omit <base> for svg (e.g. in blockly workspace) to
  // work (https://github.com/angular/angular.js/issues/8934). As the
  // consequence, we should use absolute URLs (otherwise, our app might
  // not work correctly in IE9 according to Angular docs).
  $locationProvider.html5Mode({enabled: true, requireBase: false});


  // --- global (re)definitions ---
  // Date.now() to work with older browsers (e.g. IE8)
  // https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/Date/now
  if (!Date.now) {
    Date.now = function now() { return new Date().getTime(); };
  }

}])

// Main application controller
.controller('appCtrl', ['$scope', function($scope) {
  // global configuration (user, language) functions go here
}])

// Configuration of ngDialog module
.config(['ngDialogProvider', function (ngDialogProvider) {
  ngDialogProvider.setDefaults({
    className: 'ngdialog-theme-default',
    plain: false,
    showClose: true,
    closeByDocument: true,
    closeByEscape: true,
    appendTo: false,
    preCloseCallback: function () {
      console.log('default pre-close callback');
    }
  });
}]);
