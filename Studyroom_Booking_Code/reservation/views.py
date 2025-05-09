from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
# Create your views here.
from django.http import HttpResponse
from .models import Classroom, Time, Classroom_info_by_time_slot, Reservation, Student

@login_required
def time_index(request):
    time_list = Time.objects.order_by("date", "time_slot")
    user_id = request.user.id
    context = {"time_list": time_list, "user_id": user_id}
    return render(request, "reservation/time_index.html", context)

# def time_slot_detail(request, time_id):
#     time = get_object_or_404(Time, pk=time_id)
#     available_classrooms = [classroom_available_info.classroom_info_by_time_slot.classroom for classroom_available_info in Classroom_availibility_by_time_slot if classroom_available_info.availability and classroom_available_info.classroom_info_by_time_slot.time=time]
#     context = {"time": time, "classrooms": available_classrooms}
# #     return render(request, "reservation/time_slot_detail.html", context)

# @login_required
# def time_slot_detail(request, time_id):
#     time = get_object_or_404(Time, pk=time_id)
    
#     availible_classroom_list = Classroom_info_by_time_slot.objects.available_classrooms(time)

#     for classroom_info in availible_classroom_list:
#         equipment_list = classroom_info.classroom.equipment
#         cleaned_equipment = ", ".join(equipment_list).replace("[", "").replace("]", "").replace("'", "")
#         classroom_info.classroom.equipment = cleaned_equipment

    
#     context = {
#         'classroom_info_list': availible_classroom_list,
#         'time': time,
#         'user_id': request.user.id,
#     }

#     return render(request, 'reservation/time_slot_detail.html', context)

@login_required
def time_slot_detail(request, time_id):
    time = get_object_or_404(Time, pk=time_id)
    user_profile = request.user.profile

    equipment_query = request.GET.get('equipment', '')
    required_equipment = [e.strip() for e in equipment_query.split(',')] if equipment_query else []
    

    classrooms = Classroom_info_by_time_slot.objects.filter(time=time_id, availibility=True)
    

    if required_equipment:
        classrooms_with_required_equipment = [
            classroom_info.classroom for classroom_info in classrooms
            if all(equip in classroom_info.classroom.equipment for equip in required_equipment)
        ]
    else:
        classrooms_with_required_equipment = [classroom_info.classroom for classroom_info in classrooms]

    if user_profile.user_type == 'student':
        classrooms_with_required_equipment = [
            classroom for classroom in classrooms_with_required_equipment
            if not classroom.is_meeting_room
        ]

    for classroom_info in classrooms_with_required_equipment:
        equipment_list = classroom_info.equipment
        cleaned_equipment = ", ".join(equipment_list).replace("[", "").replace("]", "").replace("'", "")
        classroom_info.equipment = cleaned_equipment
    
    context = {
        'classrooms_with_required_equipment': classrooms_with_required_equipment,
        'time': time,
        'user_id': request.user.id,
    }

    return render(request, 'reservation/time_slot_detail.html', context)



@login_required
def make_reservation(request, classroom_id, time_id):
    student = get_object_or_404(Student, student_id=request.user.username)
    classroom_info = get_object_or_404(Classroom_info_by_time_slot, classroom_id=classroom_id, time_id=time_id)

    if classroom_info.availibility:
        reservation = Reservation(student=student, classroom_info=classroom_info)
        reservation.save()
        return redirect('reservation:reservation_success')
    else:
        return HttpResponse("This classroom is already booked for the selected time slot.")
    
@login_required
def reservation_success(request):
    context = {
        "user_id": request.user.id,
    }
    return render(request, "reservation/success.html", context)

def custom_logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def user_reservation(request, student_id):
    # reservations = Reservation.objects.filter(student__student_id=request.user.username)
    student = get_object_or_404(Student, student_id=request.user.username)
    reservations = Reservation.objects.student_reservations(student)
    context = {
        'reservations': reservations,
        'user_id': request.user.id,
        }
    return render(request, 'reservation/user_reservation.html', context)

@login_required
def cancel_reservation(request, reservation_id):
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, id=reservation_id)
        student_id = reservation.student.student_id
        classroom_info = get_object_or_404(Classroom_info_by_time_slot, classroom=reservation.classroom_info.classroom, time=reservation.classroom_info.time)
        classroom_info.availibility = True
        classroom_info.save()
        reservation.delete()
        return redirect(reverse('reservation:user_reservation', args=[student_id]))
    else:
        return redirect(reverse('reservation:user_reservation', args=[request.user.id]))

def test(request):
    return render(request, "reservation/test.html")

@login_required
def redirect_to_user_profile(request):
    user_id = request.user.id
    redirect_url = f'/user/{user_id}/profile/'
    return redirect(redirect_url)

@login_required
def user_profile_view(request, user_id):
    first_name = request.user.first_name
    last_name = request.user.last_name
    name = first_name + " " + last_name
    student = get_object_or_404(Student, user=request.user)
    major = student.major
    context = {
        'user_name': name,
        'user_email': request.user.email,
        'user_id': request.user.id,
        'major': major,
        }
    return render(request, "reservation/user_profile.html", context)

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect(f'/user/{user.id}/profile')
        else:
            return render(request, 'registration/login.html', {'error_message': 'Invalid Credentials'})
    else:
        return render(request, 'registration/login.html')
    
def redirect_to_login(request):
    return redirect('/login/')