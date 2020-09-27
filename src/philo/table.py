# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    table.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/27 12:44:48 by charles           #+#    #+#              #
#    Updated: 2020/09/27 16:54:52 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

from philo.philo import Philo
from philo.event import Event


class Table:
    def __init__(self, philo_num):
        self._philos = [Philo(id_) for id_ in range(1, philo_num + 1)]
        self._logs = []
        self._philo_num = philo_num

    def add_log(self, log):
        self._logs.append(log)
        philo = next(p for p in self._philos if p.id == log.id)
        philo.add_log(log)

    def check(self):
        died_count = len([p for p in self._philos if p.last_event == Event.DIED])
        if died_count > 1:
            raise RuntimeError("died")
        fork_used = 2 * len([p for p in self._philos if p.last_event == Event.EATING])
        if fork_used > self._philo_num:
            raise RuntimeError("too much fork")
        for p in self._philos:
            p.check()
        for l1, l2 in zip(self._logs, self._logs[1:]):
            if l1.timestamp > l2.timestamp:
                raise RuntimeError("timestamp not ordered")

