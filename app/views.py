from django.core import exceptions
from django.db import transaction
from django.http import Http404
from rest_framework import status, views
from rest_framework.response import Response

from .models import Choice, Product, Question
from .serializers import ProductSerializer, QuestionSerializer


class SampleApi(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response({"status": "OK"}, status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return Response(request.data, status.HTTP_201_CREATED)


class QuestionApi(views.APIView):
    def get(self, request, *args, **kwargs):
        query = Question.objects.all()
        serializer = QuestionSerializer(instance=query, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        serializer = QuestionSerializer(instance=instance)
        return Response(serializer.data, status.HTTP_201_CREATED)


class QuestionDetailApi(views.APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            instance: Question = Question.objects.prefetch_related("choices").get(pk=pk)
            choices_instance = instance.choices.all()
            for choice_instance in choices_instance:
                print(choice_instance.id)

        except exceptions.ObjectDoesNotExist:
            raise Http404("Data Not Found")

        serializer = QuestionSerializer(instance=instance)
        return Response(exclude_null(serializer.data), status.HTTP_200_OK)

    @transaction.atomic
    def patch(self, request, pk, *args, **kwargs):
        try:
            instance = Question.objects.get(pk=pk)
        except exceptions.ObjectDoesNotExist:
            raise Http404("Data Not Found")
        serializer = QuestionSerializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        serializer = QuestionSerializer(instance=instance)
        return Response(exclude_null(serializer.data), status.HTTP_200_OK)

    @transaction.atomic
    def delete(self, request, pk, *args, **kwargs):
        instance = Question.objects.get(pk=pk)
        serializer = QuestionSerializer(instance=instance)
        id = serializer.delete()

        return Response(id, status.HTTP_200_OK)


class ProductApi(views.APIView):
    def get(self, request, *args, **kwargs):
        query_parameter = request.GET
        print(query_parameter)
        print(kwargs)
        print(args)
        query = Product.objects.all()
        serializer = ProductSerializer(instance=query, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        serializer = ProductSerializer(instance=instance)
        return Response(serializer.data, status.HTTP_201_CREATED)


class ProductDetailApi(views.APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            instance = Product.objects.get(pk=pk)
        except exceptions.ObjectDoesNotExist:
            raise Http404("Data Not Found")
        serializer = ProductSerializer(instance=instance)

        return Response(exclude_null(serializer.data), status.HTTP_200_OK)

    @transaction.atomic
    def patch(self, request, pk, *args, **kwargs):
        try:
            instance = Product.objects.get(pk=pk)
        except exceptions.ObjectDoesNotExist:
            raise Http404("Data Not Found")
        serializer = ProductSerializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        serializer = ProductSerializer(instance=instance)
        return Response(exclude_null(serializer.data), status.HTTP_200_OK)

    @transaction.atomic
    def delete(self, request, pk, *args, **kwargs):
        instance = Product.objects.get(pk=pk)
        serializer = ProductSerializer(instance=instance)
        id = serializer.delete()

        return Response(id, status.HTTP_200_OK)


def exclude_null(d):
    def empty(x):
        return x is None

    if not isinstance(d, (dict, list)):
        return d
    elif isinstance(d, list):
        return [v for v in (exclude_null(v) for v in d) if not empty(v)]
    else:
        return {k: v for k, v in ((k, exclude_null(v)) for k, v in d.items()) if not empty(v)}
