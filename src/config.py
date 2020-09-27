# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    config.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/27 11:05:38 by charles           #+#    #+#              #
#    Updated: 2020/09/27 11:51:41 by charles          ###   ########.fr        #
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
