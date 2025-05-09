from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Classroom, Time, Classroom_info_by_time_slot

@receiver(post_save, sender=Classroom)
def add_classroom_in_Classroom_info_by_time_slot(sender, instance, created, **kargs):
    if created:
        times = Time.objects.all()
        for time in times:
            Classroom_info_by_time_slot.objects.create(classroom=instance, time=time, availibility=True)

@receiver(post_save, sender=Time)
def add_time_in_Classroom_info_by_time_slot(sender, instance, created, **kargs):
    if created:
        classrooms = Classroom.objects.all()
        for classroom in classrooms:
            Classroom_info_by_time_slot.objects.create(classroom=classroom, time=instance, availibility=True)

# @receiver(post_save, sender=Classroom_info_by_time_slot)
# def add_classroom_info_by_time_slot_in_Classroom_availability_by_time_slot(sender, instance, created, **kargs):
#     if created:
#         Classroom_availibility_by_time_slot.objects.create(classroom_info_by_time_slot=instance)