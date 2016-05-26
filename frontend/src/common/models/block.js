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

  Block.prototype.isPassive = function() {
    return (!this.active) && (!this.purchased);
  };

  return Block;
});
