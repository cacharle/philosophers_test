# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    philo.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/27 17:49:41 by charles           #+#    #+#              #
#    Updated: 2020/09/29 10:54:03 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import re
import time
import enum
import itertools

import test.error as error

def current_ms():
    return int(time.time() * 1000)

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
    def __init__(self, line, philo_num):
        match = re.match(
            r"^(?P<timestamp>\d+) "
            r"(?P<id>\d+) "
            r"(?P<event>is thinking|is eating|is sleeping|died)$",
            line
        )
        if match is None:
            raise error.Format(line, "wrong format")

        curr = current_ms()
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
                raise error.Format(s, "should be between {} - {}".format(lo, hi))
        except ValueError:
            raise error.Format(s, "sould be an integer".format(s))
        return value

    def __repr__(self):
        return "{}ms #{} {}".format(self.timestamp, self.id, self.event)


class Philo:
    def __init__(self, id_: int, timeout_eat: int, meal_num: int = 1):
        self._logs = []
        self.id = id_
        self.meal_num = meal_num
        self._timeout_eat = timeout_eat
        # self._start_time = current_ms()

    def add_log(self, log):
        self._logs.append(log)

    def check(self):
        if len(self._logs) == 0:
            return
        grouped = [(e, list(g)) for e, g in itertools.groupby(self._logs, (lambda x: x.event))]
        for e, g in grouped:
            if e is Event.EATING:
                if len(g) != self.meal_num:
                    raise error.Log(self._logs, "should eat {} times".format(self.meal_num))
            else:
                if len(g) != 1:
                    raise error.Log(self._logs, "should {} 1 time".format(Event.to_verb(e)))

        events = [e for e, _ in grouped]
        for e1, e2 in zip(events, events[1:]):
            if e2 is Event.DIED:
                break
            second = {
                Event.THINKING: Event.EATING,
                Event.EATING:   Event.SLEEPING,
                Event.SLEEPING: Event.THINKING
            }[e1]
            if e2 is not second:
                raise error.Log(self._logs, "invalid switch {} -> {}".format(e1, e2))

        last_eat = None
        for log in reversed(self._logs):
            if log.event is Event.EATING:
                last_eat = log
                break
        last = self._logs[-1]
        if last_eat is not None and last_eat is not last:
            if last.timestamp - last_eat.timestamp > self._timeout_eat + 20:
                raise error.Log(self._logs, "{} should be dead {}".format(self.id, last.timestamp))

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
                raise error.Log("timestamp not in ordered")
        for p in self._philos:
            p.check()
