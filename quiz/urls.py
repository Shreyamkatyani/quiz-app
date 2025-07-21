from django.urls import path
from .views import SignupView, QuizView, SubmitQuizView, HomeView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),                         # ← New home page
    path('quiz/', QuizView.as_view(), name='quiz'),                    # Quiz page
    path('submit/', SubmitQuizView.as_view(), name='submit_quiz'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
