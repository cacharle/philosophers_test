# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/27 11:36:32 by charles           #+#    #+#              #
#    Updated: 2020/09/28 12:23:40 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import subprocess

import config
import test.philo as philo


class Test:
    _tests = []
    _exec_path = None

    @classmethod
    def run_all(cls, exec_path: str):
        cls._exec_path = exec_path
        for t in cls._tests:
            t.run()

    @staticmethod
    def new_error(error_cmd: [str]):
        Test(error_cmd=error_cmd)

    def __init__(
        self,
        philo_num:     int = None,
        timeout_die:   int = None,
        timeout_eat:   int = None,
        timeout_sleep: int = None,
        meal_num:      int = None,
        should_fail:   bool = False,
        error_cmd:     [str] = None
    ):
        self._philo_num     = philo_num
        self._timeout_die   = timeout_die
        self._timeout_eat   = timeout_eat
        self._timeout_sleep = timeout_sleep
        self._meal_num      = meal_num
        self._error_cmd     = error_cmd
        Test._tests.append(self)

    def run(self):
        if self._error_cmd is not None:
            argv = [Test._exec_path, *self._error_cmd]
        else:
            argv = [
                Test._exec_path,
                str(self._philo_num),
                str(self._timeout_die),
                str(self._timeout_eat),
                str(self._timeout_sleep)
            ]
            if self._meal_num is not None:
                argv.append(str(self._meal_num))
        process = subprocess.Popen(
            argv,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        if self._error_cmd is not None:
            self._check_error(process)
        else:
            self._check_output(process.stdout)
        process.wait(timeout=config.TIMEOUT)

    def _check_output(self, stream):
        table = philo.Table(self._philo_num, self._timeout_eat)
        for line in stream:
            line = line.decode()[:-1]
            table.add_log(philo.Log(line, self._philo_num))
            table.check()

    def _check_error(self, process):
        line_num = len([None for _ in process.stdout])
        if line_num != 1:
            raise ValueError("you should have an error message")
        if process.returncode == 0:
            raise ValueError("you should have a non zero status code")

