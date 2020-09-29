# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    philo.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/27 17:49:41 by charles           #+#    #+#              #
#    Updated: 2020/09/29 15:16:16 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import re
import enum
import itertools

import test.error as error
from helper import current_ms

class Event(enum.Enum):
    EATING = 1
    SLEEPING = 2
    THINKING = 3
    DIED = 4
    NONE = 5

    @staticmethod
    def to_verb(event):
        return {
            Event.EATING:   "eat",
            Event.SLEEPING: "sleep",
            Event.THINKING: "think",
            Event.DIED:     "die",
            Event.NONE:     "none",
        }[event]


class Log:
    def __init__(self, line, philo_num, start_time):
        match = re.match(
            r"^(?P<timestamp>\d+) "
            r"(?P<id>\d+) "
            r"(?P<event>is thinking|is eating|is sleeping|died)$",
            line
        )
        if match is None:
            raise error.Format(line, "wrong format")

        self._line = line
        self.id = self._parse_ranged_int(match.group("id"), 1, philo_num)
        self.timestamp = self._parse_ranged_int(
            match.group("timestamp"), start_time, current_ms())

        self.event = {
            "is thinking": Event.THINKING,
            "is eating":   Event.EATING,
            "is sleeping": Event.SLEEPING,
            "died":        Event.DIED,
        }[match.group('event')]

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


class Philo:
    def __init__(
        self,
        id_: int,
        timeout_die:   int,
        timeout_eat:   int,
        timeout_sleep: int,
        meal_num:      int
    ):
        self._logs = []
        self.id = id_
        self._timeout_die = timeout_die
        self._timeout_eat = timeout_eat
        self._timeout_sleep = timeout_sleep
        self._meal_num = meal_num

    def add_log(self, log):
        self._logs.append(log)

    def check(self):
        if len(self._logs) == 0:
            return
        grouped = [(e, list(g)) for e, g in itertools.groupby(self._logs, (lambda x: x.event))]
        for e, g in grouped:
            if e is Event.EATING:
                if len(g) != self._meal_num:
                    raise error.Log(self._logs, "should eat {} times".format(self._meal_num))
            else:
                if len(g) != 1:
                    raise error.Log(self._logs, "should {} 1 time".format(Event.to_verb(e)))

        # events = [e for e, _ in grouped]
        for l1, l2 in zip(self._logs, self._logs[1:]):
            if l2.event is Event.DIED:
                break
            if l1.event is Event.EATING and l2.event is Event.EATING:
                if l2.timestamp - l1.timestamp > self._timeout_eat:
                    raise ValueError
            second, timeout = {
                Event.THINKING: (Event.EATING, None),
                Event.EATING:   (Event.SLEEPING, self._timeout_eat),
                Event.SLEEPING: (Event.THINKING, self._timeout_sleep)
            }[l1.event]
            if l2.event is not second:
                raise error.Log(self._logs, "invalid switch {} -> {}".format(l1.event, l2.event))
            if timeout is not None and l2.timestamp - l1.timestamp > timeout:
                raise ValueError

        last_eat = None
        for log in reversed(self._logs):
            if log.event is Event.EATING:
                last_eat = log
                break
        last = self._logs[-1]
        if last_eat is not None and last_eat is not last:
            if last.timestamp - last_eat.timestamp > self._timeout_die + 10:
                raise error.Log(self._logs, "{} should be dead {} - {} > {}".format(
                    self.id, last.timestamp, last_eat.timestamp, self._timeout_die + 10))


    @property
    def last_event(self):
        if len(self._logs) == 0:
            return Event.NONE
        return self._logs[-1].event


class Table:
    def __init__(
        self,
        philo_num:     int,
        timeout_die:   int,
        timeout_eat:   int,
        timeout_sleep: int,
        meal_num:      int
    ):
        self._philos = [Philo(id_, timeout_die, timeout_eat, timeout_sleep, meal_num)
                        for id_ in range(1, philo_num + 1)]
        self._logs = []
        self._philo_num = philo_num
        self.dead = False

    def add_log(self, log):
        self._logs.append(log)
        philo = next(p for p in self._philos if p.id == log.id)
        philo.add_log(log)
        if self.dead:
            raise error.Log(self._logs, "should not output after death")
        if log.event is Event.DIED:
            self.dead = True

    def check(self):
        if self.dead:
            return
        fork_used = 2 * len([p for p in self._philos if p.last_event == Event.EATING])
        if fork_used > self._philo_num:
            raise error.Log(self._logs, "using nonexistant forks")
        for l1, l2 in zip(self._logs, self._logs[1:]):
            if l1.timestamp > l2.timestamp:
                raise error.Log(self._logs, "timestamp not in ordered")
        for p in self._philos:
            p.check()
