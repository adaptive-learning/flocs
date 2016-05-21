from collections import namedtuple
from practice.models import StudentModel
from practice.models import StudentTaskInfoModel
from practice.services.statistics_service import percentil as compute_percentil



def get_statistics_for_user(user):
    student = StudentModel.objects.get_or_create(user=user)[0]
    return get_statistics_for_student(student)


def get_statistics_for_student(student):
    StudentStatistics = namedtuple('StudentStatistics', ['finished_tasks'])
    statistics = StudentStatistics(finished_tasks=get_finished_tasks(student))
    return statistics


def get_finished_tasks(student):
    task_infos = StudentTaskInfoModel.objects.filter(student=student)
    finished_tasks_instances = [t_info.last_solved_instance
                                for t_info in task_infos if t_info.is_solved()]
    sorted_finished_tasks_instances = sorted(finished_tasks_instances,
            key=lambda instance: (instance.task.get_level(), instance.task.pk))
    finished_tasks = [FinishedTask.from_task_instance(task_instance)
                      for task_instance in sorted_finished_tasks_instances]
    return finished_tasks


class FinishedTask(namedtuple('FinishedTaskTuple',
                   'title credits concepts time percentil flow')):

    #def __init__(self, title, credits, concepts, time, percentil, flow):
    #    self.title = title
    #    self.credits = credits
    #    self.concepts = concepts
    #    self.time = time
    #    self.percentil = percentil
    #    self.flow = flow

    @staticmethod
    def from_task_instance(instance):
        task = instance.task
        finished_task = FinishedTask(
            title=task.title,
            credits=task.get_level(), # hack -> TODO: synchronize with computing credits
            concepts=task.get_programming_concepts(),
            time=instance.time_spent,  # fake -> TODO: compute real time
            percentil=compute_percentil(instance),
            flow=instance.get_reported_flow_key())
        return finished_task

