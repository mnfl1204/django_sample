from rest_framework import serializers
from rest_framework.utils import model_meta

from app import models


class BaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    def nest_create(self, **fk_instances):
        ModelClass = self.Meta.model
        instance = ModelClass._default_manager.create(**fk_instances, **self.initial_data)
        return instance

    def nest_update(self, **fk_instances):
        info = model_meta.get_field_info(self.instance)
        for attr in info.relations:
            if attr in self.initial_data:
                self.initial_data.pop(attr)
        instance = self.update(self.instance, self.initial_data, **fk_instances)
        return instance

    def nest_delete(self):
        deleted_id = self.instance.id
        self.instance.delete()
        return deleted_id


class ChoiceSerializer(BaseSerializer):
    question_id = serializers.IntegerField(source="question.id", required=False)

    class Meta:
        model = models.Choice
        exclude = ["question"]


class QuestionSerializer(BaseSerializer):
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = models.Question
        fields = "__all__"

    def create(self, validated_data):
        choice_list = validated_data.pop("choices") if "choices" in self.initial_data else None
        # Question
        question_instance = models.Question.objects.create(**validated_data)
        # Choice
        if choice_list is not None:
            for data in choice_list:
                ChoiceSerializer(data=data).nest_create(question=question_instance)
        return question_instance

    def update(self, instance, validated_data):
        # Choice
        if "choices" in validated_data:
            choice_list = validated_data.pop("choices")
            choice_instance_list = instance.choices.all()
            for choice_instance in choice_instance_list:
                for data in choice_list:
                    if "id" in data and choice_instance.id == data["id"]:
                        ChoiceSerializer(choice_instance, data).nest_update()
                        choice_list.remove(data)
                        break
                else:
                    ChoiceSerializer(choice_instance).nest_delete()
            for data in choice_list:
                if "id" not in data:
                    if "question" in data:
                        question = data.pop("question")
                        if question["id"] != instance.id:
                            raise serializers.ValidationError("choice.question_id cannot be changed")
                    ChoiceSerializer(data=data).nest_create(question=instance)

                else:
                    id = data["id"]
                    raise serializers.ValidationError(f"choice.id cannot be chenge(choice.id={id})")
        # Question
        question_instance = super().update(instance, validated_data)

        return question_instance

    def delete(self):
        question_id = self.instance.id
        self.instance.delete()
        return question_id


class ProductSerializer(BaseSerializer):
    # orders = OrderSerializer(many=True, required=False)
    class Meta:
        model = models.Product
        fields = "__all__"
