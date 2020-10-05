# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    helper.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/29 11:19:32 by cacharle          #+#    #+#              #
#    Updated: 2020/10/05 13:49:25 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import time


def current_ms():
    return int(time.time() * 1000)


RED_CHARS   = "\033[31m"
GREEN_CHARS = "\033[32m"
BLUE_CHARS  = "\033[34m"
CLOSE_CHARS = "\033[0m"


def red(string):
    return RED_CHARS + string + CLOSE_CHARS


def green(string):
    return GREEN_CHARS + string + CLOSE_CHARS


def blue(string):
    return BLUE_CHARS + string + CLOSE_CHARS
