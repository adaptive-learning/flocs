/**
 * Factory for creating Flow instances
 * @ngInject
 */
angular.module('flocs.models')
.constant('FLOWS_DATA', [
    {key: 'UNKNOWN'},
    {key: 'VERY_DIFFICULT'},
    {key: 'DIFFICULT'},
    {key: 'RIGHT'},
    {key: 'EASY'},
])
.factory('flowFactory', function(FLOWS_DATA) {

  function Flow(data) {
    this.key = data.key;
  }

  Flow.prototype.getTranslationKey = function () {
    return 'FLOW.' + this.key;
  };

  // build dictionary of all possible flows
  var FLOWS = {};
  for (var i=0; i < FLOWS_DATA.length; i++) {
    var data = FLOWS_DATA[i];
    FLOWS[data.key] = new Flow(data);
  }

  function flowFromKey(key) {
    if (key in FLOWS) {
      return FLOWS[key];
    } else {
      throw "Unknown flow key: " + key;
    }
  }

  // only publish fromKey builder to disallow creating new flows
  return {
    fromKey: flowFromKey,
  };
});
