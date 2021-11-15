from fileinput import FileInput
from json import dump, load


class File:
    def __init__(self, path, backup=False):
        self.path = path
        if backup:
            self.backup = '.bkp'
        else:
            self.backup = ''

    def replace(self, find, replace):
        with FileInput(self.path, inplace=True, backup=self.backup) as file:
            for line in file:
                print(line.replace(find, replace), end='')

    def save(self, data):
        if ".json" in str(self.path):
            with open(self.path, "w") as file:
                dump(data, file, indent=4)
        if ".diskpw" in str(self.path):
            with open(self.path, "wb") as file:
                file.write(data)

    def load(self):
        if ".json" in str(self.path):
            with open(self.path) as file:
                return load(file)
        else:
            with open(self.path) as file:
                return file.readlines()
