from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question

@login_required(login_url='users:login')
def question_create(request):
    """
    board 질문등록
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False) # 모델에 저장
            question.author = request.user
            question.create_date = timezone.now() # 작성 시간은 폼에서 작성되지 않았기 때문에 따로 만들어줌
            question.save() # DB에 저장
            return redirect('board:index')
    # get
    else:
        form = QuestionForm()
    
    context = {'form': form}
    return render(request, 'board/question_form.html', context)

@login_required(login_url='users:login')
def question_modify(request, question_id):
    # 수정
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author: # 작성자 여부 판단
        messages.error(request, '수정권한이 없습니다')
        return redirect('board:detail', question_id=question.id)

    if request.method == "POST":
        # 질문 수정을 위해 값 덮어쓰기
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now() # 수정일 저장
            question.save()
            return redirect('board:detail', question_id=question.id)
    else:
        # 질문 수정 화면에 기존 제목, 내용 반영
        form = QuestionForm(instance=question)
        context = {'form': form}
        return render(request, 'board/question_form.html', context)

@login_required(login_url='users:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('board:detail', question_id=question.id)

    question.delete()
    return redirect('board:index')