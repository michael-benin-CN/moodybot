# -*- coding: utf8 -*-

from __future__ import unicode_literals

import grequests

from pyaib.plugins import every, plugin_class


@plugin_class('reddit')
class RedditTailer(object):
    def __init__(self, ctx, config):
        self.subreddits = config.subreddits
        self.latest = None
        self.channels = config.channels or ctx.channels.channels

    @every(5 * 60, 'tail-reddit')
    def tail_reddit(self, ctx, name):
        responses = grequests.map([
            grequests.get('http://www.reddit.com/r/{subreddit}/new.json'.format(subreddit=subreddit))
            for subreddit in self.subreddits
        ])

        for res in responses:
            data = res.json()['data']
            posts = []

            if self.latest is None:
                posts.append(data['children'][0]['data'])
            else:
                is_new_enough = True
                _i = 0

                while is_new_enough:
                    child = data['children'][_i]
                    is_new_enough = float(child['data']['created']) > self.latest
                    if is_new_enough:
                        posts.append(child['data'])
                        _i += 1

            posts = sorted(posts, key=lambda p: p['created'])
            posts.reverse()

            if len(posts) > 0:
                self.latest = float(posts[0]['created'])

            posts.reverse()
            for channel in self.channels:
                for post in posts:
                    score = post['score']
                    title = post['title']
                    u = post['author']
                    r = post['subreddit']
                    url = post['url']
                    ctx.PRIVMSG(channel, '^v {score} {title} submitted by {u} to {r} {url}'.format(
                        score=score, title=title, u=u, r=r, url=url
                    ))
