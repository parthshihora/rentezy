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
    url(r'^delete_answer/(?P<object_id>.*)', views.objectDelete, name='delete_object'),
    url(r'^modify/(?P<object_id>.*)', views.modifyCar, name='modify_car'),
    url(r'^allcars/$', views.allCars, name='allcars'),
    url(r'^reserve/(?P<object_id>.*)', views.make_reservation, name='reserve'),
    url(r'^myreservations/$', views.my_reservations, name='myreservations'),
    url(r'^filtercars/$', views.filteredcars, name='filteredcars')

]