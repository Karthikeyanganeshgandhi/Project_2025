from django.urls import path
from hubapp import views


urlpatterns = [
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('about/',views.about,name='about'),
    path('price/',views.price,name='price'),
    path('account/',views.account,name='account'),
    path('contact/',views.contact,name='contact'),
    path('coursedet/',views.coursedet,name='coursedet'),
    path('courses/',views.courses,name='courses'),
    path('event/',views.event,name='event'),
    path('ml/',views.ml,name='ml'),
    path('progress/',views.progress,name='progress'),
    path('skilltester/',views.skilltester,name='skilltester'),
    path('subscription/',views.subscription,name='subscription'),
    path('trainers/',views.trainers,name='trainers'),
    path('web/',views.web,name='web'),
    path('testsuccess/',views.testsuccess,name='testsuccess'),
    path('thank_you_view/',views.thank_you_view,name='thank_you_view'),
    path('contacts/', views.contacts, name='contacts'),
]