// @ngInject
angular.module('flocs.sessionBar')
.factory('sessionBarService', function() {
  var sessionTasksStatuses = [];

  var API = {
    sessionTasksStatuses: sessionTasksStatuses,
    updateSessionTasksStatutes: updateSessionTasksStatutes,
  };

  function updateSessionTasksStatutes(session) {
    sessionTasksStatuses.length = 0;
    if (!session.active) {
      return;
    }
    for (var i = 1; i <= session.max; i++) {
      var taskStatus = null;
      if (i < session.task) {
        var taskInstance = session.taskInstances[i-1];
        if (taskInstance.solved) {
          taskStatus = 'solved';
        } else {
          taskStatus = 'given-up';
        }
      } else if (i == session.task) {
        taskStatus = 'current';
      } else {
        taskStatus = 'future';
      }
      sessionTasksStatuses.push(taskStatus);
    }
  }

  return API;
});
