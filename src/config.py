# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    config.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/27 11:05:38 by charles           #+#    #+#              #
#    Updated: 2020/10/01 10:15:26 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import os


# Location of your project directory
PROJECT_PATH = "../philosophers"

# Build your project before the test if set to True
BUILD_BEFORE = True

# Command to run before the test to build your project
# `{path}` is replaced by the philosophers directory (e.g `../philo_one` `../philo_two`)
BUILD_CMD = "make --no-print-directory -C {path}"

# Timeout for non infinite test
TIMEOUT = 1.0

# Timeout for error test
TIMEOUT_ERROR = 0.2

# Destination of the full summary of failed tests
RESULT_FILE = "result.log"

# Pager command
PAGER_CMD = ["less"]

################################################################################
# Do not edit
################################################################################

PHILO_PATHS = [
    os.path.join(PROJECT_PATH, "philo_one"),
    os.path.join(PROJECT_PATH, "philo_two"),
    os.path.join(PROJECT_PATH, "philo_three")
]

PHILO_EXEC_PATHS = [
    os.path.join(PHILO_PATHS[0], "philo_one"),
    os.path.join(PHILO_PATHS[1], "philo_two"),
    os.path.join(PHILO_PATHS[2], "philo_three")
]

INT_MIN   = -2147483648
INT_MAX   = 2147483647
UINT_MAX  = 4294967295
LONG_MIN  = -9223372036854775808
LONG_MAX  = 9223372036854775807
ULONG_MAX = 18446744073709551615
