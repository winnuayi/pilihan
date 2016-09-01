from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy
from django.core.validators import validate_email
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.text import slugify
from django.views.generic import View

from topics.models import Answer, Category, Choice, CustomUser, Question

import simplejson as json


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']

        # check parameters
        if len(email) == 0 or len(password) == 0:
            context = {
                'error_message': "Isian tidak lengkap"
            }
            return render(request, 'login.html', context)

        # check email format
        try:
            validate_email(email)
        except ValidationError:
            context = {
                'error_message': "Format email salah"
            }
            return render(request, 'login.html', context)

        # check whether user is registered
        user = authenticate(username=email, password=password)
        if user is None:
            context = {
                'error_message': "Kombinasi email dan password tidak cocok"
            }
            return render(request, 'login.html', context)

        login(request, user)

        return HttpResponseRedirect(reverse_lazy('feed'))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('login'))


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

        # check parameters
        if len(email) == 0 or len(password) == 0 or len(confirm) == 0:
            context = {
                'email': email,
                'password': password,
                'confirm': confirm,
                'error_message': "Isian tidak lengkap"
            }
            return render(request, 'register.html', context)

        # check email format
        try:
            validate_email(email)
        except ValidationError:
            context = {
                'password': password,
                'confirm': confirm,
                'error_message': "Format email salah"
            }
            return render(request, 'register.html', context)

        # check password and confirm match
        if password != confirm:
            context = {
                'email': email,
                'error_message': "Password dan konfirmasi tidak cocok"
            }
            return render(request, 'register.html', context)

        # check user has been registered
        try:
            CustomUser.objects.get(email=email)
            context = {
                'password': password,
                'confirm': confirm,
                'error_message': "Email telah terdaftar"
            }
            return render(request, 'register.html', context)
        except CustomUser.DoesNotExist:
            pass

        # create new user
        user = CustomUser(email=email, password=make_password(password))
        user.save()

        login(request, user)

        return HttpResponseRedirect(reverse_lazy('feed'))


class FeedView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.all().order_by('name')
        questions = self.get_questions()
        context = {
            'fullname': request.user.fullname,
            'categories': categories,
            'questions': questions
        }
        return render(request, 'feed.html', context)

    def get_questions(self):
        questions = Question.objects.all().order_by('-created_at')
        return questions


class AskView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'ask.html')

    def post(self, request):
        question = request.POST['question']

        # check question
        if not self.validate_question(question):
            response = {
                'success': -1,
                'message': "Pertanyaan terlalu singkat"
            }
            return HttpResponse(json.dumps(response),
                                content_type='application/json') 

        # insert question to database
        q = Question(question=question,
                     user=request.user,
                     slug=slugify(question))
        q.save()

        response = { 'success': 0 }
        return HttpResponse(json.dumps(response),
                            content_type='application/json') 

    def validate_question(self, question):
        THRESHOLD = 3

        token = question.split(' ')
        if len(token) < THRESHOLD:
            return False
        return True


class QuestionView(LoginRequiredMixin, View):
    def get(self, request, slug):
        q = Question.objects.get(slug=slug)

        is_follow = 0
        if request.user in q.followers.all():
            is_follow = 1

        is_downvote = 0
        if request.user in q.downvoters.all():
            is_downvote = 1

        self.increment_view(q)

        answers = Answer.objects.filter(question=q).order_by('-created_at')

        context = {
            'question': q,
            'answers': answers,
            'answer_count': len(answers),
            'is_follow': is_follow,
            'is_downvote': is_downvote,
        }

        return render(request, 'question.html', context)

    def post(self, request, slug):
        answer = request.POST['answer']
        if len(answer) == 0:
            response = { 'success': -1, 'message': 'Jawaban kosong' }
            return HttpResponse(json.dumps(response),
                                content_type='application/json') 

        # if len(answer) <= 140:
        #     response = { 'success': -1, 'message': 'Jawaban terlalu singkat' }
        #     return HttpResponse(json.dumps(response),
        #                         content_type='application/json') 

        q = Question.objects.get(slug=slug)

        a = Answer(question=q, answer=answer, creator=request.user)
        a.save()

        response = {
            'success': 0,
            'data': {
                'fullname': request.user.fullname,
                'answer': answer,
                'created_at': a.created_at.isoformat()
            }
        }

        return HttpResponse(json.dumps(response),
                            content_type='application/json') 

    def increment_view(self, q):
        # increase view counter
        q.view = q.view + 1
        q.save()
