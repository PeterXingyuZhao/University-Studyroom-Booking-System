from django.urls import path

from . import views

app_name = 'reservation'

urlpatterns = [
    path("time/", views.time_index, name="time_index"), # (/reservation/)time/
    path("time/<int:time_id>/", views.time_slot_detail, name="time_slot_detail"), # (/reservation)/time/2/
    # path("make_reservation/<str:classroom_id>/<int:time_id>/", views.make_reservation, name='make_reservation'),
    # path("reservation_success/", views.reservation_success, name="reservation_success"),
    path('make_reservation/<str:classroom_id>/<int:time_id>/', views.make_reservation, name='make_reservation'),
    path('reservation_success/', views.reservation_success, name='reservation_success'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('user/<str:student_id>/', views.user_reservation, name='user_reservation'),
    path('cancel/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
]