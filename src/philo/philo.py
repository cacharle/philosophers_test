# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    philo.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/10/01 10:52:56 by cacharle          #+#    #+#              #
#    Updated: 2021/01/10 15:35:14 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import itertools

from philo import error
from philo.event import Event


class Philo:
    def __init__(
        self,
        id_:           int,
        timeout_die:   int,
        timeout_eat:   int,
        timeout_sleep: int,
        meal_num:      int
    ):
        self.logs           = []
        self.id             = id_
        self._timeout_die   = timeout_die
        self._timeout_eat   = timeout_eat
        self._timeout_sleep = timeout_sleep
        self._meal_num      = meal_num

    def check(self):
        """ Check log for errors

            - Must take 2 forks before eating
            - The delay between the taking of the second fork and eating should be almost 0
            - State switch should be
              thinking -> take fork -> take fork -> eat * meal_num -> sleep -> repeat
            - Should die when starving: last log timestamp - timeout_death > last_time_eat
            - Should eat n times, Should take fork 2 times, The other event should happend 1 time
        """

        if len(self.logs) == 0:
            return

        # check 2 forks before eating
        for l1, l2, l3 in zip(self.logs, self.logs[1:], self.logs[2:]):
            if (l3.event is Event.EAT
                and (l1.event is not Event.FORK
                     or l2.event is not Event.FORK)):
                self._raise("should take 2 forks then eat")

        # check log event number
        grouped = [(e, list(g)) for e, g in itertools.groupby(self.logs, (lambda x: x.event))]
        for e, g in grouped[:-1]:
            if e is Event.FORK:
                if len(g) != 2:
                    self._raise("Should take fork 2 times")
            elif len(g) != 1:
                self._raise("Event `{}` should occur 1 time".format(Event.to_string(e)))

        # check state switch order
        events = [e for e, _ in grouped]
        for e1, e2 in zip(events, events[1:]):
            second = {
                Event.THINK: Event.FORK,
                Event.FORK:  Event.EAT,
                Event.EAT:   Event.SLEEP,
                Event.SLEEP: Event.THINK
            }[e1]
            if e2 is not second:
                self._raise("invalid state switch `{}` -> `{}`".format(
                    Event.to_string(e1), Event.to_string(e2)))

        # check timeouts
        for l1, l2 in zip(self.logs, self.logs[1:]):
            e1, e2 = l1.event, l2.event
            t1, t2 = l1.timestamp, l2.timestamp
            if e1 is Event.FORK and e2 is Event.EAT:
                if t2 - t1 > 10:
                    self._raise("Delay between taking second fork and eat > 10")
            if e1 is Event.SLEEP:
                self._check_time_range(t1, t2, self._timeout_sleep, "Slept")
            if e1 is Event.EAT:
                self._check_time_range(t1, t2, self._timeout_eat, "Ate")

        # check if should be dead
        last_eat = next(
            (log for log in reversed(self.logs) if log.event is Event.EAT),
            None
        )
        last = self.logs[-1]
        if last_eat is not None and last_eat is not last:
            if last.timestamp - last_eat.timestamp > self._timeout_die + 10:
                self._raise(
                    "{} should be dead {} - {} > {}"
                    .format(self.id, last.timestamp,
                            last_eat.timestamp, self._timeout_die + 10)
                )

    def _check_time_range(self, t1, t2, timeout, verb):
        start = timeout - 10
        end = timeout + 10
        if not (start <= t2 - t1 <= end):
            self._raise("{} {}ms expected {}-{}ms".format(verb, t2 - t1, start, end))

    def _raise(self, msg):
        """ Helper to raise Log errrors"""
        raise error.Log(self.logs, msg)

    @property
    def used_forks(self):
        """ The number of forks currently used by the philosopher """
        if len(self.logs) < 1:
            return 0
        if self.logs[-1].event is Event.EAT:
            return 2
        if self.logs[-1].event is Event.FORK:
            if len(self.logs) > 1 and self.logs[-2].event is Event.FORK:
                return 2
            else:
                return 1
        return 0

    @property
    def meal_num_finished(self):
        return len([log for log in self.logs if log.event is Event.EAT]) >= self._meal_num
