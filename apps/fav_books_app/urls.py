from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^books$', views.books),
    url(r'^add_book$', views.add_book),
    url(r'^books/(?P<id>\d+)$', views.book_session),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^update/(?P<id>\d+)$', views.update),
    url(r'^logout$', views.logout),
    url(r'^add_book_to_fav/(?P<id>\d+)$', views.add_book_to_fav),
    url(r'^unfav/(?P<id>\d+)$', views.unfavorite),



    # url(r'^books/(?P<id>\d+)$', views.),



]
