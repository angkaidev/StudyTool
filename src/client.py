from __future__ import annotations
from typing import NamedTuple
from enum import Enum
import os
import set_parser
import session
import utils

# TODO: Collections
class Command(Enum):
    EXIT = 0
    HELP = 1
    UPDATE = 2
    OPEN = 3

class SetInfo(NamedTuple):
    name: str
    directory_path: str
    filename: str

class Client:
    def __init__(self):
        self.sets: list[SetInfo] = []
        self.sessions: dict[str, session.Session] = {}
        self.run = False

        self.parser = set_parser.Parser()
    
    def start(self) -> None:
        self.run = True
    
    def stop(self) -> None:
        self.run = False

    def get_name(self, filepath: str) -> str:
        with open(filepath, "r") as file:
            line = file.readline()

        name = line.split(":")[0].strip()
        return name

    def update_sets(self) -> None:
        """
        Updates the sets dictionary
        """
        self.sets: list[SetInfo] = []

        data_dir = f"{os.path.dirname(os.path.realpath(__file__))[:-3]}data/"
        try:
            for category in os.listdir(data_dir):
                directory_path = f"{data_dir}{category}/"
                for file in os.listdir(directory_path):
                    parts = file.split(".")
                    name = self.get_name(f"{directory_path}{file}")
                    extension = parts[1]
                    if extension == "set":
                        self.sets.append(SetInfo(name, directory_path, parts[0]))
        except NotADirectoryError:
            pass
    
    def print_sets(self) -> None:
        count = 0
        for set_info in self.sets:
            print(f"\t{count}: {set_info.name}")
            count += 1
    
    # TODO: Add collections
    def open(self) -> None:
        self.update_sets()
        print("Available Sets:")
        self.print_sets()
        
        index = utils.prompt("[StudyTool | Open] $ ").strip()
        if index.isnumeric():
            index = int(index)
            if index >= 0 and index < len(self.sets):
                set_info = self.sets[index]
                if set_info.name not in self.sessions:
                    generic_path = f"{set_info.directory_path}{set_info.filename}"
                    set_data = self.parser.parse_set(f"{generic_path}.set")
                    self.sessions[set_info.name] = session.Session(set_info.name, generic_path, set_data)
                self.sessions[set_info.name].main()
        else:
            print("Invalid Input")
    
    def action(self, command: Command) -> None:
        if command is Command.EXIT:
            self.stop()
        if command is Command.UPDATE:
            self.update_sets()
            print("Available Sets:")
            self.print_sets()
        if command is Command.OPEN:
            self.open()
        if command is Command.HELP:
            print("Commands:")
            print("\tExit (e): Quit out of StudyTool")
            print("\tUpdate (u): Update the list of sets/collections")
            print("\tOpen (o): Open a session for a given set/collection")
    
    def prompt(self) -> Command:
        command_str = utils.prompt("[StudyTool] $ ").strip().lower()
        if command_str in ["e", "exit"]:
            return Command.EXIT
        if command_str in ["u", "update"]:
            return Command.UPDATE
        if command_str in ["o", "open"]:
            return Command.OPEN
        if command_str in ["h", "help"]:
            return Command.HELP

    def main(self) -> None:
        self.start()

        while(self.run):
            self.action(self.prompt())

if __name__ == "__main__":
    os.system("stty erase '^H'")
    client = Client()
    client.main()