from rest_framework import generics, mixins, status
from rest_framework.decorators import action
from django.db.models import Q

from .models import *
from .serializers import *
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.timezone import make_aware
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404

#settings.TIME_ZONE


class TodoTaskListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = TodoTask.objects.all()
    serializer_class = TodoTaskSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        t_delta = self.request.query_params.get('timedelta')
        # project = self.request.query_params.get('project_id')
        if t_delta:
            if len(t_delta) < 11:
                due_date = datetime.strptime(t_delta, '%d.%m.%Y')
                due_date = make_aware(due_date)
                start_of_day = due_date.replace(hour=0, minute=0, second=0, microsecond=0)
                end_of_day = start_of_day + timedelta(days=1)
                queryset = TodoTask.objects.filter(date_end__range=[start_of_day, end_of_day])
            else:
                date_range = t_delta.split(',')
                # return Response(len(timedelta))
                start_date = datetime.strptime(date_range[0], '%d.%m.%Y')
                end_date = datetime.strptime(date_range[1], '%d.%m.%Y')

                # Convert start_date and end_date to aware datetime objects
                start_date = make_aware(start_date)
                end_date = make_aware(end_date)

                queryset = TodoTask.objects.filter(date_end__range=[start_date, end_date])
        else:
            return self.list(request, *args, **kwargs)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        desc_list_data = request.data.pop('items', [])
        task_serializer = self.get_serializer(data=request.data)
        task_serializer.is_valid(raise_exception=True)
        task = task_serializer.save()

        for item_data in desc_list_data:
            item_data['task'] = task.id

        item_serializer = TodoItemSerializer(data=desc_list_data, many=True)
        item_serializer.is_valid(raise_exception=True)
        items = item_serializer.save()

        task.desc_list.set(items)
        return Response(task_serializer.data, status=status.HTTP_201_CREATED)

        # todo_task = task_serializer.save()
        # todo_task.desc_list.set(items)

        # return Response(task_serializer.data, status=status.HTTP_201_CREATED)


class TodoTaskDetailView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):
    queryset = TodoTask.objects.all()
    serializer_class = TodoTaskSerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        t_delta = self.request.query_params.get('timedelta')
        # project = self.request.query_params.get('project_id')
        if t_delta:
            if len(t_delta) < 11:
                due_date = datetime.strptime(t_delta, '%d.%m.%Y')
                due_date = make_aware(due_date)
                start_of_day = due_date.replace(hour=0, minute=0, second=0, microsecond=0)
                end_of_day = start_of_day + timedelta(days=1)
                queryset = TodoTask.objects.filter(date_end__range=[start_of_day, end_of_day])
            else:
                date_range = t_delta.split(',')
                # return Response(len(timedelta))
                start_date = datetime.strptime(date_range[0], '%d.%m.%Y')
                end_date = datetime.strptime(date_range[1], '%d.%m.%Y')

                # Convert start_date and end_date to aware datetime objects
                start_date = make_aware(start_date)
                end_date = make_aware(end_date)

                queryset = TodoTask.objects.filter(date_end__range=[start_date, end_date])
        else:
            return self.retrieve(request, *args, **kwargs)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        # return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update_done(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def update_done(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance._is_put_request = True
        request.data['done'] = not instance.done
        if request.data['done'] == True and instance.desc_list != []:
            for item in instance.desc_list.all():
                item.done = True
                item.save()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TodoTaskDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = TodoTask.objects.all()
    serializer_class = TodoTaskSerializer
    lookup_field = 'pk'
    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TodoItemListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TodoItemDetailView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        # task = self.get_object()
        # task_serializer = self.get_serializer(task)
        # task_data = task_serializer.data
        #
        # todo_items = task.desc_list.all()
        # task_data['desc_list'] = TodoItemSerializer(todo_items, many=True).data
        #
        # return Response(task_data)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update_done(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def update_done(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        request.data['done'] = not instance.done
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TodoItemDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    lookup_field = 'pk'
    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProjectListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        t_delta = self.request.query_params.get('timedelta')
        # project = self.request.query_params.get('project_id')
        if t_delta:
            if len(t_delta) < 11:
                due_date = datetime.strptime(t_delta, '%d.%m.%Y')
                due_date = make_aware(due_date)
                start_of_day = due_date.replace(hour=0, minute=0, second=0, microsecond=0)
                end_of_day = start_of_day + timedelta(days=1)
                queryset = Project.objects.filter(date_end__range=[start_of_day, end_of_day])
            else:
                date_range = t_delta.split(',')
                # return Response(len(timedelta))
                start_date = datetime.strptime(date_range[0], '%d.%m.%Y')
                end_date = datetime.strptime(date_range[1], '%d.%m.%Y')

                # Convert start_date and end_date to aware datetime objects
                start_date = make_aware(start_date)
                end_date = make_aware(end_date)

                queryset = Project.objects.filter(date_end__range=[start_date, end_date])
        else:
            return self.list(request, *args, **kwargs)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # return self.create(request, *args, **kwargs)


class ProjectDetailView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'id'
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        t_delta = self.request.query_params.get('timedelta')

        if t_delta:
            if len(t_delta) < 11:
                due_date = datetime.strptime(t_delta, '%d.%m.%Y')
                due_date = make_aware(due_date)
                start_of_day = due_date.replace(hour=0, minute=0, second=0, microsecond=0)
                end_of_day = start_of_day + timedelta(days=1)
                project = self.get_object()
                tasks_list = TodoTask.objects.filter(
                    Q(date_end__range=[start_of_day, end_of_day]) & Q(project=project)
                )
            else:
                date_range = t_delta.split(',')
                start_date = datetime.strptime(date_range[0], '%d.%m.%Y')
                end_date = datetime.strptime(date_range[1], '%d.%m.%Y')

                start_date = make_aware(start_date)
                end_date = make_aware(end_date)

                project = self.get_object()
                tasks_list = TodoTask.objects.filter(
                    Q(date_end__range=[start_date, end_date]) & Q(project=project)
                )
        else:
            return self.retrieve(request, *args, **kwargs)

        task_serializer = TodoTaskSerializer(tasks_list, many=True)
        tasks_data = task_serializer.data

        serializer = self.get_serializer(project)
        project_data = serializer.data
        project_data['tasks_list'] = tasks_data

        return Response(project_data)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update_done(request, *args, **kwargs)

    def update_done(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        request.data['done'] = not instance.done
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProjectDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'pk'
    permission_classes = [AllowAny]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
