from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from users.forms import UserForm
from django.contrib.auth.models import User
# from django.views.generic.detail import DetailView
from django.views import View
from .forms import UserForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def signup(request):
    # 계정생성
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save() # 유효성 검사를 통과하면 폼을 DB에 저장
            username = form.cleaned_data.get('username') # cleaned_Data는 사전
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) # 암호화시켜서 저장
            login(request, user) # 로그인 된 걸로 처리한다
            return redirect('index') # 메인 페이지
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

# @login_required
# def profile(request):
#     return render(request, 'common/profile.html')

# class ProfileView(DetailView):
#     context_object_name = 'profile_user'
#     model = User
#     template_name = 'common/profile.html'

@login_required(login_url='users:login')
def profile(request, pk):
    user = get_object_or_404(User, pk=pk)
    context = {"profile_user": user}
    return render(request, 'common/profile.html', context)

class ProfileUpdateView(View):
    # 프로필 편집에서 보여주기위한 get 메소드
    
    def get(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        user_form = UserForm(initial={
            'username': user.username,
            'email': user.email,
        })

        if hasattr(user, 'profile'):
            profile = user.profile
            profile_form = ProfileForm(initial={
                'address': profile.address,
                'avatar': profile.avatar,
                'phone': profile.phone,
                'Mobile': profile.Mobile,
                'Git_url': profile.Git_url,
                'Twit_url': profile.Twit_url,
                'Ins_url': profile.Ins_url,
                'face_url': profile.face_url,
            })
        else:
            profile_form = ProfileForm()

        return render(request, 'common/profile_update.html', {"user_form": user_form, "profile_form": profile_form})

    def post(self, request):
        u = User.objects.get(id=request.user.pk)        
        user_form = UserForm(request.POST, instance=u)
          
        # User 폼
        if user_form.is_valid() :
            user_form.save()
            update_session_auth_hash(request, u)

        if hasattr(u, 'profile'):
            profile = u.profile
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile) 
        else:
            profile_form = ProfileForm(request.POST, request.FILES) 

        # Profile 폼
        if profile_form.is_valid():
            profile = profile_form.save() 
            profile.user = u
            profile.save()
        
        return redirect('users:profile', pk=request.user.pk)

def scheduler(request):
    return render(request, 'common/scheduler.html')

def member(request):
    return render(request, 'common/member.html')




# @login_required
# def ProfileUpdateView(request):
#     if request.method == "POST":
#         form = ProfileForm(request.POST)
#         if form.is_valid():
#             """
#             현재 유저의 프로필을 가져오고
#             받은 값으로 프로필을 갱신한다.
#             """
#             old_profile = request.user.profile
#             old_profile.address = form.cleaned_data['address']
#             old_profile.phone = form.cleaned_data['phone']
#             old_profile.Mobile = form.cleaned_data['Mobile']
#             old_profile.Git_url = form.cleaned_data['Git_url']
#             old_profile.Twit_url = form.cleaned_data['Twit_url']
#             old_profile.Ins_url = form.cleaned_data['Ins_url']
#             old_profile.face_url = form.cleaned_data['face_url']

#             old_profile.save()
#             return redirect('users:profile', pk=request.user.pk)
            
#     elif request.method == "GET":
#         form = ProfileForm(instance=request.user.profile)
#         return render(request, 'common/profile_update.html', {
#             'user_form': form,
#         })