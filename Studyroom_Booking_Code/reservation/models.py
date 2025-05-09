from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

# Create your models here.
class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')

    def __str__(self):
        return self.user.username


class Classroom(models.Model):
    classroom_id = models.CharField(max_length=20, primary_key=True)
    floor = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    equipment = models.JSONField()
    is_meeting_room = models.BooleanField(default=False)  # New field to indicate meeting rooms


    def __str__(self):
        return self.classroom_id

class Time(models.Model):
    date = models.DateField()
    time_slot = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.date} - {self.time_slot}"
    
class ClassroomManager(models.Manager):
    def available_classrooms(self, time_slot):
        return self.filter(time=time_slot, availibility=True)

class Classroom_info_by_time_slot(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    time = models.ForeignKey(Time, on_delete=models.CASCADE)
    availibility = models.BooleanField(default=True)

    objects = ClassroomManager()

    class Meta:
        unique_together = ('classroom', 'time')

    def __str__(self):
        return f"{self.classroom} - {self.time} - {'Available' if self.availibility else 'Unavailable'}"
    
    @staticmethod
    def find_available_classrooms_with_equipment(time_id, required_equipment):
        available_classrooms = Classroom_info_by_time_slot.objects.filter(
            time_id=time_id,
            availibility=True,
            classroom__equipment__contains=required_equipment
        ).values_list('classroom_id', flat=True)

        classrooms_with_required_equipment = Classroom.objects.filter(
            classroom_id__in=available_classrooms
        ).distinct()

        return classrooms_with_required_equipment


# class Classroom_availibility_by_time_slot(models.Model):
#     classroom_info_by_time_slot = models.ForeignKey(Classroom_info_by_time_slot, on_delete=models.CASCADE)
#     availibility = models.BooleanField(default=True)

#     def __str__(self):
#         return f"{self.classroom_info_by_time_slot} - {'Available' if self.availibility else 'Unavailable'}"
    
class Student(models.Model):
    student_id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    password = models.CharField(max_length=128, default=12345678)
    major = models.CharField(max_length=100, null=True)

    def save(self, *args, **kargs):
        if not self.user:
            username = self.student_id
            email = f"{username}@m.fudan.edu.cn"
            self.user = User.objects.create_user(username=username, password=self.password, email=email)
            self.user.first_name = self.name.split(' ')[0]
            self.user.last_name = ' '.join(self.name.split(' ')[1:])
            self.user.save()
        else:
            self.user.set_password(self.password)
            self.user.save()
        super().save(*args, **kargs)
    
    def __str__(self):
        return self.name
    
class ReservationManager(models.Manager):
    def student_reservations(self, student):
        return self.filter(student=student)

class Reservation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom_info = models.ForeignKey(Classroom_info_by_time_slot, on_delete=models.CASCADE, null=True)

    objects = ReservationManager()
    
    def save(self, *args, **kargs):
        self.classroom_info.availibility = False
        self.classroom_info.save()
        super().save(*args, **kargs)

    def __str__(self):
        if self.classroom_info:
            return f"{self.student.name} reserved {self.classroom_info.classroom} at {self.classroom_info.time}"
        else:
            return f"{self.student.name} reservation information unavailable"
        

