import json
from taggit.models import Tag

from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail

from .forms import AddQuestionForm, AddAnswerForm, CreateUserForm, CreateProfileForm, UpdateUserForm, UpdateProfileForm

from .models import Question, Answer, Vote, Score


def index(request, tag_slug=None, sort_by=None, tag_sort_by=None, tab=0):
    tag = None
    page_obj = None
    questions = Question.objects.all()
    if tab==0:
        if sort_by:
            sort_by = '-' + str(sort_by)
            questions = questions.order_by(sort_by)
        paginator = Paginator(questions, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'index.html', {'page_obj': page_obj, 'keyword': "", 'tags': tag, 'tab': tab })
    if tab==1:
        tag = Question.tags.all()
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            questions = questions.filter(tags__in=[tag])
            if tag_sort_by:
                tag_sort_by = '-' + tag_sort_by
                questions = questions.order_by(tag_sort_by)
            paginator = Paginator(questions, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        return render(request, 'index.html', {'page_obj': page_obj, 'keyword': "", 'tags': tag, 'tab': tab })
    if tab==2:
        return render(request, 'index.html', {'page_obj': page_obj, 'keyword': "", 'tags': tag, 'tab': tab })

def details(request, question_id):
    question = get_object_or_404(Question, QuestionId=question_id)
    answers = Answer.objects.filter(ParentId=question_id).order_by('-Score')
    ids = []
    for answer in answers:
        ids.append(answer.OwnerUserId.id)
    users = User.objects.filter(id__in=ids)
    form = AddAnswerForm(request.POST)
    return render(request, 'detail.html', { 'question' : question, 'answers' : answers, 'users': users, 'form': form})

def search(request):        
    if request.method == 'GET':
        keyword =  request.GET.get('search', None)  
        if keyword:
            questions = Question.objects.filter(Title__icontains=keyword)
            if (questions.count() != 0):
                paginator = Paginator(questions, 10)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
                return render(request, 'index.html', {'page_obj': page_obj, 'keyword': keyword})
            else:
                return render(request, 'error.html', {'keyword': keyword})
        else:
            return redirect('/')

@login_required(login_url='main:login')
def feedback(request):
    return render(request, 'feedback.html')

def send_feedback(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    subject = request.POST.get('subject')
    content = str(name) + ':' + str(request.user.id) + ':' + request.POST.get('message')
    send_mail(subject, content, email, ['to@example.com'], fail_silently=False,)
    return redirect('/')


@login_required(login_url='main:login')
def add_question(request):
    form = AddQuestionForm(request.POST)
    return render(request, 'add_question.html', {'form': form})

@login_required(login_url='main:login')
def adding_question(request):
    current_user = request.user
    if request.method == 'POST':
        form = AddQuestionForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.OwnerUserId = User.objects.get(id=current_user.id)
            temp.save()
            form.save_m2m()
            return HttpResponseRedirect(reverse('main:details', args=(temp.QuestionId,)))
    else:
        form = AddQuestionForm(request.POST)
        return render(request, 'add_question.html', {'form': form})

@login_required(login_url='main:login')
def adding_answer(request, question_id):
    ids = []
    current_user = request.user
    if request.method == 'POST':
        form = AddAnswerForm(request.POST)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.OwnerUserId = User.objects.get(id=current_user.id)
            temp.ParentId = Question.objects.get(QuestionId=question_id)
            temp.save()
            question = get_object_or_404(Question, QuestionId=question_id)
            return HttpResponseRedirect(reverse('main:details', args=(question_id,)))
    else:
        form = AddAnswerForm(request.POST)
        question = get_object_or_404(Question, QuestionId=question_id)
        return render(request, 'add_answer.html', { 'question' : question })

@login_required(login_url='main:login')
def upvote(request, question_id):
    question = get_object_or_404(Question, QuestionId=question_id)
    current_user = request.user
    if not (Vote.objects.filter(UserId=current_user, Question=question).exists()):
        question.Score += 1
        question.save()
        Vote.objects.create(UserId=current_user, Question=question)
        return HttpResponseRedirect(reverse('main:details', args=(question_id,)))
    else:
        return HttpResponseRedirect(reverse('main:details', args=(question_id,)))


@login_required(login_url='main:login')
def upscore(request, answer_id, question_id):
    answer = Answer.objects.get(AnswerId=answer_id)
    current_user = request.user
    if not (Score.objects.filter(UserId=current_user, Answer=answer).exists()):
        answer.Score += 1
        answer.save()
        Score.objects.create(UserId=current_user, Answer=answer)
        return HttpResponseRedirect(reverse('main:details', args=(question_id,)))
    else:
        return HttpResponseRedirect(reverse('main:details', args=(question_id,)))

def signup(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = CreateUserForm()
        return render(request, 'signup.html', {'form': form})

def loginUser(request):
    # 509839
    message = ''
    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(request, username=username, password=password)
        except:
            message = 'username/password is wrong'
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('main:index'))
        
        else:
            message = 'Try Again'
    return render(request, 'login.html', {'message' : message})

def logoutUser(request):
    logout(request)
    return HttpResponseRedirect(reverse('main:index'))

@login_required
def edit_profile(request, user_id):
    current_user = request.user
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user, initial={'email': current_user.email,
                                                  'first_name': current_user.first_name,
                                                  'last_name': current_user.last_name})
        profile_form = UpdateProfileForm(request.POST, instance=request.user.profile, initial={'Bio': current_user.profile.Bio,
                                                                                                'Country': current_user.profile.Country})
        print(user_form.is_valid())
        print(profile_form.is_valid())
        if user_form.is_valid() and profile_form.is_valid():
            print('here')
            user_form.save()
            profile_form.save()
            return redirect('main:dashboard', args=(user_id,))
    else:
        user_form = CreateUserForm(instance=request.user)
        profile_form = CreateProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', { 'user_form': user_form, 'profile_form': profile_form })

def dashboard(request, user_id):
    questions = []
    answers = []
    questions_temp = Question.objects.filter(OwnerUserId=request.user)
    answers_temp = Answer.objects.filter(OwnerUserId=request.user)
    for i in range(questions_temp.count()):
        questions.append(questions_temp[i])
    for i in range(answers_temp.count()):
        answers.append(answers_temp[i])
    for question in questions:
        print(question.Body)
    return render(request, 'dashboard.html', {'questions': questions, 'answers': answers})