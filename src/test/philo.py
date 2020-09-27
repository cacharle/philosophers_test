# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    philo.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/27 17:49:41 by charles           #+#    #+#              #
#    Updated: 2020/09/27 17:53:10 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import re
import time
import enum
import itertools


class Event(enum.Enum):
    EATING = 1
    SLEEPING = 2
    THINKING = 3
    DIED = 4
    NONE = 5


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
            "is thinking": Event.THINKING,
            "is eating":   Event.EATING,
            "is sleeping": Event.SLEEPING,
            "died":        Event.DIED,
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


class Philo:
    def __init__(self, id_: int, timeout_eat: int, meal_num: int = 1):
        self._logs = []
        self.id = id_
        self.meal_num = meal_num
        self._timeout_eat = timeout_eat

    def add_log(self, log):
        self._logs.append(log)

    def check(self):
        grouped = [(e, list(g)) for e, g in itertools.groupby(self._logs, (lambda x: x.event))]
        for e, g in grouped:
            if e is Event.EATING:
                if len(g) != self.meal_num:
                    raise RuntimeError("lala")
            else:
                if len(g) != 1:
                    raise RuntimeError("1lala")

        events = [e for e, _ in grouped]
        for e1, e2 in zip(events, events[1:]):
            if e2 is Event.DIED:
                break
            if e1 is Event.THINKING and e2 is not Event.EATING:
                raise RuntimeError("2lala")
            elif e1 is Event.EATING and e2 is not Event.SLEEPING:
                raise RuntimeError("2lala")
            elif e1 is Event.SLEEPING and e2 is not Event.EATING:
                raise RuntimeError("2lala")

        last_eat_time = int(time.time() * 1000)
        for l in reversed(self._logs):
            if l.event is Event.EATING:
                last_eat_time = l.timestamp
                break

        if int(time.time() * 1000) - last_eat_time > self._timeout_eat + 20:
            raise RuntimeError("should be dead")

    @property
    def last_event(self):
        if len(self._logs) == 0:
            return Event.NONE
        return self._logs[-1].event


class Table:
    def __init__(self, timeout_eat, philo_num):
        self._philos = [Philo(id_, timeout_eat) for id_ in range(1, philo_num + 1)]
        self._logs = []
        self._philo_num = philo_num
        self.dead = False

    def add_log(self, log):
        if self.dead:
            raise RuntimeError("died")
        if log.event is Event.DIED:
            self.dead = True
        self._logs.append(log)
        philo = next(p for p in self._philos if p.id == log.id)
        philo.add_log(log)

    def check(self):
        if self.dead:
            return
        fork_used = 2 * len([p for p in self._philos if p.last_event == Event.EATING])
        if fork_used > self._philo_num:
            raise RuntimeError("too much fork")
        for p in self._philos:
            p.check()
        for l1, l2 in zip(self._logs, self._logs[1:]):
            if l1.timestamp > l2.timestamp:
                raise RuntimeError("timestamp not ordered")
