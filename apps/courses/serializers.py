from rest_framework import serializers
from common.enums import ModelFields, SerializerFields
from apps.courses.models import Course, Lecture
from apps.users.serializers import UserListSerializer
from apps.courses.services import CourseCreationService, CourseUpdateService, CourseCreationRequest, CourseUpdateRequest


class CourseListSerializer(serializers.ModelSerializer):
    primary_owner = UserListSerializer(read_only=True)
    teacher_count = serializers.IntegerField(read_only=True)
    student_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Course
        fields = [
            ModelFields.ID.value, ModelFields.NAME.value, ModelFields.DESCRIPTION.value,
            ModelFields.PRIMARY_OWNER.value,
            SerializerFields.TEACHER_COUNT.value, SerializerFields.STUDENT_COUNT.value,
        ]
        read_only_fields = [ModelFields.ID.value]


class CourseCreateSerializer(serializers.ModelSerializer):
    primary_owner_id = serializers.IntegerField(required=False)
    teacher_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True,
        default=list
    )
    student_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True,
        default=list
    )

    class Meta:
        model = Course
        fields = [
            ModelFields.NAME.value,
            ModelFields.DESCRIPTION.value,
            SerializerFields.PRIMARY_OWNER_ID.value,
            SerializerFields.TEACHER_IDS.value,
            SerializerFields.STUDENT_IDS.value
        ]
        extra_kwargs = {
            SerializerFields.PRIMARY_OWNER_ID.value: {'write_only': True, 'required': False},
            SerializerFields.TEACHER_IDS.value: {'write_only': True},
            SerializerFields.STUDENT_IDS.value: {'write_only': True},
        }

    def to_representation(self, instance):
        """Remove write-only fields from response"""
        data = super().to_representation(instance)
        for field in [SerializerFields.PRIMARY_OWNER_ID.value,
                      SerializerFields.TEACHER_IDS.value,
                      SerializerFields.STUDENT_IDS.value]:
            data.pop(field, None)
        return data

    def create(self, validated_data):
        request_obj = self.context.get('request', None)
        user_obj = request_obj.user if request_obj else None
        authenticated_user_id = user_obj.id if user_obj else None

        request = CourseCreationRequest(
            name=validated_data[ModelFields.NAME.value],
            description=validated_data[ModelFields.DESCRIPTION.value],
            primary_owner_id=authenticated_user_id,
            teacher_ids=validated_data.get(SerializerFields.TEACHER_IDS.value, []),
            student_ids=validated_data.get(SerializerFields.STUDENT_IDS.value, [])
        )

        course_service = CourseCreationService()
        return course_service.create_course(request)


class CourseUpdateSerializer(serializers.ModelSerializer):
    primary_owner_id = serializers.IntegerField(required=False)
    teacher_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True
    )
    student_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True
    )

    class Meta:
        model = Course
        fields = [
            ModelFields.ID.value,
            ModelFields.NAME.value,
            ModelFields.DESCRIPTION.value,
            SerializerFields.PRIMARY_OWNER_ID.value,
            SerializerFields.TEACHER_IDS.value,
            SerializerFields.STUDENT_IDS.value
        ]
        read_only_fields = [ModelFields.ID.value]
        extra_kwargs = {
            SerializerFields.PRIMARY_OWNER_ID.value: {'write_only': True},
            SerializerFields.TEACHER_IDS.value: {'write_only': True},
            SerializerFields.STUDENT_IDS.value: {'write_only': True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in [SerializerFields.PRIMARY_OWNER_ID.value,
                      SerializerFields.TEACHER_IDS.value,
                      SerializerFields.STUDENT_IDS.value]:
            data.pop(field, None)
        return data

    def update(self, instance, validated_data):
        request = CourseUpdateRequest(
            course_id=instance.id,
            name=validated_data.get(ModelFields.NAME.value),
            description=validated_data.get(ModelFields.DESCRIPTION.value),
            primary_owner_id=validated_data.get(SerializerFields.PRIMARY_OWNER_ID.value),
            teacher_ids=validated_data.get(SerializerFields.TEACHER_IDS.value),
            student_ids=validated_data.get(SerializerFields.STUDENT_IDS.value)
        )

        course_service = CourseUpdateService()
        return course_service.update_course(instance, request)


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = [
            ModelFields.ID.value,
            ModelFields.TOPIC.value,
            ModelFields.PRESENTATION.value,
            ModelFields.CREATED_AT.value,
            ModelFields.UPDATED_AT.value,
        ]
        read_only_fields = [ModelFields.ID.value, ModelFields.CREATED_AT.value, ModelFields.UPDATED_AT.value]
