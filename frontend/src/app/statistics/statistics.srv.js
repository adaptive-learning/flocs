// @ngInject
angular.module('flocs.statistics')
.factory('statisticsService', function (statisticsDao) {

  // === public API ===
  return {
    gettingStatistics: gettingStatistics,
  };


  // === implementation ===

  function gettingStatistics() {
    return statisticsDao.gettingStatistics();
  }

});
