"""Updates skill of student and difficulty of task
"""

def update_skill(student, task, feedback, predicted_feedback):
    """Updates student's skill as well as task's difficulty base on predicted
    and real feedback from the student. Update is based on ELO.

    Args:
        student: vector of student's skills
        task: vector of task's difficulties
        feedback: real feedback collected from the student
        predicted_feedback: feedback predicted by out model of student and task
    """

    # coefficients of decay function (the more answers is collected the less
    # effect will the new answer have)
    alpha = 1
    beta = 1

    # same as in ELO for amateur chess players; later might by substituted by
    # PFA prediction
    k = 32

    # number of previously collected answers, not implemented yet
    answers = 1

    # for all skills that the task tests update the students skill
    for i in range(len(student)):
        if task[i] != -1:
            student[i] += k * (predicted_feedback - feedback)

    # updates general difficulty of task
    task[0] += alpha / (1 + beta * answers)  * (feedback - predicted_feedback)
