/*
 * Data Access Object for Tasks.
 */
angular.module('flocs.services')
.factory('taskDao', ['$http', function ($http) {

  // public API
  return {
    gettingAllTaskIds: gettingAllTaskIds,
    gettingTaskById: gettingTaskById,
    gettingNextTask: gettingNextTask,
  };

  // private implementation

  /**
   * Return promise of getting list of ids of all tasks.
   */
  function gettingAllTaskIds() {
    return $http.get('api/tasks/get-ids')
      .then(function(response) {
        return response.data.ids;
      });
  }

  /**
   * Return promise of getting task by given id.
   */
  function gettingTaskById(id) {
    return $http.get('api/tasks/get-task/' + id)
      .then(function(response) {
        return response.data;
      });
  }

  /**
   * Return promise of getting next task in current session.
   */
  function gettingNextTask() {
    return $http.get('api/practice/next-task')
      .then(function(response) {
        return response.data;
      });
  }

}]);
