from __future__ import unicode_literals

from pyaib.plugins import keyword, plugin_class

@plugin_class('source')
class PugMe(object):
    def __init__(self, irc_context, config):
        pass

    @keyword('sauce')
    @keyword('source')
    def print_sauce(self, irc_c, msg, trigger, args, kargs):
        msg.reply('https://github.com/jesusabdullah/moodybot')

