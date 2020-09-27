#!/bin/python3

# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    run                                                :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/27 11:36:34 by charles           #+#    #+#              #
#    Updated: 2020/09/27 11:36:34 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

# invalid state switch
# none existant fork
# timestamp not in order
# crash
# should be infinity
# print lines after died
# bad output format
# should be dead

import os
import sys
import subprocess
import argparse

import config
from test import Test


def main():
    parser = argparse.ArgumentParser(description="Philosophers test")
    parser.add_argument("-p", "--philo", help="Id of the philosophers to test ",
                        required=True, type=int, choices=[1, 2, 3])
    parser.add_argument("-b", "--build", help="Build and exit")
    args = parser.parse_args()

    if config.BUILD_BEFORE or args.build:
        try:
            print("=====================================BUILD======================================")
            subprocess.run(config.BUILD_CMD.format(path=config.PHILO_PATHS[0]).split(' '), check=True)
            print("================================================================================")
        except subprocess.CalledProcessError:
            sys.exit(1)
        if args.build:
            sys.exit(0)

    if args.philo != 1:
        sys.exit(1)

    Test(10, 100, 100, 10)
    Test.run_all(config.PHILO_EXEC_PATHS[0])
    # print("yo")

if __name__ == "__main__":
    main()
