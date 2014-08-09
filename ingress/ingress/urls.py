from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='ingress_home'),
    url(r'^actions/$', views.actions, name='ingress_actions'),
    url(r'^actions/player/(\w+)/$', views.actions_player, name='ingress_actions_player'),
    url(r'^actions/portal/([\.\w]+)/$', views.actions_portal, name='ingress_actions_portal'),
    url(r'^portals/$', views.portals, name='ingress_portals'),
    url(r'^players/$', views.players, name='ingress_players'),
    url(r'^players/over_lv8/$', views.players_over_lv8, name='ingress_players_over_lv8'),
    url(r'^mus/$', views.mus, name='ingress_mus'),
    url(r'^search/$', views.search, name='ingress_search'),
    url(r'^maps/([\.\w]+)/$', views.maps, name='ingress_maps'),
)
