/**
 * Factory for creating Block instances.
 *
 * @ngInject
 */
angular.module('flocs.models')
.factory('Block', function() {

  function Block(identifier, name, level, credits) {
    this.identifier = identifier;
    this.name = name;
    this.level = level;
    this.credits = credits;
    this.creditsPaid = 0;
    this.active = false;
    this.purchased = false;
    this.conceptStats = null;
  }

  Block.prototype.setCreditsPaid = function(creditsPaid) {
    this.creditsPaid = creditsPaid;
  };

  Block.prototype.setActive = function(active) {
    this.active = active;
  };

  Block.prototype.setPurchased = function(purchased) {
    this.purchased = purchased;
  };

  Block.prototype.setConceptStats = function(conceptStats) {
    this.conceptStats = conceptStats;
  };

  Block.prototype.getSolvedCount = function() {
    return this.conceptStats.solvedCount;
  };

  Block.prototype.isPassive = function() {
    return (!this.active) && (!this.purchased);
  };

  Block.prototype.isMastered = function() {
    return this.conceptStats.mastered;
  };

  return Block;
});
