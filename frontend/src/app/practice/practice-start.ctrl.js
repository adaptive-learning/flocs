// @ngInject
angular.module('flocs.practice')
.controller('practiceStartCtrl', function ($scope, practiceService) {
  $scope.taskLoading = true;
  practiceService.settingNextTask();
});
