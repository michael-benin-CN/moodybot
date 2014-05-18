from __future__ import unicode_literals

import grequests

from pyaib.plugins import keyword, plugin_class

@plugin_class('pug')
class PugMe(object):
    def __init__(self, irc_context, config):
        pass

    # See: https://github.com/github/hubot/blob/master/src/scripts/pugme.coffee

    @keyword('pugme')
    @keyword.autohelp
    def getPug(self, irc_c, msg, trigger, args, kargs):
        """:: You need more small yappy dogs in your life."""
        res = grequests.map([grequests.get('http://pugme.herokuapp.com/random')])[0]
        msg.reply(res.json()['pug'])

    @keyword('pugbomb')
    @keyword.autohelp
    def pugBomb(self, irc_c, msg, trigger, args, kwargs):
        """:: You need WAY more small yappy dogs in your life!"""
        res = grequests.map([grequests.get('http://pugme.herokuapp.com/bomb?count=5')])[0]

        for pug in res.json()['pugs']:
            msg.reply(pug)

