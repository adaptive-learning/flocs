/**
 * Factory for creating Flow instances
 * @ngInject
 */
angular.module('flocs.models')
.constant('FLOWS_DATA', [
    {key: 'UNKNOWN', value: null},
    {key: 'VERY_DIFFICULT', value: -1},
    {key: 'DIFFICULT', value: -1},
    {key: 'RIGHT', value: 0},
    {key: 'EASY', value: 1},
])
.factory('flowFactory', function(FLOWS_DATA) {

  function Flow(data) {
    this.key = data.key;
    this.value = data.value;
  }

  Flow.prototype.getTranslationKey = function() {
    return 'FLOW.' + this.key;
  };

  /**
   * Return normalized flow value (-1 difficilt, 0 right, 1 easy)
   */
  Flow.prototype.getFlowValue = function() {
    return this.value;
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

  /**
   * Return color corresponding to normalized flow value
   * -1 -> red
   *  0 -> green
   * +1 -> blue
   */
  function valueToColor(value) {
      var hue = (value + 1) * 120;
      return 'hsl(' + hue + ',100%, 50%)';
  }

  // only publish fromKey builder to disallow creating new flows
  return {
    fromKey: flowFromKey,
    valueToColor: valueToColor,
  };
});
