# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    table.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/27 12:44:48 by charles           #+#    #+#              #
#    Updated: 2020/09/27 12:54:01 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

class Table:
    def __init__(self, philo_num):
        self._philos = [Philo(id_) for id_ in range(1, philo_num + 1)]

    def update(self, match):
        philo = itertools.first_true(self._philos, pred = lambda x: x.id == match.id)
        philo.add_log(match)

    def check(self):
        return True

