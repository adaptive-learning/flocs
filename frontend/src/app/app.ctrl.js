/**
 * Main application controller (controls user, language, etc.).
 * @ngInject
 */
angular.module('flocs')
.controller('appCtrl', function($scope, $rootScope, $translate, localesService) {
  $scope.setLanguage = function(languageCode) {
    localesService.setLanguage(languageCode);
  };

  $scope.setLanguageDomains = function(languageDomains) {
    localesService.setLanguageDomains(languageDomains);
  };

  $rootScope.$on('$stateChangeSuccess', function(event, toState) {
    $translate('TITLE').then(function(appTranslation) {
      if (toState.data && toState.data.titleTraslationKey) {
        $translate(toState.data.titleTraslationKey).then(function(stateTranslation) {
          $scope.title = stateTranslation + ' | ' + appTranslation;
        });
      } else {
        $scope.title = appTranslation;
      }
    });
  });
});
