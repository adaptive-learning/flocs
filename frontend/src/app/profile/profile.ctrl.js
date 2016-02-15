/*
 * Profile controller
 */
angular.module('flocs.profile')
.controller('profileCtrl', function($scope, userService) {
  $scope.data = {
    details: null
  };

  userService.getUserDetails()
    .then(function(details){
      $scope.data.details = details.data;
    });
});
