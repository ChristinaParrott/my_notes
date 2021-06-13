#Defines URL patterns for my_notes

from django.urls import path
from . import views

app_name = 'my_notess'
urlpatterns = [
    #Home page
    path('', views.index, name='index'),
    #Page that shows all topics
    path('topics/', views.topics, name='topics'),
    #Notes page for a single topic
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    #Add a new topic page
    path('new_topic/', views.new_topic, name='new_topic'),
    #Add a new note to a topic
    path('new_note/<int:topic_id>/', views.new_note, name='new_note'),
    #Edit a note
    path('edit_note/<int:note_id>/', views.edit_note, name='edit_note'),
]