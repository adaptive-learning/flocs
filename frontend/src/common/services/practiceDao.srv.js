/*
 * Communication with server Practice API.
 */
angular.module('flocs.services')
.factory('practiceDao', ['$http', function ($http) {

  // public API
  return {
    gettingNextTask: gettingNextTask,
    sendingAttemptReport: sendingAttemptReport,
  };

  // private implementation

  /**
   * Return promise of getting next task instance in current session.
   */
  function gettingNextTask() {
    return $http.get('api/practice/next-task')
      .then(function(response) {
        return response.data;
      });
  }

  /**
   * Send results of an attempt to server
   */
  function sendingAttemptReport(report) {
    $http.post('api/practice/attempt-report', report);
  }

}]);
