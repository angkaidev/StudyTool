import data
import utils
import copy
import random

class WriteProctor:
    def __init__(self, name: str, generic_path: str, set_data: data.Set):
        self.name = name
        self.generic_path = generic_path
        self.set = set_data

        self.entry_pool: list[data.Entry] = []

        self.run = False
    
    def start(self):
        self.run = True
        self.entry_pool = copy.deepcopy(self.set.entries)

    def stop(self):
        self.run = False
    
    def get_entry(self) -> data.Entry:
        if len(self.entry_pool) == 0:
            self.entry_pool = copy.deepcopy(self.set.entries)
        
        index = int(random.random() * len(self.entry_pool))
        entry = self.entry_pool[index]
        self.entry_pool.pop(index)

        return entry

    def main(self):
        self.start()

        while self.run:
            entry = self.get_entry()

            answered = False
            while not answered:
                answer = utils.prompt(f"Definition: {entry.definition}\nTerm: ")
                if answer in ["e", "exit"]:
                    self.stop()
                if answer in ["h", "help"]:
                    print("Input the corresponding term for the given definition")
                    print("\tExit (e): Exit out of write mode")
                    print("\tOverride (o): Upon getting an answer wrong, this will override that judgement")
                else:
                    answered = True

            if answer == entry.term:
                print(utils.correct("Correct!"))
            else:
                correct_msg = "Correct Answer: "
                user_msg = "Your Answer:    "

                for index in range(max(len(answer), len(entry.term))):
                    color_function = utils.incorrect
                    if index < len(answer) and index < len(entry.term) and answer[index] == entry.term[index]:
                        color_function = utils.correct
                    if index < len(entry.term):
                        correct_msg = f"{correct_msg}{color_function(entry.term[index])}"
                    if index < len(answer):
                        user_msg = f"{user_msg}{color_function(answer[index])}"
                
                print(correct_msg)
                print(user_msg)