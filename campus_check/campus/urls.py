from django.urls import path
from campus import views
from .views import TopUniversitiesView #Xuanming Feng


app_name = 'universities'

urlpatterns = [
    path('', views.university_list, name='university_list'),
    path('university_detail/<slug:university_name_slug>/', views.university_detail, name='university_detail'),
    path('courses/<slug:course_name_slug>/', views.course_detail, name='course_detail'),
    path('courses/<slug:course_name_slug>/submit_review/', views.submit_review, name='submit_review'),
    path('top_universities/', TopUniversitiesView.as_view(), name='top_universities'),  #Xuanming Feng
]


