/*
 * Controller for login page
 */
angular.module('flocs.user')
.controller('loginCtrl', function($uibModal){

  function openLoginModal() {
    $uibModal.open({
      templateUrl: 'user/login-modal.tpl.html',
      controller: 'loginModalCtrl',
    });
  }
});
