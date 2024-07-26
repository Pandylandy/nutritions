from aiogram import Router
from aiogram.types import Message, input_file
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from custom_states import MyStates
from aiogram_dialog import DialogManager, ChatEvent
from aiogram_dialog.widgets.kbd import Checkbox, ManagedCheckbox
from aiogram_dialog.widgets.text import Const
from utils import create_sc


router = Router()


@router.message(Command('start'))
async def my_callback(message: Message):
    await message.answer('Для создания графика приема добавок нажмите /create')


@router.message(Command('create'))
async def my_callback(message: Message, state: FSMContext):
    await message.answer('Введите список добавок по шаблону: \n\n'
                         '[Название, сколько дней принимать, условия приема]\n\n'
                         'Например, прием магния в течение двух месяцев на завтрак и обед:\n'
                         'Магний 2 таблетки, 60, завтрак+обед\n'
                         'Хром 1 капсула, 10, за 30 минут до завтрака\n\n'
                         'и нажмите /done')

    await state.set_state(MyStates.wait_list)


@router.message(Command('done'))
async def my_callback(message: Message, state: FSMContext):
    data = await state.get_data()
    supplements = {}
    lines = data['text'].strip().split('\n')  # Разделение строки на отдельные строки
    for line in lines:
        name, days, meal_times = line.strip().split(', ')
        supplements[name] = [int(days), meal_times]
    print(supplements)
    await create_sc(supplements)

    await message.answer_document(input_file.BufferedInputFile.from_file('nutri_schedule.txt'))
    # await message.answer_document(input_file.BufferedInputFile.from_file('nutri_schedule.md'))
    await message.answer_document(input_file.BufferedInputFile.from_file('nutri_schedule.xlsx'))
    await message.answer('Done!')
    await state.clear()


@router.message(StateFilter(MyStates.wait_list))
async def by_id(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    print(message.text)


async def check_changed(event: ChatEvent, checkbox: ManagedCheckbox,
                        manager: DialogManager):
    print("Check status changed:", checkbox.is_checked())


check = Checkbox(
    Const("✓  Checked"),
    Const("Unchecked"),
    id="check",
    default=True,  # so it will be checked by default,
    on_state_changed=check_changed,
)
