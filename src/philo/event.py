# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    event.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/10/01 10:51:13 by cacharle          #+#    #+#              #
#    Updated: 2020/10/05 13:51:48 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import enum


class Event(enum.Enum):
    FORK  = 1
    EAT   = 2
    SLEEP = 3
    THINK = 4
    DIE   = 5
    NONE  = 6

    @staticmethod
    def from_string(representation: str) -> "Event":
        return {
            "has taken a fork": Event.FORK,
            "is thinking":    Event.THINK,
            "is eating":      Event.EAT,
            "is sleeping":    Event.SLEEP,
            "died":           Event.DIE,
        }[representation]

    @staticmethod
    def to_string(event: "Event") -> str:
        return {
            Event.FORK:  "has taken a fork",
            Event.THINK: "is thinking",
            Event.EAT:   "is eating",
            Event.SLEEP: "is sleeping",
            Event.DIE:   "died"
        }[event]
