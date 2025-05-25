from datacenter.models import Schoolkid, Mark, Chastisement
from datacenter.models import Lesson, Commendation
import random


COMPLIMENTS = ["Молодец!", "Отлично!", "Хорошо!", "Великолепно!",
               "Потрясающе!", "Очень хороший ответ!",
               "С каждым разом у тебя получается всё лучше!"]


def get_student(student_name):
    try:
        student = Schoolkid.objects.get(full_name__contains=student_name)
        return student
    except Schoolkid.DoesNotExist:
        print('Такого ученика не существует!')
        return None
    except Schoolkid.MultipleObjectsReturned:
        print('Учеников с таким именем много. Пожалуйста, уточните!')
        return None


def fix_marks(student_name):
    student = get_student(student_name)
    if not student:
        return 0
    bad_marks = Mark.objects.filter(schoolkid=student, points__in=[2, 3])
    bad_marks.update(points=5)


def remove_chastisements(student_name):
    student = get_student(student_name)
    if not student:
        return 0
    student_chastisements = Chastisement.objects.filter(schoolkid=student)
    student_chastisements.delete()


def create_commendation(student_name, subject=""):
    student = get_student(student_name)
    if not student:
        return 0
    student_grade = student.year_of_study
    student_group = student.group_letter

    commendation_lesson = Lesson.objects.filter(
        year_of_study=student_grade,
        group_letter=student_group,
        subject__title__contains=subject
    ).order_by("?").first()
    if not commendation_lesson:
        print("Уроков по данному предмету нет!")
        return 0

    commendation_date = commendation_lesson.date
    commendation_subject = commendation_lesson.subject
    commendation_teacher = commendation_lesson.teacher
    commendation_text = random.choice(COMPLIMENTS)

    Commendation.objects.create(
        text=commendation_text,
        created=commendation_date,
        schoolkid=student,
        subject=commendation_subject,
        teacher=commendation_teacher
    )
