from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
   	url(r'^startpage/', views.start_page, name='start_page'),
    #url(r'^ownerlogin/', views.OwnerLogin, name='owner_new'),
    #url(r'^login/', views.login_view, name='login'),
    #url(r'^register/', views.register_view, name='register'),
    #url(r'^ownerreg/', views.OwnerRegister, name='owner_reg'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^accounts/profile/$', views.owner_profile, name='owner_page'),
    url(r'^signup/$', views.signup, name='signup'),
	url(r'^yourcars/$', views.your_cars, name='your_cars'),
	url(r'^addcar/$', views.add_car, name='add_car'),
	url(r'^logout/$', views.logout_view, name='logout_view'),
   # url(r'^(?P<object_id>[0-9]+)/delete_answer/$', views.objectDelete, name='delete_object')


]