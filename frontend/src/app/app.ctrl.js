/**
 * Main application controller (controls user, language, etc.).
 * @ngInject
 */
angular.module('flocs')
.controller('appCtrl', function($scope, $translate) {
  $scope.setLanguage = function(languageCode) {
    $translate.use(languageCode);
  };
});
