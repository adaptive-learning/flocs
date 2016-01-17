/**
 * Main application controller (controls user, language, etc.).
 * @ngInject
 */
angular.module('flocs')
.controller('appCtrl', function($scope, $translate) {
  $scope.setLanguage = function(languageCode) {
    $translate.use(languageCode);
    // TODO: Blockly.Msg = neco v zavislosti na language_code
  };
});
