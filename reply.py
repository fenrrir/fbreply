#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Copyright (C) 2013 Rodrigo Pinheiro Marques de Araujo
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.




import time
import datetime
import fbconsole as fb
from collections import namedtuple

Message = namedtuple('Message', 'id text author')



def get_date_from_post(post):
    year, month, day = map(int, post['created_time'].\
            split('T')[0].\
            split('-'))
    return day, month, year


class Bot(object):


    def __init__(self):
        self.setup()
        self.me_id = fb.get("/me")['id']

    def setup(self):
        fb.AUTH_SCOPE = ['publish_stream', \
                'publish_checkins', 'read_stream']
        fb.authenticate()

    def get_posts(self, days=3):

        day = datetime.datetime.now().day

        for post in fb.iter_pages(fb.get('/me/feed')):
            d, m, y = get_date_from_post(post)
            if day - d > days:
                break
            else:
                yield post

    def get_posts_by_other_people(self):
        for post in self.get_posts():
            if post['from']['id'] != self.me_id:
                yield post


    def get_posts_with_words(self, words):
        for post in self.get_posts_by_other_people():
            for word in words:
                if word.lower() in post[u'message'].lower():
                    yield Message(post['id'], post[u'message'], post['from']['name'])
                    break


    def show_messages_on_console(self):
        for message in self.get_posts_with_words([u"felicidades", u"parabéns"]):
            print message.id, message.text, message.author

    def reply_messages(self, msg):
        for message in self.get_posts_with_words([u"felicidades", u"parabéns"]):
            fb.post("/" + message.id + "/comments", {"message" : msg})
            time.sleep(1)
        

def test():
    b = Bot()
    b.reply_messages("Muito Obrigado!")


if __name__ == "__main__":
    test()
