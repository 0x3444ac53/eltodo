#!/bin/python3
import yaml
import datetime
import pprint
from terminaltables import AsciiTable as tabler
import argparse

pp = pprint.PrettyPrinter(indent=4)

class Todo:
    def __init__(self, file='/home/ellie/.config/eltodo/list.yaml'):
        self.file = file
        try:
            with open(file) as f:
                self.todo = yaml.safe_load(f.read())
        except FileNotFoundError:
            self.todo = []

    def add(self, name: str, catagory : str, note=" ", urgency=0):
        self.todo.append({'name': name, 'added': datetime.datetime.now(),
                          'catagory' : catagory.lower(), 'note': note, 'urgency' : urgency,
                          'done' : None})
        self.todo.sort(key=lambda x: x['added'])
        self.todo.sort(key=lambda x: x['urgency'], reverse=True)
        self.save()

    def remove(self, index):
        self.todo.pop(index)
        self.save()

    def done(self, index):
        self.todo[index]['done'] = datetime.datetime.now()
        self.save()

    def dump(self):
        pp.pprint(self.todo)

    def __str__(self):
        reset = '\033[0m' # Normal
        italics = lambda x: f'\033[3m{x}{reset}'
        strike = lambda x: f'\033[9m{x}'
        urgency_colour_map = [
            '\033[3m',   # Normal
            '\033[33m',  # Yellow
            '\033[31m',  # red
            '\033[31;1;4m' # red and blinking
        ]
        table_data = [list(map(italics, ['#', 'Task', 'Note',
                                         'Catagory', 'Done']))]

        for i in range(len(self.todo)):
            urgency_colour = urgency_colour_map[self.todo[i]['urgency']]
            table_data.append(
                list(
                    map(italics,
                    [ i,
                    f"{urgency_colour}{self.todo[i]['name']}",
                    f"{urgency_colour}{self.todo[i]['note']}",
                    f"{urgency_colour}{self.todo[i]['catagory']}",
                    "{}".format(self.todo[i]["done"].strftime('%d/%m %H:%m') if
                                 self.todo[i]['done'] else '')
                    ]
                    )
                )
            )
        return tabler(table_data, title='TODO').table

    def __len__(self):
        return len(self.todo)

    def save(self):
        with open(self.file, 'w') as f:
            f.write(yaml.dump(self.todo))

def main():
    mainList = Todo()
    p = pargs(len(mainList))
    if "index" in vars(p):
        mainList.remove(p.index)
    elif "task" in vars(p):
        mainList.add(p.task, p.catagory, note=p.note, urgency=p.urgency)
    elif "doneindex" in vars(p):
        mainList.done(p.doneindex)
    print(mainList)

def pargs(removalindexs):
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='add or remove task')
    add_todo_parser = subparsers.add_parser("new", help="add new task")
    add_todo_parser.add_argument("task", help='task name')
    add_todo_parser.add_argument("-n", "--note", help='task note',
                                 default="")
    add_todo_parser.add_argument("-u", "--urgency", type=int,
                                 choices=[0, 1, 2, 3], default=0)
    add_todo_parser.add_argument("-c", "--catagory", type=str,
                                 default="General")
    removal_parser = subparsers.add_parser("remove", help="remove task")
    removal_parser.add_argument("index", type=int, choices =
                                range(removalindexs), help="index to remove")
    done_parser = subparsers.add_parser("done", help="Set Task to Done")
    done_parser.add_argument("doneindex", type = int,
                             choices=range(removalindexs))
    return parser.parse_args()

if __name__ == '__main__':
    main()
