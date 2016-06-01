// @ngInject
angular.module('flocs.about')
.controller('aboutCtrl', function($scope, IMAGE_RESOURCES) {
  $scope.imageResources = IMAGE_RESOURCES;
});
