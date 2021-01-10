# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    test.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/09/27 11:36:32 by charles           #+#    #+#              #
#    Updated: 2021/01/03 13:53:38 by cacharle         ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import os
import subprocess

import config
import philo
from helper import current_ms, red, green


class Test:
    _tests = []
    _exec_path = None
    _fail_summaries = []

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
    ):
        self._philo_num     = philo_num
        self._timeout_die   = timeout_die
        self._timeout_eat   = timeout_eat
        self._timeout_sleep = timeout_sleep
        self._meal_num      = meal_num
        self._error_cmd     = error_cmd
        Test._tests.append(self)

    def run(self):
        try:
            self._run_tested()
        except philo.error.Philo as e:
            self._print_fail(e.summary)
            Test._fail_summaries.append(self._argv_str + '\n' + e.full_summary)
        else:
            self._print_pass()

    @classmethod
    def write_failed(cls):
        with open(config.RESULT_FILE, "w") as f:
            f.write('\n\n'.join(cls._fail_summaries))

    @classmethod
    def print_summary(cls):
        fail_total = len(cls._fail_summaries)
        pass_total = len(cls._tests) - fail_total
        print("Summary: Total {}   {}   {}".format(
            len(cls._tests),
            green("[PASS] {:3}".format(pass_total)),
            red("[FAIL] {:3}".format(fail_total))
        ))

    def _run_tested(self):
        start_time = current_ms()
        process = subprocess.Popen(
            self._argv(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0

        )
        if self._error_cmd is not None:
            self._check_error(process)
            return

        try:
            out, err = process.communicate(timeout=config.TIMEOUT)
        except subprocess.TimeoutExpired:
            process.kill()
            out, err = process.communicate()
        end_time = current_ms()
        out = out.decode()
        err = err.decode()

        table = philo.Table(
            self._philo_num,
            self._timeout_die,
            self._timeout_eat,
            self._timeout_sleep,
            1 if self._meal_num is None else self._meal_num
        )
        for line in out.split('\n')[:-1]:
            table.add_log(philo.Log(line, self._philo_num, start_time, end_time))
            table.check()

    def _check_error(self, process):
        try:
            _, err = process.communicate(timeout=config.TIMEOUT_ERROR)
        except subprocess.TimeoutExpired:
            raise philo.error.ShouldFail("no error message")
        if process.returncode == 0:
            raise philo.error.ShouldFail("non zero status code: {}".format(process.returncode))
        if err.decode().count('\n') != 1:
            raise philo.error.ShouldFail("no error message on stderr")

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

    @property
    def _argv_str(self):
        return ' '.join(self._argv(basename=True))

    def _print_fail(self, msg):
        print(red("[FAIL] {}: {}".format(self._argv_str, msg)))

    def _print_pass(self):
        print(green("[PASS] {}".format(self._argv_str)))
