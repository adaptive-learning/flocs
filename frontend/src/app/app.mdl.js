/**
 * Flocs application module
 */
angular.module('flocs', [
    'templates-app',
    'templates-common',
    'ngAnimate',
    'ui.bootstrap',
    'ui.router',
    'ngDialog',
    'pascalprecht.translate',
    'flocs.locales',
    'flocs.models',
    'flocs.services',
    'flocs.directives',
    'flocs.filters',
    'flocs.header',
    'flocs.footer',
    'flocs.feedback',
    'flocs.home',
    'flocs.practice',
    'flocs.taskPreview',
    'flocs.user',
    'flocs.profile',
    'flocs.statistics',
    'flocs.session-overview',
    'flocs.about',
])

// routes configuration
.config(function($httpProvider, $stateProvider, $locationProvider) {

  // settings for CSRF protection
  // (Django uses different name for CSFR cookie than Angular by default)
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

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

    .state('practice-start', {
      url: '/practice',
      templateUrl: 'practice/practice-start.tpl.html',
      controller: 'practiceStartCtrl',
      data: {
          titleTraslationKey: 'PRACTICE'
      }
    })

    .state('practice-task', {
      url: '/practice/task/{taskId:int}',
      templateUrl: 'practice/practice.tpl.html',
      controller: 'practiceCtrl',
      data: {
          titleTraslationKey: 'PRACTICE'
      }
    })

    .state('profile', {
      url: '/profile',
      templateUrl: 'profile/profile.tpl.html',
      controller: 'profileCtrl',
      data: {
          titleTraslationKey: 'PROFILE'
      }
    })

    .state('statistics', {
      url: '/statistics',
      templateUrl: 'statistics/statistics.tpl.html',
      controller: 'statisticsCtrl',
      data: {
          titleTraslationKey: 'STATISTICS_PAGE.TITLE'
      }
    })

    .state('session-overview', {
      url: '/session-overview',
      templateUrl: 'session-overview/session-overview.tpl.html',
      controller: 'session-overviewCtrl',
      data: {
          titleTraslationKey: 'SESSION_OVERVIEW'
      }
    })

    .state('about', {
      url: '/about',
      templateUrl: 'about/about.tpl.html',
      data: {
          titleTraslationKey: 'ABOUT'
      }
    })

    .state('404', {
      url: '/*path',
      templateUrl: '404/404.tpl.html'
    });

  // Use URLs without hashes (if the browser supports HTML5 history).
  // Note that we need to omit <base> for svg (e.g. in blockly workspace) to
  // work (https://github.com/angular/angular.js/issues/8934). As the
  // consequence, we should use absolute URLs (otherwise, our app might
  // not work correctly in IE9 according to Angular docs).
  $locationProvider.html5Mode({enabled: true, requireBase: false});
})

// localization
.config(function($translateProvider, localeEn, localeCs) {
  $translateProvider.useMessageFormatInterpolation();
  $translateProvider.useSanitizeValueStrategy('escapeParameters');
    // NOTE: If requested, it's possible to sanitize parameters or the
    // complete translation (needs angular-sanitize as a dependency,
    // see http://angular-translate.github.io/docs/#/guide/19_security).
  $translateProvider.translations('en', localeEn);
  $translateProvider.translations('cs', localeCs);
  $translateProvider.preferredLanguage('en');  // overridden by ng-init in index.html
})

// global (re)definitions
.config(function() {
  // Date.now() to work with older browsers (e.g. IE8)
  // https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/Date/now
  if (!Date.now) {
    Date.now = function now() { return new Date().getTime(); };
  }
})

// Configuration of ngDialog module
.config(function (ngDialogProvider) {
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
});
