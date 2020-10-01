# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    philo.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/10/01 10:52:56 by cacharle          #+#    #+#              #
#    Updated: 2020/10/01 11:19:23 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import itertools

from . import error
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
        self.logs          = []
        self.id             = id_
        self._timeout_die   = timeout_die
        self._timeout_eat   = timeout_eat
        self._timeout_sleep = timeout_sleep
        self._meal_num      = meal_num

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

    def check(self):
        """ Check log for errors

            - Must take 2 forks before eating
            - The delay between the taking of the second fork and eating should be almost 0
            - State switch should be
              thinking -> take fork -> take fork -> eat * meal_num -> sleep -> repeat
            - Should die when starving: last log timestamp - timeout_death > last_time_eat
        """

        if len(self.logs) == 0:
            return

    # def _check_fork_taking(self):
    #     for l1, l2, l3 in zip(self.logs, self.logs[1:], self.logs[2:]):
    #         if l1.event is Event.FORK and (l2.event is not Event.FORK or l2.event is not Event.EAT):
    #             self._raise("should take 2 forks then eat")
    #
    # def _check_meal(self):
    #     grouped = [(e, list(g)) for e, g in itertools.groupby(self.logs, (lambda x: x.event))]
    #     for e, g in grouped:
    #         if e is Event.EATING:
    #             if len(g) != self._meal_num:
    #                 raise error.Log(self.logs, "should eat {} times".format(self._meal_num))
    #         else:
    #             if len(g) != 1:
    #                 raise error.Log(self.logs, "event {} should occur 1 time".format(Event.to_string(e)))
    #
    # def _check_order(self):
    #     for l1, l2 in zip(self.logs, self.logs[1:]):
    #         if l2.event is Event.DIED:
    #             break
    #         if l1.event is Event.EATING and l2.event is Event.EATING:
    #             if l2.timestamp - l1.timestamp > self._timeout_eat:
    #                 raise ValueError
    #         second, timeout = {
    #             Event.THINKING: (Event.EATING, None),
    #             Event.EATING:   (Event.SLEEPING, self._timeout_eat),
    #             Event.SLEEPING: (Event.THINKING, self._timeout_sleep)
    #         }[l1.event]
    #         if l2.event is not second:
    #             raise error.Log(self.logs, "invalid switch {} -> {}".format(l1.event, l2.event))
    #         if timeout is not None and l2.timestamp - l1.timestamp > timeout:
    #             raise ValueError
    #
    # def _check_death_timeout(self):
    #     last_eat = None
    #     for log in reversed(self.logs):
    #         if log.event is Event.EATING:
    #             last_eat = log
    #             break
    #     last = self.logs[-1]
    #     if last_eat is not None and last_eat is not last:
    #         if last.timestamp - last_eat.timestamp > self._timeout_die + 10:
    #             raise error.Log(self.logs, "{} should be dead {} - {} > {}".format(
    #                 self.id, last.timestamp, last_eat.timestamp, self._timeout_die + 10))

    def _raise(self, msg):
        """ Helper to raise Log errrors"""
        raise error.Log(self.logs, msg)

