# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/27 11:36:32 by charles           #+#    #+#              #
#    Updated: 2020/09/27 13:28:15 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import re
import subprocess
# import threading

# from result import Result


class Test: #(threading.Thread):
    _tests = []
    _exec_path = None
    # _stdout_lock = threading.Lock()

    @classmethod
    def run_all(cls, exec_path: str):
        cls._exec_path = exec_path
        for t in cls._tests:
            t.run()
        # threads = [test.start() for test in cls._tests]
        # for thread in threads:
        #     thread.join()

    def __init__(
        self,
        philo_num:     int,
        timeout_die:   int,
        timeout_eat:   int,
        timeout_sleep: int,
        meal_num:      int = None,
        should_fail:   bool = False
    ):
        self._philo_num     = philo_num
        self._timeout_die   = timeout_die
        self._timeout_eat   = timeout_eat
        self._timeout_sleep = timeout_sleep
        self._meal_num      = meal_num
        Test._tests.append(self)
        # threading.Thread.__init__(self)

    def run(self):
        argv = [
            Test._exec_path,
            str(self._philo_num),
            str(self._timeout_die),
            str(self._timeout_eat),
            str(self._timeout_sleep)
        ]
        if self._meal_num is not None:
            argv.append(str(self._meal_num))
        # try:
        process_result = subprocess.run(
            argv,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        output = process_result.stdout.decode()
        print(output)
                # timeout=1,
        # except subprocess.TimeoutExpered as err:
        #     return Result(err)
        # except subprocess.CalledProcessError as err:
        #     return Result(err)

        self._check_output(output)
        # return Result()

    def _check_output(self, stream):
        # table = Table(self._philo_num)

        for line in stream.split('\n'):
            match = re.match(
                "^(?P<timestamp>\d+) "
                "(?P<id>\d+) "
                "(?P<event>is thinking|is eating|is sleeping|died)$",
                line
            )
            if match is None:
                print("Bad line format |{}|".format(line))
                return

            print(match.group('event'))
            try:
                timestamp = int(match.group("timestamp"))
                # if timestamp < 0
            except ValueError:
                print("Invalid timestamp value {}".format(match.group("timestamp")))

            table.add_log(match)

            # philo_states.append(Philo)

    # def _print(self, *args):
    #     Test._stdout_lock.aquire()
    #     print(*args)
    #     Test._stdout_lock.release()

# from enum import Enum
# class PhiloEvent(Enum):
#     EATING = 1
#     SLEEPING = 2
#     THINKING = 3
