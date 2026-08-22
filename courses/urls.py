from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/<int:id>/', views.course_detail, name='course_detail'),
    path('course/<int:id>/enroll/', views.enroll_course, name='enroll_course'),
    path('create/', views.create_course, name='create_course'),
    path('course/<int:course_id>/add-lesson/', views.create_lesson, name='create_lesson'),
    path('lesson/<int:lesson_id>/complete/', views.mark_lesson_complete, name='mark_lesson_complete'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('course/<int:course_id>/students/', views.course_students, name='course_students'),
    path('my-courses/', views.student_dashboard, name='student_dashboard'),
    path('course/<int:id>/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/verify/', views.verify_code, name='verify_code'),
    path('checkout/success/', views.payment_success, name='payment_success'),
]