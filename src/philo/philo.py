# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    philo.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/27 12:54:12 by charles           #+#    #+#              #
#    Updated: 2020/09/27 16:50:22 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import itertools
from philo.event import Event

class Philo:
    def __init__(self, id_: int, meal_num: int = 1):
        self._logs = []
        self.id = id_
        self.meal_num = meal_num

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

    @property
    def last_event(self):
        if len(self._logs) == 0:
            return Event.NONE
        return self._logs[-1].event
