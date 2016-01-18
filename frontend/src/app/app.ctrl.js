/**
 * Main application controller (controls user, language, etc.).
 * @ngInject
 */
angular.module('flocs')
.controller('appCtrl', function($scope, localesService) {
  $scope.setLanguage = function(languageCode) {
    localesService.setLanguage(languageCode);
  };

  $scope.setLanguageDomains = function(languageDomains) {
    localesService.setLanguageDomains(languageDomains);
  };
});
