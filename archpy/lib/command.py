import shlex
import subprocess
import sys
from time import sleep

from archpy import Message


class Cmd:
    def __init__(
        self,
        cmd,
        *pipes,
        cwd=None,
        msg=None,
        debug=False,
        shell=False,
        call=False,
        quiet=False,
    ):

        if type(cmd) is not list and not shell:
            try:
                self.cmd = shlex.split(cmd)
            except Exception as e:
                raise ValueError(f"Incorrect string to split: {cmd}\n{e}")
        else:
            self.cmd = cmd
        self.quiet = quiet
        self.pipes = pipes
        self.cwd = cwd
        self.message = msg
        self.debug = debug
        self.stdout = None
        self.stderr = None
        self.return_code = None
        self.shell = shell
        self.call = call
        self.run()

    def main_command(self):

        main_command = subprocess.Popen(
            self.cmd,
            cwd=self.cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=self.shell,
        )
        return main_command

    def pipe_command(self, previous, pipe):
        pipe_command = subprocess.Popen(
            pipe,
            stdin=previous.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=self.shell,
        )
        return pipe_command

    def progress(self, command):
        while command.poll() is None and not self.debug and self.message is not None:
            sys.stdout.write(
                "[" + Message.YELLOW + ". " + Message.RESET + "]" + f" {self.message}\r"
            )
            sleep(0.3)
            sys.stdout.flush()
            sys.stdout.write(
                "[" + Message.YELLOW + " ." + Message.RESET + "]" + f" {self.message}\r"
            )
            sleep(0.3)
            sys.stdout.flush()
        if self.debug:
            for line in command.stdout:
                print(line.decode("UTF-8").strip(), flush=True)

    def run(self):
        if self.call:
            subprocess.call(self.cmd)
        else:
            if self.pipes:
                main_command = self.main_command()
                pipe_command = None
                previous = main_command
                for index, pipe in enumerate(self.pipes):
                    if type(pipe) is not list:
                        try:
                            pipe = shlex.split(pipe)
                        except Exception as e:
                            raise ValueError(f"Incorrect string to split: {pipe}\n{e}")
                    if index == len(self.pipes):
                        pipe_command = self.pipe_command(previous, pipe)
                    else:
                        pipe_command = self.pipe_command(previous, pipe)
                    previous = pipe_command
                result = pipe_command
            else:
                main_command = self.main_command()
                result = main_command
            self.progress(result)
            self.stdout, self.stderr = result.communicate()
            self.stdout = self.stdout.decode("UTF-8").strip()
            self.stderr = self.stdout
            self.return_code = int(result.returncode)
            if self.return_code == 0:
                if self.message is not None:
                    sys.stdout.write(
                        "["
                        + Message.GREEN
                        + "OK"
                        + Message.RESET
                        + "]"
                        + f" {self.message}\n"
                    )
                if self.debug:
                    print(
                        f"{Message.BLUE}{self.cmd} {Message.GREEN}succeed{Message.RESET}"
                    )
                    print(self.stdout)
            else:
                if self.message is not None:
                    sys.stdout.write(
                        "["
                        + Message.RED
                        + "--"
                        + Message.RESET
                        + "]"
                        + f" {self.message}\n"
                    )
                if self.debug:
                    print(
                        f"{Message.BLUE}{self.cmd} {Message.RED}fail{Message.RESET}"
                    )
                if not self.quiet:
                    Message("red_alert").print(self.stdout)
