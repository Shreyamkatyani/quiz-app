from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Question
from .forms import SignupForm
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'quiz/home.html'
# quiz/views.py


class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically login after signup
            return redirect('quiz')  # Change to your homepage/quiz page
        return render(request, 'registration/signup.html', {'form': form})


#  Quiz View (TemplateView with login protection)
class QuizView(LoginRequiredMixin, TemplateView):
    template_name = 'quiz/quiz.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = Question.objects.all()
        return context

#  Submit Quiz View (View + POST logic)
class SubmitQuizView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        questions = Question.objects.all()
        score = 0

        for question in questions:
            selected = request.POST.get(str(question.id))
            if selected:
                try:
                    selected_choice = question.choices.get(id=selected)
                    if selected_choice.is_correct:
                        score += 1
                except:
                    pass  # ignore bad data

        return render(request, 'quiz/result.html', {
            'score': score,
            'total': questions.count()
        })

    def get(self, request):
        return redirect('quiz')
