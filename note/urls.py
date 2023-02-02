from django.urls import path

from . import views

urlpatterns = [
    path('note', views.Note.as_view(), name='note'),
    path('collaborator', views.NoteCollaborator.as_view(), name='collaborator'),
    path('label', views.Label.as_view(), name='label'),
    path('label_note', views.AddLabelToNote.as_view(), name='label_note')
]
