from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.contrib import messages
from django.utils.safestring import mark_safe
import calendar
from django.contrib.auth.decorators import login_required

from .models import *
from .utils import Calendar
from .forms import EventForm

def index(request):
    return HttpResponse('hello')

class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    context = {'event' : event}
    return render(request, 'cal/event_detail.html', context)


@login_required(login_url='users:login')
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False) # 모델에 저장
            event.author = request.user
            event.save() # DB에 저장
            return redirect('cal:calendar')
    # get
    else:
        form = EventForm()
    
    context = {'form': form}
    return render(request, 'cal/event_form.html', context)

@login_required(login_url='users:login')
def event_modify(request, event_id):
    # 수정
    event = get_object_or_404(Event, pk=event_id)
    if request.method == "POST":
        # 질문 수정을 위해 값 덮어쓰기
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            event.author = request.user
            event.save()
            return redirect('cal:detail', event_id=event.id)
    else:
        # 질문 수정 화면에 기존 제목, 내용 반영
        form = EventForm(instance=event)
        context = {'form': form}
        return render(request, 'cal/event_form.html', context)

@login_required(login_url='users:login')
def event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.user != event.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('cal:detail', event_id=event.id)

    event.delete()
    return redirect('cal:calendar')