from django.contrib.auth.models import User
from math import inf
from collections import OrderedDict
from common.flow_factors import FlowFactors
from common.simulation import Simulation
from tasks.models import TaskModel
from practice.models import TasksDifficultyModel
from practice.models import TaskInstanceModel
from practice.models import StudentModel
from practice.models.task_instance import FlowRating
from practice.services import practice_service


class PracticeSimulation(Simulation):
    """
    Simulation of a practice session.
    """

    fixtures = ['blocks', 'levels', 'tasks', 'task-difficulties', 'instructions']
    log_path_pattern = 'practice/simulated-data/practice-simulation-{timestamp}'

    def prepare(self, behavior, max_instances=7, max_time=inf):
        """
        Set simulation parameters.

        Args:
            behavior: behavior of a simulated student (SimulatedStudent)
            max_task_instances: maximum length of session in number of instances
            max_time: maximum number of session in number of seconds
        """
        self.behavior = behavior
        self.max_instances = max_instances
        self.max_time = max_time

    def run_simulation(self):
        """
        Run the simulation and create simulation log as a list of dictionaries,
        each dictonary for one task instance taken.
        """
        # TODO: decomposition
        # create some task instances to avoid time bonuses for poor performances
        any_student = StudentModel.objects.create(user=User.objects.create(username='any'))
        for task in TaskModel.objects.all():
            TaskInstanceModel.objects.create(task=task, student=any_student,
                                             solved=True, time_spent=300)
        user = User.objects.create()
        instances_count, time_spent = 0, 0
        while instances_count < self.max_instances and time_spent < self.max_time:
            self.logger.new_round()
            self.logger.log('instance', instances_count + 1)

            task_info = practice_service.get_next_task_in_session(user)
            task_id = task_info.task.pk
            task_difficulty = TasksDifficultyModel.objects.get(task_id=task_id)

            student = StudentModel.objects.get(user=user)
            self.logger.log('level', student.level.block_level)
            self.logger.log('total-credits', student.total_credits)
            self.logger.log('free-credits', student.free_credits)
            student_skill = student.get_skill_dict()
            for factor in FlowFactors.student_factors():
                self.logger.log('student-' + factor.name, student_skill[factor])

            self.logger.log('task-id', task_id)
            self.logger.log('task-title', task_info.task.title)
            self.logger.log('task-level', task_info.task.level)
            task_difficulty = task_difficulty.get_difficulty_dict()
            for factor in FlowFactors.task_factors():
                self.logger.log('task-' + factor.name, task_difficulty[factor])
            self.logger.log('instructions', ' '.join(task_info.instructions))


            #self.logger.log('flow-prediction', TaskInstanceModel.objects
            #    .get(id=task_info.task_instance.['task-instance-id']).predicted_flow)
            self.logger.log('flow-prediction', task_info.task_instance.predicted_flow)

            solved, time = self.behavior.solve_task(task_difficulty)
            self.logger.log('solved', solved)
            self.logger.log('time-spent', time)
            result = practice_service.process_attempt_report(user, report={
                'task-instance-id': task_info.task_instance.pk,
                'attempt': 1,
                'solved': solved,
                'time': time,
            })
            instance_pk = task_info.task_instance.pk
            if solved:
                flow = self.behavior.report_flow()
                practice_service.process_flow_report(
                        user=user,
                        task_instance_id=instance_pk,
                        reported_flow=flow)
            else:
                practice_service.process_giveup_report(
                        user=user,
                        task_instance_id=instance_pk,
                        time_spent=time)
            self.logger.log('flow-report',
                    TaskInstanceModel.objects.get(pk=instance_pk).reported_flow)

            self.logger.log('result-earned-credits', result.credits)
            self.logger.log('result-speed-bonus', result.speed_bonus)
            self.logger.log('result-new-blocks', len(result.purchases))
            self.logger.log('updated-task-difficulty',
                    TasksDifficultyModel.objects.get(task_id=task_id) \
                    .get_difficulty_dict()[FlowFactors.TASK_BIAS])

            instances_count += 1
            time_spent += time
            #print(instances_count, ' ', time_spent)
