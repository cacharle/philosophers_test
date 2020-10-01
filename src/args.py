# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    args.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/10/01 10:23:09 by cacharle          #+#    #+#              #
#    Updated: 2020/10/01 10:33:00 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #


import argparse

import config

def parse_args():
    parser = argparse.ArgumentParser(
        description="Philosophers test",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-p", "--philo",
        help="Id of the philosopher program to test \n"
             "- 1: philo_one\n"
             "- 2: philo_two\n"
             "- 3: philo_three\n"
             "- 0: all programs\n",
        required=True,
        type=int,
        choices=[0, 1, 2, 3]
    )
    parser.add_argument(
        "-b", "--build",
        help="Build and exit",
        action="store_true"
    )
    parser.add_argument(
        "-g", "--pager",
        help="Open {} in a pager after the test".format(config.RESULT_FILE),
        action="store_true"
    )
    parser.add_argument(
        "-t", "--timeout",
        help="Change the philosopher process time (in seconds)",
        type=float,
        default=config.TIMEOUT
    )
    return parser.parse_args()
