from __future__ import annotations
from proctors.write_proctor import WriteProctor
from enum import Enum
import data
import utils

class Command(Enum):
    EXIT = 0
    HELP  = 1
    SHOW = 2
    WRITE = 3

class Session:
    def __init__(self, name: str, generic_path: str, set_data: data.Set):
        self.name = name
        self.generic_path = generic_path
        self.set = set_data
        self.run = False
    
    def start(self):
        self.run = True
    
    def stop(self):
        self.run = False
    
    def action(self, command: Command):
        if command is Command.EXIT:
            self.stop()
        if command is Command.SHOW:
            print(self.set)
        if command is Command.WRITE:
            proctor = WriteProctor(self.name, self.generic_path, self.set)
            proctor.main()
        if command is Command.HELP:
            print("Commands:")
            print("\tExit (e): Exit out of the current session")
            print("\tShow (s): Show the contents of the current session")
            print("\tWrite (w): Begin write mode")

    def prompt(self) -> Command:
        command_str = utils.prompt(f"[StudyTool | {self.name}] $ ").strip().lower()
        if command_str in ["e", "exit"]:
            return Command.EXIT
        if command_str in ["s", "show"]:
            return Command.SHOW
        if command_str in ["w", "write"]:
            return Command.WRITE
        if command_str in ["h", "help"]:
            return Command.HELP

    def main(self) -> None:
        self.start()

        while self.run:
            self.action(self.prompt())