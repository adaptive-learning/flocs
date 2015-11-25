/*
 * Main practice controller
 */
angular.module('flocs.practice')
    .controller('practiceCtrl', ['$scope', '$timeout', 'practiceSessionService',
        function ($scope, $timeout, practiceSessionService) {

            // start a new practice session
            practice();

            function practice() {
                // set task
                practiceSessionService.practicingTask().then(function () {

                        // ask for next task
                        // TODO: show modal ("Continue to next task?")
                        $timeout(nextTaskQuestion, 400).then(function() {

                            // set next task
                            practice();
                        });
                    }
                );
            }

            function nextTaskQuestion() {
                alert('Solved. Next task?');
            }

        }]);

