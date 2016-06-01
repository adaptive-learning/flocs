angular.module('flocs.statistics')
.directive('flocsOverviewBlock', function() {
  return {
    restrict: 'E',
    scope: {
      section: '@',
      icon: '@',
      count: '@',
      labelTranslationKey: '@',
    },

    templateUrl: 'statistics/overview-block.tpl.html',

    controller: function($scope){
    },

    link: function(scope, element, attrs) {
    }
  };
});
