# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    log.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/10/01 10:51:39 by cacharle          #+#    #+#              #
#    Updated: 2020/10/01 11:30:53 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import re

from .event import Event
from . import error

class Log:
    def __init__(self, line: str, philo_num, start_time, end_time):
        match = re.match(
            r"^(?P<timestamp>\d+) "
            r"(?P<id>\d+) "
            r"(?P<event>is thinking|is eating|is sleeping|died|has taken fork)$",
            line
        )
        if match is None:
            raise error.Format(line, "wrong format")

        self._line = line
        self.id = self._parse_ranged_int(match.group("id"), 1, philo_num)
        self.timestamp = self._parse_ranged_int(
            match.group("timestamp"), start_time, end_time)

        self.event = Event.from_string(match.group('event'))

    def _parse_ranged_int(self, s, lo, hi):
        try:
            value = int(s)
            if not (lo <= value <= hi):
                raise error.Format(self._line,
                        "{} should be between {} - {}".format(s, lo, hi))
        except ValueError:
            raise error.Format(self._line, "{} sould be an integer".format(s))
        return value

    def __repr__(self):
        return "{}ms #{} {}".format(self.timestamp, self.id, self.event)
