describe('Testing the maze filter', function() {

  var filter;

  beforeEach( module('flocs.maze'));

  it('multiply real coordinates with boxSize',
      inject(function(pixelCoordinatesFilter) {
    // prepare data
    var input = 4;
    // QUESTION should we import viualisation object from maze.dr.js ?
    var visualisation = {
      boxSize: 10
    };
    expect(pixelCoordinatesFilter(input, visualisation)).toBe(input * visualisation.boxSize);
  }));

});
