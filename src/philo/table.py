# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    table.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/10/01 10:53:29 by cacharle          #+#    #+#              #
#    Updated: 2020/12/30 14:26:37 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

from philo import Philo
from philo import error
from philo.event import Event


class Table:
    def __init__(
        self,
        philo_num:     int,
        timeout_die:   int,
        timeout_eat:   int,
        timeout_sleep: int,
        meal_num:      int
    ):
        self._philos    = [Philo(id_, timeout_die, timeout_eat, timeout_sleep, meal_num)
                           for id_ in range(1, philo_num + 1)]
        self._logs      = []
        self._philo_num = philo_num
        self.finished       = False
        self._meal_num  = meal_num

    def add_log(self, log):
        """ Add a log to the correct philosopher
            Set the finished flag if it's a death log
        """
        self._logs.append(log)
        philo = next(p for p in self._philos if p.id == log.id)
        philo.logs.append(log)
        # move
        if self.finished:
            raise error.Log(self._logs, "Output after death")
        if log.event is Event.DIE or all(p.meal_num_finished for p in self._philos):
            self.finished = True

    def check(self):
        """ Check global logs and all philosophers logs for errors

            - Should not output after one philosopher died
            - Should not take non existant forks
            - Timestamps should be in increasing order
        """

        if self.finished:
            return
        for p in self._philos:
            p.check()
        fork_used = sum([p.used_forks for p in self._philos])
        if fork_used > self._philo_num:
            raise error.Log(self._logs, "Using nonexistant forks")
        for l1, l2 in zip(self._logs, self._logs[1:]):
            if l1.timestamp > l2.timestamp:
                raise error.Log(self._logs, "Timestamps not in ordered")
