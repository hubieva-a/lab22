#!/usr/bin/env python3
# -*- config: utf-8 -*-

from dataclasses import dataclass, field
from typing import List
from datetime import date
import sqlite3

class UnknownCommandError(Exception):

    def __init__(self, command, message="Unknown command"):
        self.command = command
        self.message = message
        super(UnknownCommandError, self).__init__(message)

    def __str__(self):
        return f"{self.command} -> {self.message}"


@dataclass(frozen=True)
class Person:
    name: str
    phone: str
    birthday: List[int]


@dataclass
class People:
    people: List[Person] = field(default_factory=lambda: [])

    db = sqlite3.connect('ind.sqlite')
    cur = db.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS peoples (
        _id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        day INTEGER,
        month INTEGER,
        year INTEGER
    )''')

    db.commit()

    def add(self, name: str, phone: str, birthday: List[int]) -> None:
        today = date.today()

        if birthday[2] < 0 or birthday[2] > today.year or birthday[0] < 0 or \
                birthday[0] > 31 or birthday[1] < 0 or birthday[1] > 12:
            raise IllegalDateError(birthday)

        self.people.append(
            Person(
                name=name,
                phone=phone,
                birthday=birthday
            )
        )

    def __str__(self) -> str:

        table = []
        line = '+-{}-+-{}-+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 8,
            '-' * 8,
            '-' * 8
            )
        table.append(line)
        table.append(
             '| {:^4} | {:^30} | {:^20} | {:^8} | {:^8} | {:^8} |'.format(
                    "№",
                    "Фамилия",
                    "Класс",
                    "Оценка 1",
                    "Оценка 2",
                    "Оценка 3"
                )
        )
        table.append(line)

        for idx, person in enumerate(self.people, 1):
            table.append(
                '| {:>4} | {:<30} | {:<20} | {:>8} | {:>8} | {:>8} |'.format(
                    idx,
                    person.name,
                    person.phone,
                    person.birthday[0],
                    person.birthday[1],
                    person.birthday[2]
                )
            )

        table.append(line)

        return '\n'.join(table)

    def select(self, value):
        result = []
        count = 0
        for person in self.people:
            if int(value) == int(person.birthday[1]):
                count += 1
                result.append(person)
        return result

    def load(self) -> None:
        self.people = []
        data = self.cur.execute("SELECT * FROM peoples")
        for i in data:
            name = i[1]
            class_number = i[2]
            grades = [i[3], i[4], i[5]]
            self.people.append(
                Person(
                    name=name,
                    phone=class_number,
                    birthday=grades
                )
            )

    def save(self) -> None:
        self.cur.execute('''DELETE FROM peoples''')
        for person in self.people:
            name = person.name
            phone = person.phone
            bdd = person.birthday[0]
            bdm = person.birthday[1]
            bdy = person.birthday[2]

            self.cur.execute('''INSERT INTO peoples (
            name, phone, day, month, year) VALUES (?, ?, ?, ?, ?)
            ''', (name, phone, bdd, bdm, bdy))
            self.db.commit()

    def kill(self) -> None:
        self.cur.execute('''DROP TABLE peoples''')
        self.db.commit()