from django.shortcuts import render
from requests import request
from rest_framework import generics
from . import models as core_models
from .serializers import *
from django.views.generic import View
from django.http import HttpResponseRedirect
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import (
        SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly, 
        BasePermission, IsAdminUser, DjangoModelPermissions, AllowAny
    )
from allauth.account.views import SignupView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import status
from . import models as core_models
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from rest_framework.pagination import PageNumberPagination
from core.pagination import PaginationHandlerMixin
from django.db.models import Q
from django.db.models import Max
from .models import assign_sequences

from core import serializers

class ProjectList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = core_models.Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    # def get_queryset(self):
    #     queryset = store_models.Item.objects.all()
    #     category_slug = self.request.query_params.get('category')
    #     if category_slug is not None:
    #         queryset = queryset.filter(category__slug=category_slug)
    #     return queryset

class TasktList(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = core_models.Task.objects.all()
    serializer_class = TaskListSerializer

    # def perform_create(self, serializer):
    #     try:
    #         serializer.save(created_by=self.request.user)
    #     except:
    #         serializer.save()

    def get_queryset(self):
        queryset = core_models.Task.objects.all()
        project_slug = self.request.query_params.get('project')
        if project_slug is not None:
            queryset = queryset.filter(project__slug=project_slug)
        return queryset

class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = core_models.Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'slug'

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = core_models.Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'slug'

class UserList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class TeamList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = core_models.Team.objects.all()
    serializer_class = TeamSerializer

class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = core_models.Team.objects.all()
    serializer_class = TeamSerializer

# Returns the total engagement time of a team
def get_team_eng_time(team):
    res = 0
    if team.assigned_tasks == None:
        return 0
    res += team.assigned_tasks.completion_time
    for tt in team.pending_tasks.all():
        res += tt.completion_time
    return res

# Returns team with least engagement time
def get_best_team():
    all_teams = Team.objects.all()
    res_team = all_teams[0]
    min_time = 100
    for tt in all_teams:
        curr_time = get_team_eng_time(tt)
        if curr_time < min_time:
            min_time = curr_time
            res_team = tt
    return res_team

def assign_tasks(task_list):
    total_tasks = task_list.count()
    assigned_tasks = 0
    if total_tasks>0:
        max_sequence = task_list.aggregate(Max('sequence'))['sequence__max']
        for j in range(1, max_sequence+1):
            c_task_list = task_list.filter(sequence=j)
            for t in c_task_list:
                team = get_best_team()
                t.assigned_to = team
                assigned_tasks += 1
                if team.assigned_tasks:
                    team.pending_tasks.add(t)
                else:
                    team.assigned_tasks = t
                team.save()
                t.save()
            
    unassigned_tasks = total_tasks - assigned_tasks
    res = {
        "total tasks": total_tasks,
        "unassigned tasks": unassigned_tasks,
        "assigned tasks": assigned_tasks
    }
    return res

class AssignTasks(APIView):

    def post(self, *args, **kwargs):
        project = self.request.data.get('project_slug')
        if project:
            curr_project = Project.objects.get(slug=project)
            unassigned_task = Task.objects.filter(assigned_to=None, project=curr_project)
        else:
            unassigned_task = Task.objects.all()
        context = {}
        context["result"] = assign_tasks(unassigned_task)
        return Response(context, status=HTTP_200_OK)



class AssignSequence(APIView):

    def post(self, *args, **kwargs):
        project_id = self.request.data.get('project_id')
        curr_project = Project.objects.get(id=project_id)
        all_tasks = Task.objects.filter(project=curr_project)
        for t in all_tasks:
            assign_sequences(t)
        context = {
            "count": all_tasks.count()
        }
        return Response(context, status=HTTP_200_OK)

def unassign_all_tasks():
    all_tasks = Task.objects.all()
    all_teams = Team.objects.all()
    for tt in all_teams:
        tt.assigned_tasks = None
        tt.pending_tasks.clear()
        tt.save()
    for t in all_tasks:
        t.assigned_to=None
        t.save()

def clear_all_task_sequence():
    for t in Task.objects.all():
        t.sequence=0
        t.save()



