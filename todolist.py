# Write your code here
import sys
from sqlalchemy import create_engine

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

def menu():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")


#Prints all tasks for today
def today_tasks():
    today = datetime.today()
    rows = session.query(Table).filter(Table.deadline == today.date()).all()

    print('Today ' + str(today.day) + ' ' + today.strftime('%b') + ':')

    if not rows:
        print('Nothing to do!')
    else:
        i = 1
        for row in rows:
            print(str(i) + '. ' + row.task)
            i += 1


#Prints all tasks from last 7 days
def week_tasks():
    today = datetime.today()
    for j in range(7):
        rows = session.query(Table).filter(Table.deadline == today.date()).all()

        print(today.strftime("%A") + ' ' + str(today.day) + ' ' + today.strftime('%b') + ':')

        if not rows:
            print('Nothing to do!')
        else:
            i = 1
            for row in rows:
                print(str(i) + '. ' + row.task)
                i += 1
        today = today + timedelta(days=1)
        print()


#Prints all tasks sorted by deadline
def all_tasks():
    rows = session.query(Table).order_by(Table.deadline).all()
    i = 1
    for row in rows:
        if row.task != '0':
            print(str(i) + '. ' + row.task + '. ' + str(row.deadline.day) + ' ' + row.deadline.strftime('%b'))
            i += 1
        else:
            session.delete(row)
    session.commit()
    print()
    return i


#Prints all tasks whose deadline was missed (tasks whose deadline date is earlier that today's date)
def missed_tasks():
    rows = session.query(Table).filter(Table.deadline < datetime.today().date()).order_by(Table.deadline).all()
    i = 1
    if not rows:
        print('Nothing is missed')
    else:
        i = 1
        for row in rows:
            if row.task != '0':
                print(str(i) + '. ' + row.task + '. ' + str(row.deadline.day) + ' ' + row.deadline.strftime('%b'))
                i += 1
        print()


#Asks for task description and saves it in the database
def add_task():
    print('Enter task: ')
    my_task = input()
    print('Enter deadline: ')
    my_deadline = input()
    new_task = Table(task = my_task, deadline = datetime.strptime(my_deadline, '%Y-%m-%d').date())
    session.add(new_task)
    session.commit()
    print('The task has been added!')


#Deletes the chosen task
def delete_task():
    if (all_tasks() == 1):
        print('Nothing to delete')
    else:
        print('Choose the number of task you want to delete')
        rows = session.query(Table).order_by(Table.deadline).all()
        choice = input()
        specific_row = rows[int(choice)-1]
        session.delete(specific_row)


    session.commit()
    print('The task has been deleted')

def error():
    print('Invalid argument!')

while(True):
    menu()
    choice = input()
    if choice == '1':
        today_tasks()
    elif choice == '2':
        week_tasks()
    elif choice == '3':
        all_tasks()
    elif choice == '4':
        missed_tasks()
    elif choice == '5':
        add_task()
    elif choice == '6':
        delete_task()
    elif choice == '0':
        print('Bye!')
        break
    else:
        error()
