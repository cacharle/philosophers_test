# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    args.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/10/01 10:23:09 by cacharle          #+#    #+#              #
#    Updated: 2021/01/03 13:32:55 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #


import argparse
import textwrap

import config


def parse_args():
    parser = argparse.ArgumentParser(
        description="Philosophers test",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent("""\
            Tested:
             - Take 2 forks before eating
             - State switch in the correct order
               think -> fork -> fork -> eat n times -> sleep
             - Almost 0 delay between second fork taken and eat
             - Die if the death timeout is expired
             - No output after death
             - Timestamp in order
             - Only take existing fork
             - Error message and status != 0 on argument error
               (not asked by subject but easy to do and cleanner)
        """)
    )
    parser.add_argument(
        "-p", "--philo",
        help=textwrap.dedent("""\
            Number of the philosopher program to test
             - 1: philo_one
             - 2: philo_two
             - 3: philo_three
             - 0: all programs
        """),
        type=int,
        choices=[0, 1, 2, 3],
        default=0
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
