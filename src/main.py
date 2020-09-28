#!/usr/bin/env python3

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

# [x] invalid state switch
# [x] none existant fork
# [x] timestamp not in order
# [ ] crash
# [ ] should be infinity
# [ ] argument error
# [x] print lines after died
# [x] bad output format
# [x] should be dead

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

    Test.new_error([])
    Test.new_error(["a", "a", "a", "a"])
    Test.new_error(["aaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "a", "a", "a"])
    Test.new_error(["10"])
    Test.new_error(["10", "10"])
    Test.new_error(["10", "10", "10"])
    Test.new_error(["10", "10", "10", "10", "10", "10"])
    Test.new_error(["-1", "10", "10", "10"])
    Test.new_error(["10", "-1", "10", "10"])
    Test.new_error(["10", "10", "-1", "10"])
    Test.new_error(["10", "10", "10", "-1"])
    Test.new_error(["10", "10", "10", "10", "-1"])

    Test.new_error([str(config.UINT_MAX + 1), "10", "10", "10"])
    Test.new_error(["10", str(config.UINT_MAX + 1), "10", "10"])
    Test.new_error(["10", "10", str(config.UINT_MAX + 1), "10"])
    Test.new_error(["10", "10", "10", str(config.UINT_MAX + 1)])
    Test.new_error(["10", "10", "10", "10", str(config.UINT_MAX + 1)])

    Test.new_error([str(-config.UINT_MAX), "10", "10", "10"])
    Test.new_error(["10", str(-config.UINT_MAX), "10", "10"])
    Test.new_error(["10", "10", str(-config.UINT_MAX), "10"])
    Test.new_error(["10", "10", "10", str(-config.UINT_MAX)])
    Test.new_error(["10", "10", "10", "10", str(-config.UINT_MAX)])

    Test.new_error(["0", "100", "100", "100"])
    Test.new_error(["1", "100", "100", "100"])

    Test(10, 100, 100, 10)
    Test(10, 200, 10, 10, infinite=True)

    Test.run_all(config.PHILO_EXEC_PATHS[0])
    # print("yo")


if __name__ == "__main__":
    main()



