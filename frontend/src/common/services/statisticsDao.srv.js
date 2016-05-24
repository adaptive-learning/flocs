/**
 * Communication with server Statistics API.
 * @ngInject
 */
angular.module('flocs.services')
.factory('statisticsDao', function ($http, conceptFactory, flowFactory) {

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
      'blocks': response.data['blocks'].map(parseBlock),
      'finishedTasks': response.data['finished-tasks'].map(parseFinishedTask),
    };
    return statistics;
  }

  function parseBlock(record) {
    console.log('parse block:', record);
    return null;
  }

  function parseFinishedTask(record) {
    var finishedTask = {
      'id': record['task-id'],
      'title': record['title'],
      'credits': record['credits'],
      'concepts': record['concepts'].map(conceptFactory.fromKey),
      'time': record['time'],
      'percentil': record['percentil'],
      'flow': flowFactory.fromKey(record['flow']),
    };
    return finishedTask;
  }

});
