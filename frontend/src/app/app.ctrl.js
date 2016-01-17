/**
 * Main application controller (controls user, language, etc.).
 * @ngInject
 */
angular.module('flocs')
.controller('appCtrl', function($scope, $translate, blocklyMessages) {
  $scope.setLanguage = function(languageCode) {
    $translate.use(languageCode);
    Blockly.Msg = blocklyMessages[languageCode];
  };
});
