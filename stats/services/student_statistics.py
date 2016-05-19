from collections import namedtuple
from practice.models import StudentModel
from practice.models import StudentTaskInfoModel



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
    # TODO: sorting (according to (credits,pk)?)
    finished_tasks = [FinishedTask.from_task_instance(task_instance)
                      for task_instance in finished_tasks_instances]
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
            concepts=["programming-sequence","programming-repeat"],
            time=30,  # fake -> TODO: compute real time
            percentil=100,  # fake -> TODO: compute real percentil
            flow=2)  # fake -> TODO: compute real flow
        return finished_task
