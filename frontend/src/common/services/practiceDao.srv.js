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

  /**
   * Send results of an attempt to server
   */
  function sendingAttemptReport(report) {
    return $http.post('/api/practice/attempt-report', report)
      .then(function(response) {
        return response.data;
      });
  }

});
