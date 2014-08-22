import datetime
from itertools import cycle, zip_longest
from django.db.models import Sum
from django.utils.timezone import now
from django.http import HttpResponse, Http404
from django.shortcuts import render
from .models import Player, Portal, Action, MU, Message


def home(request):
    context = {}
    context['player_count'] = Player.objects.count()
    context['portal_count'] = Portal.objects.count()
    context['action_count'] = Action.objects.count()
    return render(request, "ingress/home.html", context)


def actions(request):
    pid = request.GET.get('pid')
    context = {}
    if pid:
        context['actions'] = Action.objects.filter(player__id=pid).order_by('-added')[:100]
    else:
        context['actions'] = Action.objects.order_by('-added')[:100]
    return render(request, "ingress/actions.html", context)


def actions_player(request, pid):
    context = {}
    try:
        context['player'] = Player.objects.get(id=pid)
    except Player.DoesNotExist:
        raise Http404()
    context['actions'] = Action.objects.filter(player__id=pid).order_by('-added')[:100]
    return render(request, "ingress/actions.html", context)


def actions_portal(request, guid, action_name=None):
    context = {}
    try:
        context['portal'] = Portal.objects.get(guid=guid)
    except Portal.DoesNotExist:
        raise Http404()
    kwargs = {'portal__guid': guid}
    if action_name:
        kwargs['name'] = action_name
    context['actions'] = Action.objects.filter(**kwargs).order_by('-added')[:100]
    return render(request, "ingress/actions.html", context)


def portals(request):
    count_E = Portal.objects.filter(team='E').count()
    count_R = Portal.objects.filter(team='R').count()
    context = {
        'count_E': count_E,
        'count_R': count_R,
        'title': 'Portals',
    }
    return render(request, "ingress/vs.html", context)


def portals_lv8(request):
    portals = Portal.objects.filter(level=8)
    context = {'portals': portals}
    return render(request, "ingress/portals_lv8.html", context)


def players(request):
    count_E = Player.objects.filter(team='E').count()
    count_R = Player.objects.filter(team='R').count()
    context = {
        'count_E': count_E,
        'count_R': count_R,
        'title': 'Players',
    }
    return render(request, "ingress/vs.html", context)


def players_over_lv8(request):
    list_E = Player.objects.filter(team='E', over_lv8=True).order_by('id')
    list_R = Player.objects.filter(team='R', over_lv8=True).order_by('id')
    context = {}
    result = zip_longest(list_E, list_R)
    context['result'] = result
    return render(request, "ingress/players_over_lv8.html", context)


def players_top(request):
    d = now()
    dt = datetime.datetime(d.year, d.month, 1, 0, 0, 0)
    info_E = MU.objects.filter(team='E', added__gt=dt).values('player')
    info_E = info_E.annotate(tpoints=Sum('points')).order_by('-tpoints')[:50]
    info_R = MU.objects.filter(team='R', added__gt=dt).values('player')
    info_R = info_R.annotate(tpoints=Sum('points')).order_by('-tpoints')[:50]
    result = zip_longest(info_E, info_R)
    context = {'result': result, 'd': d}
    return render(request, "ingress/players_top.html", context)


def mus(request):
    d = now()
    dt = datetime.datetime(d.year, d.month, 1, 0, 0, 0)
    count_E = MU.objects.filter(team='E', added__gt=dt).aggregate(points=Sum('points'))['points']
    count_R = MU.objects.filter(team='R', added__gt=dt).aggregate(points=Sum('points'))['points']
    context = {
        'count_E': count_E,
        'count_E_with_comma': '{:,d}'.format(count_E),
        'count_R': count_R,
        'count_R_with_comma': '{:,d}'.format(count_R),
        'title': 'MUs',
        'mus_now': d,
        'is_mus': True,
    }
    return render(request, "ingress/vs.html", context)


def search(request):
    context = {}
    if request.method == "POST":
        text = request.POST.get('name_to_search', '')[:40]
        players = Player.objects.filter(id__icontains=text)[:40] or ['']
        portals = Portal.objects.filter(name__icontains=text) \
            .exclude(has_problem=True)[:40] or ['']
        result = zip_longest(players, portals)
        context['result'] = result
    return render(request, "ingress/search.html", context)


def portal_detail(request, guid):
    context = {}
    try:
        context['portal'] = Portal.objects.get(guid=guid)
    except Portal.DoesNotExist:
        raise Http404()
    return render(request, "ingress/portal_detail.html", context)


def portals_popular(request):
    context = {}
    context['result'] = Portal.objects.order_by('-capture_count')[:50]
    return render(request, "ingress/portals_popular.html", context)


def portals_long_time_hold_enlightened(request):
    context = {}
    result = Portal.objects.filter(team='E').exclude(last_captured=None).order_by('last_captured')[:100]
    others = Portal.objects.filter(team='E', last_captured=None)
    try:
        context['max_days_tracked'] = result[0].get_hold_days()
    except:
        context['max_days_tracked'] = 0
    context['result'] = result
    context['others'] = others
    context['team'] = 'E'
    return render(request, "ingress/portals_long_time_hold.html", context)


def portals_long_time_hold_r(request):
    context = {}
    result = Portal.objects.filter(team='R').exclude(last_captured=None).order_by('last_captured')[:100]
    others = Portal.objects.filter(team='R', last_captured=None)
    try:
        context['max_days_tracked'] = result[0].get_hold_days()
    except:
        context['max_days_tracked'] = 0
    context['result'] = result
    context['others'] = others
    context['team'] = 'R'
    return render(request, "ingress/portals_long_time_hold.html", context)


def about(request):
    return render(request, "ingress/about.html")


def messages(request):
    context = {}
    dt = now() - datetime.timedelta(days=7)
    timestamp = dt.replace(tzinfo=datetime.timezone.utc).timestamp()
    result = Message.objects.filter(
        timestamp__gt=timestamp * 1000,
        is_secure=False,
    ).order_by('-timestamp')
    context['result'] = result
    return render(request, "ingress/messages.html", context)
