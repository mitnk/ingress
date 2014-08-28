from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='ingress_home'),

    url(r'^actions/$', views.actions, name='ingress_actions'),
    url(r'^actions/player/(\w+)/$', views.actions_player, name='ingress_actions_player'),
    url(r'^actions/portal/([\.\w]+)/$', views.actions_portal, name='ingress_actions_portal'),
    url(r'^actions/portal/([\.\w]+)/(\w+)/$', views.actions_portal, name='ingress_actions_portal_action'),

    url(r'^portals/$', views.portals, name='ingress_portals'),
    url(r'^portals/popular/$', views.portals_popular, name='ingress_portals_popular'),
    url(r'^portals/lv8/$', views.portals_lv8, name='ingress_portals_lv8'),
    url(r'^portals/beijing_does_not_have_long_time_portals/enlightened/$', views.portals_long_time_hold_enlightened, name='ingress_portals_long_time_hold_enlightened'),
    url(r'^portals/beijing_has_long_time_portals/resistance/$', views.portals_long_time_hold_resistance, name='ingress_portals_long_time_hold_resistance'),
    url(r'^portals/([\.\w]+)/$', views.portal_detail, name='ingress_portal_detail'),

    url(r'^players/$', views.players, name='ingress_players'),
    url(r'^players/over_lv8/$', views.players_over_lv8, name='ingress_players_over_lv8'),
    url(r'^players/top/$', views.players_top, name='ingress_players_top'),

    url(r'^mus/$', views.mus, name='ingress_mus'),
    url(r'^search/$', views.search, name='ingress_search'),
    url(r'^messages/$', views.messages, name='ingress_messages'),
    url(r'^about/$', views.about, name='ingress_about'),

    # this should be removed in the future
    url(r'^maps/([\.\w]+)/$', views.portal_detail, name='ingress_maps'),
)
