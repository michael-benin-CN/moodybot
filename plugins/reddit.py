# -*- coding: utf8 -*-

from __future__ import unicode_literals

import grequests

from pyaib.plugins import every, plugin_class

@plugin_class('reddit')
class RedditTailer(object):
    def __init__(self, ctx, config):
        self.subreddits = config.reddit.subreddits
        self.latest = None
        self.channels = config.reddit.channels or ctx.channels

    @every(15, 'tail-reddit')
    def tail_reddit(self, ctx, name):
        responses = grequests.map([
            grequests.get('http://www.reddit.com/r/{subreddit}/new.json'.format(subreddit=subreddit))
            for subreddit in self.subreddits
        ])

        for res in responses:
            data = res.json()
            posts = []

            if self.latest is None:
                posts.append(data.children[0]['data'])
            else:
                is_new_enough = True

                while is_new_enough:
                    is_new_enough = int(child['data']['id']) > self.latest
                    if is_new_enough:
                        posts.append(child['data'])

                posts = posts.sort(sort_posts).reverse()

            if len(posts) > 0:
                self.latest = int(posts[0]['id'])

            posts.reverse()
            for channel in self.channels:
                for post in posts:
                    ctx.PRIVMSG(channel, '⬆ ⬇ {score} {title} submitted by {u} to {r} {url}'.format(
                        score=post.score,
                        title=post.title,
                        u=post.author,
                        r=post.subreddit
                    ))
