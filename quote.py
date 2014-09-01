"""
quote.py - A simple quotes module for willie
Copyright (C) 2014  Andy Chung - iamchung.com
Copyright (C) 2014  Luis Uribe - acme@eviled.org

iamchung.com

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

from __future__ import unicode_literals
import willie
from willie import module

import random
import codecs # TODO in python3, codecs.open isn't needed since the default open does encoding.
import re

@willie.module.commands('quote')
def quote(bot, trigger):
	filename = bot.config.quote.filename
	raw_args = trigger.group(2)
	output = ''
	if raw_args is None or raw_args == '':
		# display random quote
		output = get_random_quote(bot, trigger.sender)
	else:
		# get subcommand
		command_parts = raw_args.split(' ', 1)
		if len(command_parts) < 2:
			output = 'invalid number of arguments'
		else:
			subcommand = command_parts[0]
			data = command_parts[1]

			# perform subcommand
			if subcommand == 'add':
				output = add_quote(bot, trigger.sender, data)
			# elif subcommand == 'delete':
			# 	output = delete_quote(filename, data)
			# elif subcommand == 'show':
			# 	output = show_quote(filename, data)
			# elif subcommand == 'search':
			# 	output = search_quote(filename, data)
			else:
				output = 'invalid subcommand'
	bot.say(output)

def get_random_quote(bot, channel):
    try:
        msg = random.choice(bot.memory['chan_quotes'][channel])
    except:
        msg = 'We have no data'
        return msg

    return msg

def add_quote(bot, channel, search):
    try:
        bot.memory['chan_messages'][channel]
    except:
        msg = "There's no history for this channel."
        return msg

    for line in bot.memory['chan_messages'][channel]:
        if re.search(search, line) is not None:
            try:
                bot.memory['chan_quotes'][channel]
            except:
                bot.memory['chan_quotes'][channel] = []
            bot.memory['chan_quotes'][channel].append(line)
            msg = "Quote addedd"
            return msg

    msg = "What are you doing, moron?"
    return msg

def setup(bot):
    bot.memory['chan_messages'] = {}
    bot.memory['chan_quotes'] = {}

#save everything it's said on the channels
@module.rule('^.*')
def log_chan_message(bot, trigger):
    try:
        bot.memory['chan_messages'][trigger.sender].append(trigger.nick + ': ' +trigger)
    except:
        bot.memory['chan_messages'][trigger.sender] = []
        bot.memory['chan_messages'][trigger.sender].append(trigger.nick + ': ' +trigger)