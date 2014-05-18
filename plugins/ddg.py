from __future__ import unicode_literals

import json
import re
from urllib import urlencode

import grequests
from pyaib.plugins import observe, plugin_class


def encode_query(q):
    return urlencode({
        'q': q,
        'format': 'json',
        'no_redirect': '1',
        'no_html': '1'
    })

def query(q):
    request = grequests.get('http://api.duckduckgo.com/?{query}'.format(query=encode_query(q)))
    res = grequests.map([request])[0]

    return res.json()

def stringify_result(data, query):
    def _check(field):
        try:
            return len(data[field]) > 0
        except:
            return False

    lines = []
    if _check('AbstractText'):
        lines.append(data['AbstractText'])
    if _check('AbstractSource') and _check('AbstractURL'):
        lines.append('{src}: {url}'.format(src=data['AbstractSource'], url=data['AbstractURL']))
    if _check('Answer'):
        lines.append('Answer: {ans}'.format(ans=data['Answer']))
    if _check('DefinitionText') and _check('DefinitionURL'):
        lines.append('Definition ( {url} ): {txt}'.format(url=data['DefinitionURL'], txt=data['DefinitionText']))
    if _check('Redirect'):
        lines.append(data['Redirect'])

    if len(lines) == 0:
        lines.append('https://duckduckgo.com/?' + urlencode({ "q": query }))


    return '\n'.join(lines)


@plugin_class('ddg')
class DDG(object):
    def __init__(self, ctx, config):
        self.prefix = config.prefix or '!'
        self._bang_re = re.compile('^' + self.prefix + '\w')
        self._ddg_re = re.compile('^' + self.prefix + 'ddg ')

    @observe('IRC_MSG_PRIVMSG')
    def ddg(self, ctx, msg):
        message = msg.message.strip()

        # TODO: This shouldn't collide with existing commands.
        # existing_commands = ctx.triggers.list()
        # See: https://github.com/facebook/pyaib/blob/master/pyaib/triggers.py#L141-L176

        if self._bang_re.match(message) is not None:
            q = self._ddg_re.sub('', message)
            r = query(q)
            print(ctx.triggers.list())
            msg.reply(stringify_result(r, q))


