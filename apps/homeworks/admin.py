from django.contrib import admin
from apps.homeworks.models import Homework, HomeworkSubmission
from common.enums import ModelFields


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = [ModelFields.TITLE.value, ModelFields.LECTURE.value, ModelFields.CREATED_BY.value, ModelFields.DUE_DATE.value, ModelFields.CREATED_AT.value]
    list_filter = [ModelFields.CREATED_AT.value, ModelFields.DUE_DATE.value]
    search_fields = [ModelFields.TITLE.value, ModelFields.DESCRIPTION.value]
    readonly_fields = [ModelFields.CREATED_AT.value, ModelFields.UPDATED_AT.value]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            ModelFields.LECTURE.value, 
            ModelFields.CREATED_BY.value
        )


@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
    list_display = [ModelFields.HOMEWORK.value, ModelFields.STUDENT.value, ModelFields.SUBMITTED_AT.value, ModelFields.IS_SUBMITTED.value]
    list_filter = [ModelFields.SUBMITTED_AT.value, ModelFields.IS_SUBMITTED.value]
    search_fields = [ModelFields.CONTENT.value]
    readonly_fields = [ModelFields.SUBMITTED_AT.value, ModelFields.UPDATED_AT.value]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            ModelFields.HOMEWORK.value, 
            ModelFields.STUDENT.value
        )
