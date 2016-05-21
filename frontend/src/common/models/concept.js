/**
 * Factory for creating Concept instances.
 *
 * @ngInject
 */
angular.module('flocs.models')
.constant('CONCEPTS_DATA', [
    {
      key: 'PROGRAMMING_SEQUENCE',
      icon: 'concept-sequence.svg',
    },
    {
      key: 'PROGRAMMING_REPEAT',
      icon: 'concept-repeat.svg',
    },
    {
      key: 'PROGRAMMING_WHILE',
      icon: 'concept-while.svg',
    },
    {
      key: 'PROGRAMMING_IF',
      icon: 'concept-if.svg',
    },
    {
      key: 'PROGRAMMING_LOGIC',
      icon: 'concept-logic.svg',
    },
])
.factory('conceptFactory', function(CONCEPTS_DATA) {

  function Concept(data) {
    this.key = data.key;
    this.icon = data.icon;
  }

  Concept.prototype.getTranslationKey = function () {
    return 'CONCEPT.' + this.key;
  };

  // build dictionary of all used concepts
  var CONCEPTS = {};
  var KEYS = [];
  for (var i=0; i < CONCEPTS_DATA.length; i++) {
    var data = CONCEPTS_DATA[i];
    CONCEPTS[data.key] = new Concept(data);
    KEYS.push(data.key);
  }

  function fromKey(key) {
    if (key in CONCEPTS) {
      return CONCEPTS[key];
    } else {
      throw "Unknown concept key: " + key;
    }
  }

  function all() {
    var allConcepts = [];
    for (var i=0; i < KEYS.length; i++) {
      allConcepts.push(CONCEPTS[KEYS[i]]);
    }
    return allConcepts;
  }

  return {
    fromKey: fromKey,
    all: all,
  };
});
