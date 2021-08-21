from django.urls import path

from . import views

app_name = 'kb_service'
urlpatterns = [
    path('user/', views.newUser, name='newUser'),                                           #POST
    path('kurs/', views.newKurs, name='newKurs'),                                           #POST
    path('lecturer/', views.newLecturer, name='newLecturer'),                               #POST
    path('learning_item/', views.newLearningItem, name='newLearningItem'),                  #POST
    path('user/<str:id>', views.userUpdateDelete, name='userUpdateDelete'),                 #PUT / DELETE
    path('lecturer/<str:id>', views.lecturerUpdate, name='lecturerUpdate'),                 #PUT
    path('learning_item/<str:id>', views.learningItemDelete, name='learningItemDelete'),   #DELETE


]