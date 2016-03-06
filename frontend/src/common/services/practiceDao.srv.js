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
    gettingPracticeDetails: gettingPracticeDetails,
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

  function gettingPracticeDetails() {
    return $http.get('/api/practice/practice-details').then(parseResponse);

    function parseResponse(response) {
      var practiceDetails = {
        totalCredits: response.data['total-credits'],
        freeCredits: response.data['free-credits'],
        solvedTasksCount: response.data['solved-tasks-count'],
        availableBlocks: response.data['available-blocks'],
      };
      return practiceDetails;
    }
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
    report['flow-report'] = flowRatingToNumber(report['flow-report']);
    return $http.post('/api/practice/flow-report', report);
  }

  function flowRatingToNumber(rating) {
    switch (rating) {
      case 'difficult': return 2;
      case 'right': return 3;
      case 'easy': return 4;
      default: throw "Unknown flow rating: " + rating;
    }
  }
});
