from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from ..models import Question

# view 함수의 첫 번째 인자는 request

def index(request):

    # # 사전을 통해 question_list를 담는다.
    # # context에 따라 홈페이지에 표시되는게 달라진다.

    # 입력 파라미터
    page = request.GET.get('page', '1') # 페이지 디폴트 값은 1
    # 조회
    question_list = Question.objects.order_by('-create_date')
    total_count = Question.objects.count()
    # 페이징처리
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page) # get 페이지에서 내가 원하는 페이지만 추출
    context = {
        'question_list': page_obj,
        'total_count' : total_count
        }
    
    return render(request, 'board/question_list.html', context)

    # 외부환경요소 : context
    # 렌더링을 통해 브라우저에 나타냄

def detail(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    context = {'question' : question}
    return render(request, 'board/question_detail.html', context)
