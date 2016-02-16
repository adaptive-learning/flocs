/**
 * Communication with server Practice API.
 * @ngInject
 */
angular.module('flocs.services')
.factory('practiceDao', function ($http) {

  // public API
  return {
    gettingNextTask: gettingNextTask,
    gettingTaskById: gettingTaskById,
    sendingAttemptReport: sendingAttemptReport,
    sendingFlowReport: sendingFlowReport,
    sendingGiveUpReport: sendingGiveUpReport,
  };

  // private implementation

  /**
   * Return promise of getting next task instance in current session.
   */
  function gettingNextTask() {
    return $http.get('/api/practice/next-task')
      .then(function(response) {
        return response.data;
      });
  }

  /**
   * Return promise of getting task by given id (in the current session).
   */
  function gettingTaskById(id) {
    return $http.get('/api/practice/task/' + id)
      .then(function(response) {
        return response.data;
      });
  }

  function sendingAttemptReport(report) {
    return $http.post('/api/practice/attempt-report', report)
      .then(function(response) {
        return response.data;
      });
  }

  function sendingGiveUpReport(report) {
    return $http.post('/api/practice/giveup-report', report);
  }

  function sendingFlowReport(report) {
    return $http.post('/api/practice/flow-report', report);
  }
});
