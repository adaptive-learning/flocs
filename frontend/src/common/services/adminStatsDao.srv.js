/**
 * Communication with server Statistics API.
 * @ngInject
 */
angular.module('flocs.services')
.factory('adminStatsDao', function ($http, conceptFactory) {

  // public API
  return {
    gettingStatistics: gettingStatistics,
  };

  // private implementation

  function gettingStatistics() {
    return $http.get('/api/stats/admin-stats').then(parseStatistics);
  }

  function parseStatistics(response) {
    var statistics = {
      daily_stats: parseDailyStats(response.data['daily_stats']),
      task_stats: parseTaskStats(response.data['task_stats']),
      concept_stats: parseConceptStats(response.data['concept_stats']),
      block_stats: parseBlockStats(response.data['block_stats']),
      session_stats: parseSessionStats(response.data['session_stats']),
    };
    return statistics;
  }

  function parseDailyStats(daily_stats) {
    var dayStats = [];
    daily_stats.forEach(function(day_stat) {
      dayStats.push({
        'date': day_stat.date,
        'students': day_stat.students,
        'solved_tasks': day_stat.solved_tasks
      });
    });
    return dayStats;
  }

  function parseTaskStats(tasks) {
    var taskStats = [];
    tasks.forEach(function(task_stat) {
      taskStats.push({
        'id': task_stat.id,
        'title': task_stat.title,
        'solved_count': task_stat.solved_count,
        'time_median': task_stat.time_median,
        'concepts': task_stat.concepts.map(conceptFactory.fromKey)
      });
    });
    return taskStats;
  }

  function parseConceptStats(concepts) {
    var conceptStats = [];
    concepts.forEach(function(concept_stat) {
      conceptStats.push({
        'name': concept_stat.name,
        'type': concept_stat.type,
        'num_of_tasks': concept_stat.num_of_tasks,
        'num_of_students': concept_stat.num_of_students,
        'num_of_solved_tasks': concept_stat.num_of_solved_tasks
      });
    });
    return conceptStats;
  }

  function parseBlockStats(blocks) {
    var blockStats = [];
    blocks.forEach(function(block_stat) {
      blockStats.push({
        'name': block_stat.name,
        'num_of_tasks': block_stat.num_of_tasks,
        'num_of_students': block_stat.num_of_students
      });
    });
    return blockStats;
  }

  function parseSessionStats(session_stats) {
    return {
      'length_median': session_stats.length_median,
      'solved_ratio': session_stats.solved_ratio,
      'unfinished': session_stats.unfinished
    };
  }


});
