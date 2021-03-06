/**
 * Communication with server Statistics API.
 * @ngInject
 */
angular.module('flocs.services')
.factory('statisticsDao', function ($http, conceptFactory, flowFactory, Block) {

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
      overview: parseOverview(response.data['overview']),
      blocks: response.data['blocks'].map(parseBlock),
      finishedTasks: response.data['finished-tasks'].map(parseFinishedTask),
    };
    return statistics;
  }

  function parseOverview(record) {
    var overview = {
      solvedCount: record['solved-count'],
      sessionsCount: record['sessions-count'],
      totalFlowTime: record['total-flow-time'],
      totalCredits: record['total-credits'],
      freeCredits: record['free-credits'],
      blocksCount: record['blocks-count'],
      conceptsCount: record['concepts-count'],
    };
    return overview;
  }

  function parseBlock(record) {
    var block = new Block(
        record['identifier'],
        record['name'],
        record['level'],
        record['credits']);
    block.setCreditsPaid(record['credits-paid']);
    block.setPurchased(record['purchased']);
    block.setActive(record['active']);
    block.setConceptStats(parseConceptStats(record['concept-stats']));
    return block;
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

  function parseConceptStats(record) {
    return {
      identifier: record['identifier'],
      solvedCount: record['solved-count'],
      mastered: record['mastered'],
    };
  }

});
