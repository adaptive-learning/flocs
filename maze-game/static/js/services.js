/* Services */
angular.module('maze-game.services', [])

.service('mazeApiService', function($rootScope) {
    this.run = function() {
      $rootScope.$broadcast('maze:run');
    };
    this.listenRun = function(callback) {
      $rootScope.$on('maze:run', callback)
    };

    this.reset = function() {
      $rootScope.$broadcast('maze:reset');
    };
    this.listenReset = function(callback) {
      $rootScope.$on('maze:reset', callback)
    };

    this.broadcastSuccess = function() {
      $rootScope.$broadcast('maze:success');
    };
    this.listenSuccess = function(callback) {
      $rootScope.$on('maze:success', callback)
    };
});
