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
    gettingSessionOverview: gettingSessionOverview,
    sendingAttemptReport: sendingAttemptReport,
    sendingFlowReport: sendingFlowReport,
    sendingGiveUpReport: sendingGiveUpReport,
  };

  // private implementation

  /**
   * Return promise of getting next task instance in current session.
   */
  function gettingNextTask() {
    return $http.get('/api/practice/next-task').then(parseTaskInstance);
  }

  /**
   * Return promise of getting task by given id (in the current session).
   */
  function gettingTaskById(id) {
    return $http.get('/api/practice/task/' + id).then(parseTaskInstance);
  }

  function parseTaskInstance(response) {
    var taskInstance = {
      taskInstanceId: response.data['task-instance-id'],
      task: parseTask(response.data['task']),
      studentToolbox: response.data['student-toolbox'],
      newInstructions: response.data['new-instructions'],
      allInstructions: response.data['all-instructions'],
      session: response.data['session'],
    };
    // hack to pass student toolbox into workspace service easily
    taskInstance.task['workspace-settings'].studentToolbox = taskInstance.studentToolbox;
    return taskInstance;
  }

  function parseTask(response) {
    // TODO: replace hyphen-case for camelCase (on frontend)
    var task = {
      'task-id': response['task-id'],
      'title': response['title'],
      'maze-settings': response['maze-settings'],
      'workspace-settings': parseWorkspaceSettings(response['workspace-settings']),
    };
    return task;
  }

  function parseWorkspaceSettings(response) {
    var workspaceSettings = {
      toolbox: response['toolbox'],
      blocksLimit: response['blocks-limit']
    };
    return workspaceSettings;
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

  function gettingSessionOverview() {
    return $http.get('/api/practice/session-overview').then(parseResponse);

    function parseResponse(response) {
      var sessionOverview = {
        taskInstances: response.data['task-instances'],
        overallTime: response.data['overall-time'],
        percentils: response.data['percentils']
      };
      return sessionOverview;
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
    return $http.post('/api/practice/flow-report', report);
  }
});
