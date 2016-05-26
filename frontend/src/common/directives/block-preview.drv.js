angular.module('flocs.directives')
.directive('flocsBlockPreview', function($timeout) {
  return {
    restrict: 'E',

    scope: {
      block: '=',  // models.Block
    },

    template: '<div class="blockly-single-block"></div>',

    controller: function($scope){
    },

    link: function(scope, element, attrs) {
      // inject Blockly
      var blocklyDiv = element[0].querySelector('.blockly-single-block');
      var blockly = Blockly.inject(blocklyDiv, {readOnly: true});

      // create new block
      var block = Blockly.Block.obtain(blockly, scope.block.identifier);
      block.initSvg();
      block.render();

      // put it to center
      var blockSize = block.getHeightWidth();
      var x = (blocklyDiv.offsetWidth - blockSize.width) / 2;
      var y = (blocklyDiv.offsetHeight - blockSize.height) / 2;
      block.moveBy(x, y);
    }
  };
});
