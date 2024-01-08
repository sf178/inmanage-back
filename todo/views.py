from rest_framework import generics, mixins, status
from rest_framework.decorators import action
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from test_backend.custom_methods import IsAuthenticatedCustom

from .models import *
from .serializers import *
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.timezone import make_aware
from django.shortcuts import get_object_or_404

#settings.TIME_ZONE


class TodoTaskListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = TodoTaskSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        # Фильтрация объектов по текущему пользователю
        return TodoTask.objects.filter(user=self.request.user)

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

        desc_list_data = request.data.pop('desc_list', [])
        task_serializer = self.get_serializer(data=request.data)
        task_serializer.is_valid(raise_exception=True)
        task = task_serializer.save(user=self.request.user)
        if 'project' in request.data:
            project_id = request.data['project']
            project_instance = Project.objects.get(id=project_id, user=self.request.user)
            project_instance.tasks_list.add(task)
            task.project = project_instance
            task.save()  # Сохраняем изменение связанного проекта
        for item_data in desc_list_data:
            item_data['task'] = task.id
            item_data['user'] = task.user

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
    serializer_class = TodoTaskSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return TodoTask.objects.filter(user=self.request.user)

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

    def update_done(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance._is_put_request = True
        request.data['done'] = not instance.done
        if request.data['done'] == True and instance.desc_list != []:
            for item in instance.desc_list.all():
                if item.done != request.data['done']:
                    item.done = request.data['done']
                    item.save()
        request.data['expenses_is_completed'] = not instance.expenses_is_completed
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TodoTaskUpdateView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):
    serializer_class = TodoTaskSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return TodoTask.objects.filter(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        # Обработка вложенных данных
        nested_data_fields = {
            'desc_list': TodoItemSerializer,
            'income': TodoIncomeSerializer,
            'expenses': TodoExpensesSerializer
        }
        for field_name, serializer_class in nested_data_fields.items():
            self._process_nested_data(field_name, serializer_class, instance, request)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def _process_nested_data(self, field_name, serializer_class, instance, request):
        if field_name in request.data:
            nested_data = request.data.pop(field_name)
            for item_data in nested_data:
                item_serializer = serializer_class(data=item_data)
                item_serializer.is_valid(raise_exception=True)
                item_instance = item_serializer.save(user=instance.user, task=instance)
                getattr(instance, field_name).add(item_instance)


class TodoTaskDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    serializer_class = TodoTaskSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return TodoTask.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TodoItemListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = TodoItemSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return TodoItem.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.perform_create(request, *args, **kwargs)

    def perform_create(self, serializer, *args, **kwargs):
        if 'user' in serializer.validated_data:
            raise ValidationError("You cannot set the user manually.")
        serializer.save(user=self.request.user)


class TodoItemDetailView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):
    serializer_class = TodoItemSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return TodoItem.objects.filter(user=self.request.user)

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
    #
    # def patch(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     income_instances = []
    #     expenses_instances = []
    #     if 'income' in request.data:
    #         income_data = request.data.pop('income')
    #         for income in income_data:
    #             income_serializer = TodoIncomeSerializer(data=income)
    #             income_serializer.is_valid(raise_exception=True)
    #             income_instance = income_serializer.save(user_id=instance.user, item=instance)
    #             income_instances.append(income_instance)
    #     if 'expenses' in request.data:
    #         expenses_data = request.data.pop('expenses')
    #         for expense in expenses_data:
    #             expenses_serializer = TodoExpensesSerializer(data=expense)
    #             expenses_serializer.is_valid(raise_exception=True)
    #             expenses_instance = expenses_serializer.save(user_id=instance.user, project=instance)
    #             expenses_instances.append(expenses_instance)
    #
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     if income_instances:
    #         instance.income.add(*[income.id for income in income_instances])
    #     if expenses_instances:
    #         instance.expenses.add(*[expense.id for expense in expenses_instances])
    #
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #
    #     return Response(serializer.data)


    def update_done(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        request.data['done'] = not instance.done
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TodoItemUpdateView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):
    serializer_class = TodoItemSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return TodoItem.objects.filter(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        # Обработка вложенных данных
        nested_data_fields = {
            # 'desc_list': TodoItemSerializer,
            'income': TodoIncomeSerializer,
            'expenses': TodoExpensesSerializer
        }
        for field_name, serializer_class in nested_data_fields.items():
            self._process_nested_data(field_name, serializer_class, instance, request)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def _process_nested_data(self, field_name, serializer_class, instance, request):
        if field_name in request.data:
            nested_data = request.data.pop(field_name)
            for item_data in nested_data:
                item_serializer = serializer_class(data=item_data)
                item_serializer.is_valid(raise_exception=True)
                item_instance = item_serializer.save(user=instance.user, task=instance)
                getattr(instance, field_name).add(item_instance)


class TodoItemDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    serializer_class = TodoItemSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return TodoItem.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProjectListView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

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

    def perform_create(self, serializer):
        if 'user' in serializer.validated_data:
            raise ValidationError("You cannot set the user manually.")
        serializer.save(user=self.request.user)


class ProjectDetailView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin):
    serializer_class = ProjectSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

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
        #project_data['tasks_list'] = tasks_data

        return Response(project_data)
    #
    # def patch(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     income_instances = []
    #     expenses_instances = []
    #     if 'income' in request.data:
    #         income_data = request.data.pop('income')
    #         for income in income_data:
    #             income_serializer = TodoIncomeSerializer(data=income)
    #             income_serializer.is_valid(raise_exception=True)
    #             income_instance = income_serializer.save(user=instance.user.id, project=instance)
    #             income_instances.append(income_instance)
    #     if 'expenses' in request.data:
    #         expenses_data = request.data.pop('expenses')
    #         for expense in expenses_data:
    #             expenses_serializer = TodoExpensesSerializer(data=expense)
    #             expenses_serializer.is_valid(raise_exception=True)
    #             expenses_instance = expenses_serializer.save(user=instance.user.id, project=instance)
    #             expenses_instances.append(expenses_instance)
    #
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     if income_instances:
    #         instance.income.add(*[income.id for income in income_instances])
    #     if expenses_instances:
    #         instance.expenses.add(*[expense.id for expense in expenses_instances])
    #
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #
    #     return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.update_done(request, *args, **kwargs)

    def update_done(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        request.data['done'] = not instance.done
        if request.data['done'] == True and instance.tasks_list != []:
            for task in instance.tasks_list.all():
                task.done = True
                for item in task.desc_list:
                    item.done = True
                    item.save()
                task.save()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProjectUpdateView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):
    serializer_class = ProjectSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        # Обработка вложенных данных
        nested_data_fields = {
            # 'desc_list': TodoItemSerializer,
            'income': TodoIncomeSerializer,
            'expenses': TodoExpensesSerializer
        }
        for field_name, serializer_class in nested_data_fields.items():
            self._process_nested_data(field_name, serializer_class, instance, request)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def _process_nested_data(self, field_name, serializer_class, instance, request):
        if field_name in request.data:
            nested_data = request.data.pop(field_name)
            for item_data in nested_data:
                item_serializer = serializer_class(data=item_data)
                item_serializer.is_valid(raise_exception=True)
                item_instance = item_serializer.save(user=instance.user, project=instance)
                getattr(instance, field_name).add(item_instance)


class ProjectDeleteView(generics.GenericAPIView, mixins.DestroyModelMixin):
    serializer_class = ProjectSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PlannerListView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = PlannerSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Planner.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        # Получение первого планировщика пользователя
        instance = self.get_queryset().first()

        # Получение всех проектов и задач пользователя
        all_projects = Project.objects.filter(user=self.request.user)
        all_tasks = TodoTask.objects.filter(user=self.request.user)

        # Обновление проектов и задач в планировщике
        instance.projects.set(all_projects)
        instance.tasks.set(all_tasks)

        # Обновление общих сумм доходов и расходов
        total_income = sum(project.total_income for project in all_projects if project.total_income)
        total_expenses = sum(project.total_expenses for project in all_projects if project.total_expenses)
        instance.total_income = total_income
        instance.total_expenses = total_expenses
        instance.save()

        # Получение сериализованных данных
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CombinedListView(generics.GenericAPIView):
    permission_classes = [IsAuthenticatedCustom]

    def get_todo_tasks(self):
        return TodoTask.objects.filter(user=self.request.user)

    def get_projects(self):
        return Project.objects.filter(user=self.request.user)

    def parse_dates(self, t_delta):
        if len(t_delta) < 11:
            due_date = datetime.strptime(t_delta, '%d.%m.%Y')
            due_date = make_aware(due_date)
            start_of_day = due_date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)
            return start_of_day, end_of_day
        else:
            date_range = t_delta.split(',')
            start_date = datetime.strptime(date_range[0], '%d.%m.%Y')
            end_date = datetime.strptime(date_range[1], '%d.%m.%Y')
            start_date = make_aware(start_date)
            end_date = make_aware(end_date)
            return start_date, end_date

    def get(self, request, *args, **kwargs):
        t_delta = self.request.query_params.get('timedelta')

        if t_delta:
            start_date, end_date = self.parse_dates(t_delta)

            tasks = self.get_todo_tasks().filter(date_end__range=[start_date, end_date])
            projects = self.get_projects().filter(date_end__range=[start_date, end_date])
        else:
            tasks = self.get_todo_tasks()
            projects = self.get_projects()

        task_serializer = TodoTaskSerializer(tasks, many=True)
        project_serializer = ProjectSerializer(projects, many=True)

        return Response({
            'tasks': task_serializer.data,
            'projects': project_serializer.data
        })


