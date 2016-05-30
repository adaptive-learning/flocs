from collections import namedtuple
from blocks.models import Toolbox
from concepts.models import BlockConcept
from practice.models import PracticeSession
from practice.models import StudentModel
from practice.models import StudentTaskInfoModel
from practice.models.task_instance import FlowRating
from practice.services.statistics_service import percentil as compute_percentil
from practice.services.practice_session_service import TASKS_IN_SESSION


def get_statistics_for_user(user):
    student = StudentModel.objects.get_or_create(user=user)[0]
    return get_statistics_for_student(student)


def get_statistics_for_student(student):
    StudentStatistics = namedtuple('StudentStatistics',
            ['overview', 'blocks', 'finished_tasks'])
    finished_tasks = get_finished_tasks(student)
    blocks = get_blocks(student)
    statistics = StudentStatistics(
            blocks=blocks,
            finished_tasks=finished_tasks,
            overview=extract_overview(student, finished_tasks, blocks))
    return statistics


StudentStatsOverview = namedtuple('StudentStatsOverview',
            ['solved_count', 'sessions_count', 'concepts_count',
             'total_flow_time', 'blocks_count', 'total_credits', 'free_credits',
            ])
def extract_overview(student, finished_tasks, blocks):
    overview = StudentStatsOverview(
            solved_count=len(finished_tasks),
            blocks_count=sum(1 for block in blocks if block.purchased),
            concepts_count=compute_practiced_concepts_count(student),
            sessions_count=compute_completed_sessions_count(student),
            total_credits=student.total_credits,
            free_credits=student.free_credits,
            total_flow_time=sum_flow_time(finished_tasks))
    return overview


def compute_practiced_concepts_count(student):
    programming_concepts = student._seen_concepts.filter(programmingconcept__isnull=False)
    return programming_concepts.count()


def compute_completed_sessions_count(student):
    sessions = PracticeSession.objects.filter(student=student, task_counter=TASKS_IN_SESSION)
    return sessions.count()


def sum_flow_time(tasks):
    total_time = sum(task.time for task in tasks
                     if FlowRating.from_key(task.flow) == FlowRating.RIGHT)
    return total_time


StudentBlockInfo = namedtuple('StudentBlockInfo',
        'identifier name level purchased active credits credits_paid concept_stats')
def get_blocks(student):
    # NOTE: current model is not very suitable for this query and should be
    # changed (problems: we need to recalculate a lot of information and some
    # extension to toolbox model or credits handling could brake the current
    # logic)
    acquiring_level = student.get_level() + 1
    block_infos = []
    for toolbox in Toolbox.objects.all():
        for block in toolbox.get_new_blocks():
            purchased = (toolbox.level < acquiring_level)
            active = (toolbox.level == acquiring_level)
            if purchased:
                credits_paid = toolbox.credits
            elif active:
                credits_paid = student.free_credits
            else:
                credits_paid = 0
            concept = BlockConcept.objects.get(block=block).concept_ptr
            block_info = StudentBlockInfo(
                identifier=block.identifier,
                name=block.name,
                level=toolbox.level,
                purchased=purchased,
                active=active,
                credits=toolbox.credits,
                credits_paid=credits_paid,
                concept_stats=compute_concept_stats(student, concept))
            block_infos.append(block_info)
    return block_infos


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
                   'task_id title credits concepts time percentil flow')):

    @staticmethod
    def from_task_instance(instance):
        task = instance.task
        finished_task = FinishedTask(
            task_id=task.pk,
            title=task.title,
            credits=task.get_level(), # hack -> TODO: synchronize with computing credits
            concepts=task.get_programming_concepts(),
            time=instance.time_spent,
            percentil=compute_percentil(instance),
            flow=instance.get_reported_flow_key())
        return finished_task


ConceptStats = namedtuple('ConceptStats', 'identifier solved_count mastered')
TASKS_TO_MASTER = 5
def compute_concept_stats(student, concept):
    solved_count = len([t_info
                        for t_info in StudentTaskInfoModel.objects.filter(student=student)
                        if t_info.is_solved()
                           and concept in t_info.task.get_contained_concepts()])
    concept_stats = ConceptStats(
        identifier=concept.name,
        solved_count=solved_count,
        mastered=solved_count >= TASKS_TO_MASTER)
    return concept_stats
