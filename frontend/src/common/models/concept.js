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
      icon: 'concept-sequence.svg', // TODO: create icon
    },
    {
      key: 'PROGRAMMING_WHILE',
      icon: 'concept-sequence.svg', // TODO: create icon
    },
    {
      key: 'PROGRAMMING_IF',
      icon: 'concept-sequence.svg', // TODO: create icon
    },
    {
      key: 'PROGRAMMING_LOGIC',
      icon: 'concept-sequence.svg', // TODO: create icon
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
  for (var i=0; i < CONCEPTS_DATA.length; i++) {
    var data = CONCEPTS_DATA[i];
    CONCEPTS[data.key] = new Concept(data);
  }

  function fromKey(key) {
    if (key in CONCEPTS) {
      return CONCEPTS[key];
    } else {
      throw "Unknown concept key: " + key;
    }
  }

  // only publish fromKey builder to disallow creating new concepts
  return {
    fromKey: fromKey,
  };
});
