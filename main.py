import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from config import password_sql, my_token
from database import list, select_tasks, create_tasks_table
from database import create_connection, execute_query, execute_read_query
from pywebio.input import input, TEXT
from pywebio.output import put_button, put_table


logging.basicConfig(level=logging.INFO)


def data():
    put_button("Add task", onclick=add_data, color="success", outline=True)
    put_button("Delete task", onclick=delete_data, color='warning', outline=True)
    put_table([elem for elem in list])


def copy_data(table):
    list.append(['id', 'Description'])
    for line in table:
        task = [line[0], line[1]]
        list.append(task)


def delete_data():
    delete_id = input("Input an id task that you want delete: ", type=TEXT)
    delete_task = f"DELETE FROM tasks WHERE id = '{delete_id}'"
    execute_query(connection, delete_task)


def add_data():
    task_description = input("Input a description of a new task: ", type=TEXT)
    index = input("Input id: ", type=TEXT)
    add_task_table = f"""
       INSERT INTO
         `tasks` (`id`, `Description`)
       VALUES
         ('{index}', '{task_description}');
       """
    execute_query(connection, add_task_table)


def run_process():
    execute_query(connection, create_tasks_table)
    tasks = execute_read_query(connection, select_tasks)
    copy_data(tasks)
    data()


bot = Bot(token=my_token, parse_mode="HTML")
dispatcher = Dispatcher(bot)


@dispatcher.message_handler(commands='start')
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text='To-Do Planner')
    keyboard.add(button)
    await message.answer('Do you want to plan something?', reply_markup=keyboard)


@dispatcher.message_handler(lambda message: message.text == 'To-Do Planner')
async def todo(message: types.Message):
    run_process()


async def start():
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    connection = create_connection('localhost', 'root', password_sql, 'my_tasks')
    asyncio.run(start())
