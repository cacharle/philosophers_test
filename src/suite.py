# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    suite.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cacharle <me@cacharle.xyz>                 +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/10/01 10:41:43 by cacharle          #+#    #+#              #
#    Updated: 2021/01/10 15:34:52 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import config
from test import Test


def suite():
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

    Test(0, 120, 60, 60)
    Test(1, 120, 60, 60)
    Test(2, 120, 60, 60)
    Test(3, 120, 60, 60)
    Test(4, 120, 60, 60)
    Test(5, 120, 60, 60)
    Test(6, 120, 60, 60)
    Test(7, 120, 60, 60)
    Test(5, 800, 200, 200)
    Test(5, 800, 200, 200, 7)
    Test(4, 410, 200, 200)
    Test(4, 310, 200, 100)

    # Test(100, 100, 50, 50)
    #
    # Test(10, 100, 100, 10)
    #
    # Test(2, 50, 10, 10)
    # Test(10, 50, 10, 10)
    # Test(10, 100, 10, 10)
    # Test(10, 200, 10, 10)
