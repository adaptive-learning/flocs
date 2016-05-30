angular.module('flocs.directives')
.directive('flocsBlockPreview', function($timeout, $window) {
  return {
    restrict: 'E',

    scope: {
      block: '=',  // models.Block
      visible: '@',  // this is just a flag to notify about visibility changes
    },

    template: '<div class="blockly-single-block"></div>',

    controller: function($scope){
    },

    link: function(scope, element, attrs) {
      // inject Blockly
      var blocklyDiv = element[0].querySelector('.blockly-single-block');
      var blockly = Blockly.inject(blocklyDiv, {readOnly: true});
      var block = null;

      function createBlockInCenter() {
        block = Blockly.Block.obtain(blockly, scope.block.identifier);
        block.initSvg();
        block.render();
        centerBlock(block);
      }

      function centerBlock(block) {
        var blockSize = block.getHeightWidth();
        var target_x = (blocklyDiv.offsetWidth - blockSize.width) / 2;
        var target_y = (blocklyDiv.offsetHeight - blockSize.height) / 2;
        var current = block.getRelativeToSurfaceXY();
        block.moveBy(target_x - current.x, target_y - current.y);
      }

      scope.$watch('visible', function() {
        $timeout(createBlockInCenter);
      });

      angular.element($window).bind('resize', function() {
        if (block !== null) {
          centerBlock(block);
        }
      });

    }
  };
});
