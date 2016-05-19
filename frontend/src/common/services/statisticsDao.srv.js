/**
 * Communication with server Statistics API.
 * @ngInject
 */
angular.module('flocs.services')
.factory('statisticsDao', function ($http) {

  // public API
  return {
    gettingStatistics: gettingStatistics,
  };

  // private implementation

  function gettingStatistics() {
    return $http.get('/api/stats/student-statistics').then(parseStatistics);
  }

  function parseStatistics(response) {
    var statistics = {
      'finishedTasks': response.data['finished-tasks'].map(parseFinishedTask),
    };
    return statistics;
  }

  function parseFinishedTask(record) {
    return {
      'title': record['title'],
      'credits': record['credits'],
      'concepts': record['concepts'],
      'time': record['time'],
      'percentil': record['percentil'],
      'flow': record['flow'],
    };
  }

});
