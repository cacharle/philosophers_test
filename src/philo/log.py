# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    log.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/27 16:04:18 by charles           #+#    #+#              #
#    Updated: 2020/09/27 16:05:21 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import re
import time

import philo


class Log:
    def __init__(self, log, philo_num):
        match = re.match(
            "^(?P<timestamp>\d+) "
            "(?P<id>\d+) "
            "(?P<event>is thinking|is eating|is sleeping|died)$",
            log
        )
        if match is None:
            raise ValueError("Bad line format |{}|".format(log))

        curr = int(time.time() * 1000)
        self.timestamp = Log._parse_ranged_int(match.group("timestamp"), curr - 100, curr + 100)
        self.id = Log._parse_ranged_int(match.group("id"), 1, philo_num)

        self.event = {
            "is thinking": philo.Event.THINKING,
            "is eating":   philo.Event.EATING,
            "is sleeping": philo.Event.SLEEPING,
            "died":        philo.Event.DIED,
        }[match.group('event')]

    @staticmethod
    def _parse_ranged_int(s, lo, hi):
        try:
            value = int(s)
            if not (lo <= value <= hi):
                raise ValueError("Invalid value range {}".format(s))
        except ValueError:
            raise ValueError("Invalid value {}".format(s))
        return value


    def __repr__(self):
        return "{} {} {}".format(self.timestamp, self.id, self.event)
