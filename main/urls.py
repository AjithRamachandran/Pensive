from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:tab>/', views.index, name='tags_tab'),
    path('<int:tab>/', views.index, name='users_tab'),
    path('sort/<str:sort_by>/', views.index, name='sort'),
    path('<int:tab>/<slug:tag_slug>/', views.index, name='tags'),
    path('<int:tab>/<slug:tag_slug>/<str:tag_sort_by>/', views.index, name='tags_sort'),
    path('questions/<int:question_id>/', views.details, name='details'),
    path('search/', views.search, name='search'),
    path('add_question/', views.add_question, name='add_question'),
    path('add_question/adding', views.adding_question, name="adding_question"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('feedback/', views.feedback, name='feedback'),
    path('send_feedback/', views.send_feedback, name='send_feedback'),
    path('<int:question_id>/add_answer/adding/', views.adding_answer, name='adding'),
    path('<int:question_id>/upvote', views.upvote, name='upvote'),
    path('<int:question_id>/<int:answer_id>/upscore', views.upscore, name='upscore'),
    path('<int:user_id>/dashboard', views.dashboard, name='dashboard'),
    path('<int:user_id>/edit_profile', views.edit_profile, name='edit_profile'),
]