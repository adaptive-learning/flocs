var workspace = Blockly.inject('blocklyDiv',
    {media: '../blockly/media/',
     maxBlocks: 10,
     toolbox: toolbox});
     
function onchange() {
      document.getElementById('capacity').innerHTML = workspace.remainingCapacity();
    }

function bindClick(el, func) {
  if (typeof el == 'string') {
    el = document.getElementById(el);
  }
  el.addEventListener('click', func, true);
  el.addEventListener('touchend', func, true);
};

workspace.addChangeListener(onchange);
