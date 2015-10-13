describe('Testing the maze filter', function() {

  // load the flocs.maze module, which contains the filter
  beforeEach( module('flocs.maze'));

  it('multiply real coordinates with boxSize',
      inject(function(pixelCoordinatesFilter) {
    // prepare data
    var input = 4;
    var visualisation = {
      boxSize: 10
    };
    expect(pixelCoordinatesFilter(input, visualisation)).toBe(input * visualisation.boxSize);
  }));

});
