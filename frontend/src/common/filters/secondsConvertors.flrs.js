angular.module('flocs.filters')
// ngInject
.filter('secondsToTime', function($filter) {
    return function(seconds) {
        var format = (seconds >= 3600) ? 'H:mm:ss' : "m:ss";
        return $filter('date')(new Date(0, 0, 0).setSeconds(seconds), format);
    };
})
// ngInject
.filter('secondsToHours', function($filter) {
    return function(seconds) {
      var hours = Math.floor(seconds / 3600);
      return hours;
    };
})
// ngInject
.filter('secondsToMins', function($filter) {
    return function(seconds) {
      //var minutes = Math.floor(seconds / 60) % 60;
      var minutes = Math.floor(seconds / 60);
      if (minutes === 0 && seconds >= 30) {
        minutes = 1;
      }
      return minutes;
    };
})
// ngInject
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
