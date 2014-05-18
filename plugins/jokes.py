# Copyright 2013 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import random

from pyaib.plugins import keyword, plugin_class


@plugin_class
class Jokes(object):
    def __init__(self, irc_context, config):
        self.ballresp = config.ballresp

    @keyword('8ball')
    @keyword.autohelp_noargs
    def magic_8ball(self, irc_c, msg, trigger, args, kargs):
        """[question]? :: Ask the magic 8 ball a question."""
        if not msg.message.endswith('?'):
            msg.reply("%s: that does not look like a question to me" %
                      msg.nick)
            return
        msg.reply("%s: %s" % (msg.nick, random.choice(self.ballresp)))

