import json
import re

from aiogram import types
from aiogram.utils import executor
from requests import post, get, delete, put

from bot import dp
from config import HEADERS, API_URL


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    post('{API_URL}telegram-users/',
         json.dumps({'user_id': str(message.from_user.id)}),
         headers=HEADERS)
    await message.reply('Welcome! Use /help to see available commands.')


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    help_text = '''
    Available commands:
    /create "<title>" "<description>" "<due_date>" - Create a new task.
    /list - Display the list of all tasks.
    /view <task_id> - View a specific task by its ID.
    /update <task_id> <new_title> - Update the title of a task.
    /complete <task_id> - Mark a task as completed.
    /delete <task_id> - Delete a task.
    '''
    await message.reply(help_text)


@dp.message_handler(commands=['create'])
async def create_task(message: types.Message):
    try:
        args = message.get_args()

        regex = r'"([^"]+)"|(\S+)'
        matches = re.findall(regex, args)
        if len(matches) != 3:
            await message.reply("Invalid command format. Use: /create \"<title>\" \"<description>\" \"<due_date>\"")
            return

        title, description, due_date = [match[0] or match[1] for match in matches]
        user_id = message.from_user.id

        if not re.match(r'^\d{4}-\d{2}-\d{2}$', due_date):
            await message.reply("Invalid due date format. Use: YYYY-MM-DD")
            return

        url = f'{API_URL}tasks/?user_id={user_id}'
        data = {
            'user_id': user_id,
            'title': title,
            'description': description,
            'due_date': due_date
        }
        print(data)

        response = post(url, json=data)
        if response.status_code == 201:
            await message.reply('Task created successfully!')
        else:
            await message.reply('Error creating task.')
    except Exception as e:
        await message.reply('Error creating task.')


@dp.message_handler(commands=['list'])
async def list_tasks(message: types.Message):
    try:
        user_id = message.from_user.id

        response = get(f'{API_URL}tasks/?user_id={user_id}')
        if response.status_code == 200:
            tasks = response.json()
            if tasks:
                task_list = '\n'.join([f"{task['id']}. {task['title']}" for task in tasks])
                await message.reply(f'Task list:\n{task_list}')
            else:
                await message.reply('You have no tasks.')
        else:
            await message.reply('Error retrieving task list.')
    except Exception as e:
        await message.reply('Error retrieving task list.')


@dp.message_handler(commands=['view'])
async def view_task(message: types.Message):
    try:
        task_id = message.get_args()
        if not task_id.isdigit():
            await message.reply('Invalid command format. Use: /view <task_id>')
            return

        response = get(f'{API_URL}tasks/{task_id}/?user_id={message.from_user.id}')
        if response.status_code == 200:
            task = response.json()
            await message.reply(
                f"Task {task['id']}:\nTitle: {task['title']}\nDescription: {task['description']}\nDue Date: {task['due_date']}\nCompleted: {task['completed']}")
        elif response.status_code == 406:
            await message.reply(f'You have not access to task with id {task_id}')
        elif response.status_code == 404:
            await message.reply(f"Task with ID {task_id} not found.")
        else:
            await message.reply('Error retrieving task.')
    except Exception as e:
        await message.reply('Error retrieving task.')


@dp.message_handler(commands=['update'])
async def update_task(message: types.Message):
    try:
        args = message.get_args().strip()

        regex = r'"(.*?)"'
        matches = re.findall(regex, args)
        if len(matches) != 2:
            await message.reply('Invalid command format. Use: /update "<task_id>" "<new_title>"')
            return

        task_id, new_title = matches
        user_id = message.from_user.id

        response = get(f'{API_URL}tasks/{task_id}/?user_id={user_id}')
        if response.status_code == 200:
            task_data = response.json()
            data = {
                'user_id': user_id,
                'title': new_title,
                'description': task_data['description'],
                'due_date': task_data['due_date']
            }

            update_response = put(f'{API_URL}tasks/{task_id}/?user_id={user_id}', json=data)
            if update_response.status_code == 200:
                await message.reply('Task title updated successfully!')
            elif update_response.status_code == 406:
                await message.reply(f'You have not access to task with id {task_id}')
            else:
                await message.reply('Error updating task title.')
        elif response.status_code == 404:
            await message.reply(f"Task with ID {task_id} not found.")
        else:
            await message.reply('Error retrieving task data.')
    except Exception as e:
        await message.reply('Error updating task data.')


@dp.message_handler(commands=['complete'])
async def complete_task(message: types.Message):
    try:
        task_id = message.get_args()
        if not task_id.isdigit():
            await message.reply('Invalid command format. Use: /complete <task_id>')
            return

        user_id = message.from_user.id

        response = put(f'{API_URL}tasks/{task_id}/complete/?user_id={user_id}')
        if response.status_code == 200:
            await message.reply('Task marked as completed!')
        elif response.status_code == 404:
            await message.reply(f"Task with ID {task_id} not found.")
        elif response.status_code == 406:
            await message.reply(f'You have not access to task with id {task_id}')
        else:
            await message.reply('Error marking task as completed.')
    except Exception as e:
        await message.reply('Error marking task as completed.')


@dp.message_handler(commands=['delete'])
async def delete_task(message: types.Message):
    try:
        task_id = message.get_args()
        if not task_id.isdigit():
            await message.reply('Invalid command format. Use: /delete <task_id>')
            return

        user_id = message.from_user.id

        response = delete(f'{API_URL}tasks/{task_id}/?user_id={user_id}')
        if response.status_code == 204:
            await message.reply('Task deleted!')
        elif response.status_code == 404:
            await message.reply(f"Task with ID {task_id} not found.")
        elif response.status_code == 406:
            await message.reply(f'You have not access to task with id {task_id}')
        else:
            await message.reply('Error deleting task.')
    except Exception as e:
        await message.reply('Error deleting task.')


@dp.message_handler()
async def all_other_messages(message: types.Message):
    await message.reply("There is no such command, Use /help to see available commands. ")


if __name__ == '__main__':
    executor.start_polling(dp)
