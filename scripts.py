from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation
import random


def fix_marks(student_name):
  student = Schoolkid.objects.filter(full_name__contains=student_name).get()
  bad_marks = Mark.objects.filter(schoolkid = student, points__in = [2,3])
  bad_marks.update(points = 5)


def remove_chastisements(student_name):
  student = Schoolkid.objects.filter(full_name__contains=student_name).get()
  student_chastisements = Chastisement.objects.filter(schoolkid=student)
  student_chastisements.delete()


def create_commendation(student_name, subject=""):
  student = Schoolkid.objects.filter(full_name__contains=student_name).get()
  student_grade = student.year_of_study
  student_group = student.group_letter
  student_lessons = Lesson.objects.filter(year_of_study=student_grade, group_letter=student_group, subject__title__contains=subject)

  commendation_texts = ["Молодец!", "Отлично!", "Хорошо!", "Великолепно!", "Потрясающе!",  "С каждым разом у тебя получается всё лучше!", "Очень хороший ответ!"]
  Commendation_lesson = random.choice(student_lessons)
  Commendation_date = Commendation_lesson.date
  Commendation_subject = Commendation_lesson.subject
  Commendation_teacher = Commendation_lesson.teacher
  commendation_text = random.choice(commendation_texts)
  Commendation.objects.create(text=commendation_text, created=Commendation_date, schoolkid=student, subject=Commendation_subject, teacher=Commendation_teacher)