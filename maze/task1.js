var maze = [['x','x','x','x'],
            ['x','x','x','x'],
            ['s','o','o','t'],
            ['x','x','x','x']];

var startDirection = {
    x:0,
    y:1
};

var startPosition = {
    x:2,
    y:0
}

var direction;
var position; 
var endCondition;
var win;

function restartGame() {
    removeFigure();
    position = startPosition; 
    direction = startDirection;
    addFigure();
    endCondition = false;
    win = false;
}

restartGame();

function removeFigure() {
    if (typeof position === 'undefined' || typeof direction === 'undefined') {
        return;
    }

    document.getElementById(position.x + '' + position.y).innerHTML = ''; 
}

function addFigure() {
    if (typeof position === 'undefined' || typeof direction === 'undefined') {
        return;
    }

    var symbol;

    if (direction.x == 0 && direction.y == 1) {
        symbol = '⇒';
    } else if (direction.x == 0 && direction.y == -1) {
        symbol = '⇐';
    } else if (direction.x == 1 && direction.y == 0) {
        symbol = '⇓';
    } else if (direction.x == -1 && direction.y == 0) {
        symbol = '⇑';
    }
    document.getElementById(position.x + '' + position.y).innerHTML = symbol;
}

addFigure();

function colourCells() {
 for (i = 0; i < 4; i++) {
     for (j = 0; j < 4; j++) {
        switch (maze[i][j]) {
            case 'x':
                document.getElementById(i + '' + j).style.backgroundColor = '#AAAAAA'
                break;
            case 't':
                document.getElementById(i + '' + j).style.backgroundColor = '#00FF00'
                break;
            default:
                document.getElementById(i + '' + j).style.backgroundColor = '#FFFFFF'
                break;
        }
     }
 }    
}

colourCells();


function stepForward() {
    removeFigure();

    newPosition = {
        x:position.x + direction.x,
        y:position.y + direction.y 
    };

    position = newPosition;
    addFigure();
    
    switch (maze[position.x][position.y]) {
        case 'x':
            endCondition = true;
            break;
        case 't':
            endCondition = true;
            win = true;
            break;
    } 
}

function stepBackward() {
    removeFigure();

    newPosition = {
        x:position.x - direction.x,
        y:position.y - direction.y 
    };

    position = newPosition;
    addFigure();
    
    switch (maze[position.x][position.y]) {
        case 'x':
            endCondition = true;
            break;
        case 't':
            endCondition = true;
            win = true;
            break;
    } 
}

function getLeftVector() {
    if (direction.x == 0 && direction.y == 1) {
        return {x:-1, y:0}
    } else if (direction.x == 0 && direction.y == -1) {
        return {x:1, y:0}
    } else if (direction.x == 1 && direction.y == 0) {
        return {x:0, y:1}
    } else if (direction.x == -1 && direction.y == 0) {
        return {x:0, y:-1}
    }
}

function getRightVector() {
    if (direction.x == 0 && direction.y == 1) {
        return {x:1, y:0}
    } else if (direction.x == 0 && direction.y == -1) {
        return {x:-1, y:0}
    } else if (direction.x == 1 && direction.y == 0) {
        return {x:0, y:-1}
    } else if (direction.x == -1 && direction.y == 0) {
        return {x:0, y:1}
    }
}

function checkLeft() {
    leftVector = getLeftVector();

    checkPosition = {
        x:position.x + leftVector.x,
        y:position.y + leftVector.y 
    };

    if (checkPosition.x < 0 
            || checkPosition.y < 0
            || checkPosition.x > maze.lenght
            || checkPosition.y > maze[0].lenght) {
        return false;
    }

    switch (maze[checkPosition.x][checkPosition.y]) {
        case 'x':
            return false;
            break;
        default:
            return true;
            break;
    } 
}

function checkRight() {
    rightVector = getRightVector();

    checkPosition = {
        x:position.x + rightVector.x,
        y:position.y + rightVector.y 
    };

    if (checkPosition.x < 0 
            || checkPosition.y < 0
            || checkPosition.x > maze.lenght
            || checkPosition.y > maze[0].lenght) {
        return false;
    }

    switch (maze[checkPosition.x][checkPosition.y]) {
        case 'x':
            return false;
            break;
        default:
            return true;
            break;
    } 
}

function turnLeft() {
    removeFigure();
    direction = getLeftVector();
    addFigure();
}

function turnRight() {
    removeFigure();
    direction = getRightVector();
    addFigure();
}

function announceResult() {
    if (win) {
        alert('Vyřešili jste úlohu správně!');
    } else {
        alert('Bouhžel jste úlohu nevyřešili, zkuste to ještě jednou.');
    }
}

document.getElementById('stepButton').disabled = 'disabled';
document.getElementById('runButton').disabled = 'disabled';

    var myInterpreter = null;

    function initApi(interpreter, scope) {
      // Add an API function for the alert() block.
      var wrapper = function(text) {
        text = text ? text.toString() : '';
        return interpreter.createPrimitive(alert(text));
      };
      interpreter.setProperty(scope, 'alert',
          interpreter.createNativeFunction(wrapper));

      // Add an API function for the prompt() block.
      var wrapper = function(text) {
        text = text ? text.toString() : '';
        return interpreter.createPrimitive(prompt(text));
      };
      interpreter.setProperty(scope, 'prompt',
          interpreter.createNativeFunction(wrapper));

      // Add an API function for highlighting blocks.
      var wrapper = function(id) {
        id = id ? id.toString() : '';
        return interpreter.createPrimitive(highlightBlock(id));
      };
      interpreter.setProperty(scope, 'highlightBlock',
          interpreter.createNativeFunction(wrapper));
          
      // Add an API function for the stepForward() block.
      interpreter.setProperty(scope, 'stepForward',
          interpreter.createNativeFunction(stepForward));
      // Add an API function for the stepBackward() block.
      interpreter.setProperty(scope, 'stepBackward',
          interpreter.createNativeFunction(stepBackward));
      // Add an API function for the checkLeft() block.
      interpreter.setProperty(scope, 'checkLeft',
          interpreter.createNativeFunction(checkLeft));
      // Add an API function for the checkRight() block.
      interpreter.setProperty(scope, 'checkRight',
          interpreter.createNativeFunction(checkRight));
      // Add an API function for the turnLeft() block.
      interpreter.setProperty(scope, 'turnLeft',
          interpreter.createNativeFunction(turnLeft));
      // Add an API function for the turnRight() block.
      interpreter.setProperty(scope, 'turnRight',
          interpreter.createNativeFunction(turnRight));
    }

    var highlightPause = false;

    function highlightBlock(id) {
      workspace.highlightBlock(id);
      highlightPause = true;
    }

    function parseCode() {
      // Generate JavaScript code and parse it.
      Blockly.JavaScript.STATEMENT_PREFIX = 'highlightBlock(%1);\n';
      Blockly.JavaScript.addReservedWords('highlightBlock');
      var code = Blockly.JavaScript.workspaceToCode(workspace);
      myInterpreter = new Interpreter(code, initApi);

      alert('Ready to execute this code:\n\n' + code);
      document.getElementById('stepButton').disabled = '';
      document.getElementById('runButton').disabled = '';
      restartGame();
      highlightPause = false;
      workspace.traceOn(true);
      workspace.highlightBlock(null);
    }

    function stepCode() {
      try {
        var ok = myInterpreter.step();
      } finally {
        if (!ok) {
          // Program complete, no more code to execute.
          document.getElementById('stepButton').disabled = 'disabled';
          document.getElementById('runButton').disabled = 'disabled';
          announceResult();
          return;
        }
      }
      if (highlightPause) {
        // A block has been highlighted.  Pause execution here.
        highlightPause = false;
      } else {
        // Keep executing until a highlight statement is reached.
        stepCode();
      }
    }

function runCode() {
    while (!endCondition) {
    try {
        var ok = myInterpreter.step();
      } finally {
        if (!ok) {
          // Program complete, no more code to execute.
          document.getElementById('stepButton').disabled = 'disabled';
          document.getElementById('runButton').disabled = 'disabled';
          endCondition = true;
        }
      }
    }
    announceResult();
}
