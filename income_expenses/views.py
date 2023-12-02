from test_backend.custom_methods import IsAuthenticatedCustom
from rest_framework import mixins, generics
from .models import WorkIncome, Work, Project
from .serializers import WorkIncomeSerializer, WorkSerializer, ProjectSerializer


class WorkIncomeListView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = WorkIncomeSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return WorkIncome.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class WorkIncomeDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = WorkIncomeSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return WorkIncome.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class WorkIncomeCreateView(mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = WorkIncomeSerializer
    permission_classes = [IsAuthenticatedCustom]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class WorkListView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = WorkSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Work.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class WorkDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = WorkSerializer
    permission_classes = [IsAuthenticatedCustom]


    def get_queryset(self):
        return Work.objects.filter(user=self.request.user)


    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProjectListView(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedCustom]


    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProjectDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedCustom]

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
