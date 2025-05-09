from django.contrib import admin
from .models import Classroom, Time, Student, Classroom_info_by_time_slot, Reservation, Profile
from django import forms
# Register your models here.

class StudentAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Student
        fields = ['student_id', 'name', 'password', 'major']

    def save(self, commit=True):
        student = super().save(commit=False)
        if commit:
            student.save()
        return student
    
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm
    list_display = ('student_id', 'name', 'major')

    def save_model(self, request, obj, form, change):
        obj.password = form.cleaned_data['password']
        obj.save()

# Custom form for Profile
class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user', 'user_type']

# Admin for Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    list_display = ('user', 'user_type')

class ClassroomInfoByTimeSlotAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'time', 'availability')
    list_filter = ('availabitlity',)

# admin.site.register(Student, StudentAdmin)

admin.site.register(Classroom)
admin.site.register(Time)
admin.site.register(Classroom_info_by_time_slot)
admin.site.register(Reservation)