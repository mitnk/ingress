import re
from django import template
from .. import models


_CACHE = {}
register = template.Library()


def ParseReplyProc(res):
    pid = res.group('pid')
    if pid[1:] in _CACHE:
        team = _CACHE[pid[1:]]
    else:
        team = models.Player.get_team(pid[1:])
        _CACHE[pid[1:]] = team
    if team == 'N':
        return '<span class="c-{}">{}</span>'.format(team, pid)
    else:
        return '<a href="/actions/player/{}/"><span class="c-{}">{}</span></a>'.format(pid[1:], team, pid)


@register.filter
def parse_agent_message(value):
    if not value:
        return value
    p1 = re.compile(r'(?P<pid>@[a-zA-Z0-9_]+)', re.VERBOSE)
    value = p1.sub(ParseReplyProc, value)
    return value
