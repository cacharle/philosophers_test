# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/27 11:36:32 by charles           #+#    #+#              #
#    Updated: 2020/09/28 16:08:51 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import os
import subprocess

import config
import test.philo as philo


class ShouldFailError(Exception):
    pass


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
        philo_num:     int   = None,
        timeout_die:   int   = None,
        timeout_eat:   int   = None,
        timeout_sleep: int   = None,
        meal_num:      int   = None,
        error_cmd:     [str] = None,
        infinite:      bool  = False
    ):
        self._philo_num     = philo_num
        self._timeout_die   = timeout_die
        self._timeout_eat   = timeout_eat
        self._timeout_sleep = timeout_sleep
        self._meal_num      = meal_num
        self._error_cmd     = error_cmd
        self._infinite      = infinite
        Test._tests.append(self)

    def run(self):
        try:
            self._run_tested()
        except ShouldFailError as e:
            self._print_fail("not failed: " + str(e))
        except philo.FormatError as e:
            self._print_fail("format: " + str(e))
        except philo.LogError as e:
            self._print_fail("log: " + str(e))
        # except Time
        else:
            self._print_pass()

    def _run_tested(self):
        process = subprocess.Popen(
            self._argv(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        if self._error_cmd is not None:
            self._check_error(process)
        elif self._infinite:
            self._check_output(process.stdout, died=False)
            time.sleep(config.INFINITE_WAIT_TIME)
            process.kill()
        else:
            self._check_output(process.stdout)
            process.wait(timeout=config.TIMEOUT)

    def _check_output(self, stream, died: bool = True):
        table = philo.Table(self._philo_num, self._timeout_eat)
        for line in stream:
            line = line.decode()[:-1]
            table.add_log(philo.Log(line, self._philo_num))
            table.check()
        if died and not table.dead:
            raise philo.LogError("one philosopher should have died")

    def _check_error(self, process):
        try:
            out, _ = process.communicate(timeout=config.TIMEOUT_ERROR)
        except subprocess.TimeoutExpired:
            raise ShouldFailError("no error message")
        if process.returncode == 0:
            raise ShouldFailError("non zero status code: {}".format(process.returncode))
        if out.decode().count('\n') != 1:
            raise ShouldFailError("no error message")

    RED_CHARS   = "\033[31m"
    GREEN_CHARS = "\033[32m"
    BOLD_CHARS  = "\033[1m"
    CLOSE_CHARS = "\033[0m"

    def _argv(self, basename=False):
        exec_path = os.path.basename(Test._exec_path) if basename else Test._exec_path
        if self._error_cmd is not None:
            return [exec_path, *self._error_cmd]
        else:
            argv = [
                exec_path,
                str(self._philo_num),
                str(self._timeout_die),
                str(self._timeout_eat),
                str(self._timeout_sleep)
            ]
            if self._meal_num is not None:
                argv.append(str(self._meal_num))
            return argv

    def _print_fail(self, msg):
        print("{}[FAIL] {}: {}{}".format(Test.RED_CHARS, self._argv_str, msg, Test.CLOSE_CHARS))

    def _print_pass(self):
        print("{}[PASS] {}{}".format(Test.GREEN_CHARS, self._argv_str, Test.CLOSE_CHARS))

    @property
    def _argv_str(self):
        return ' '.join(self._argv(basename=True))
