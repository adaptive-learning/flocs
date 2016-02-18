from practice.models import StudentModel


def get_practice_details(user):
    details_dict = {}
    student = StudentModel.objects.get(user_id=user.pk)
    details_dict['total-credits'] = student.total_credits
    details_dict['free-credits'] = student.free_credits
    return details_dict
