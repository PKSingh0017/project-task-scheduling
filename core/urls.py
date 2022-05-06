from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    # path('', views.home, name="home"),
    path('project-list', views.ProjectList.as_view(), name="project-list"),
    path('project-detail/<slug>/', views.ProjectDetail.as_view(), name="project-detail"),
    path('team-list/', views.TeamList.as_view(), name="team-list"),
    path('team-detail/<int:id>/', views.TeamDetail.as_view(), name="team-detail"),
    path('task-list', views.TasktList.as_view(), name="task-list"),
    path('task-detail/<slug>/', views.TaskDetail.as_view(), name="task-detail"),
    path('user-list', views.UserList.as_view(), name="user-list"),
    path('user-detail/<int:id>/', views.UserDetail.as_view(), name="task-detail"),
    path('assign-tasks/', views.AssignTasks.as_view(), name="assign-tasks"),
    path('assign-sequence/', views.AssignSequence.as_view(), name="assign-sequence"),
]