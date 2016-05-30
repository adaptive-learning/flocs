// ngInject
angular.module('flocs.filters')
.filter('secondsToHoursMins', function($filter) {
    return function(seconds) {
      var hours = Math.floor(seconds / 3600);
      var minutes = Math.floor(seconds / 60) % 60;
      if (hours >= 5) {
        return hours + 'h';
      } else if (hours >= 1) {
        return hours + 'h ' + minutes + 'm';
      } else {
        if (minutes === 0 && seconds >= 30) {
          minutes = 1;
        }
        return minutes + 'm';
      }
    };
});
