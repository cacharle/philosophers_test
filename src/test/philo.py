# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    philo.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/27 12:54:12 by charles           #+#    #+#              #
#    Updated: 2020/09/27 12:59:50 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

class Philo:
    def __init__(id_: int):
        self.id = id_
        self.last_event = None
        self.last_eat_date = None

    def add_log(self, match):
        pass

    def check(self):
        return True
