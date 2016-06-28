/*
 * Http error controller
 */
angular.module('flocs.httpErrors')
.controller('httpErrorsCtrl', function($scope, $stateParams) {
  $scope.event= $stateParams.event;

});
