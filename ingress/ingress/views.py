import datetime
from itertools import cycle, zip_longest
from django.db.models import Sum
from django.utils.timezone import now
from django.http import HttpResponse, Http404
from django.shortcuts import render
from .models import Player, Portal, Action, MU


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
    context['actions'] = Action.objects.filter(player__id=pid).order_by('-added')[:100]
    return render(request, "ingress/actions.html", context)


def actions_portal(request, guid):
    context = {}
    try:
        context['portal'] = Portal.objects.get(guid=guid)
    except Portal.DoesNotExist:
        raise Http404()
    context['actions'] = Action.objects.filter(portal__guid=guid).order_by('-added')[:100]
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


def mus(request):
    n = now()
    dt = datetime.datetime(n.year, n.month, 1, 0, 0, 0)
    count_E = MU.objects.filter(team='E', added__gt=dt).aggregate(points=Sum('points'))['points']
    count_R = MU.objects.filter(team='R', added__gt=dt).aggregate(points=Sum('points'))['points']
    context = {
        'count_E': count_E,
        'count_E_with_comma': '{:,d}'.format(count_E),
        'count_R': count_R,
        'count_R_with_comma': '{:,d}'.format(count_R),
        'title': 'MUs',
        'mus_now': n,
        'is_mus': True,
    }
    return render(request, "ingress/vs.html", context)


def search(request):
    context = {}
    if request.method == "POST":
        text = request.POST.get('name_to_search', '')[:40]
        players = Player.objects.filter(id__icontains=text)[:40] or ['']
        portals = Portal.objects.filter(name__icontains=text)[:40] or ['']
        #result = zip(players, cycle(portals)) if len(players) > len(portals) else zip(cycle(players), portals)
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


def about(request):
    return render(request, "ingress/about.html")
