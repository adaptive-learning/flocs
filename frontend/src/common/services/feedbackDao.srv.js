/**
 * Communication with server Feedback API.
 * @ngInject
 */
angular.module('flocs.services')
.factory('feedbackDao', function ($http) {

  var API = {
    sendingFeedback: sendingFeedback,
  };

  function sendingFeedback(feedback) {
    return $http.post('/api/feedback/add', feedback)
      .then(function(response) {
        return response.data;
      });
  }

  return API;
});
