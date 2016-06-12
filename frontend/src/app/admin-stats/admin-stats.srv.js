// @ngInject
angular.module('flocs.admin-stats')
.factory('adminStatsService', function (adminStatsDao) {

  // === public API ===
  return {
    gettingStatistics: gettingStatistics,
  };


  // === implementation ===

  function gettingStatistics() {
    return adminStatsDao.gettingStatistics();
  }

});
