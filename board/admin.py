from django.contrib import admin
from .models import Question, Answer
# 현재 패키지의 models 모듈

# Register your models here.
# 검색 기능 추가하는 클래스
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']
    list_display = ['id', 'subject', 'create_date']

admin.site.register(Question, QuestionAdmin)

admin.site.register(Answer)
# admin 사이트에 이 모델을 등록