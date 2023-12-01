import dbmanager as db
import parse_csv as pcsv

from config import bot, router

from aiogram import types, F
from aiogram.types import FSInputFile

@router.callback_query(lambda callback_query: callback_query.data.startswith("send_to_channel:"))
async def send_to_channel_callback(callback_query: types.CallbackQuery):
    channel_index = int(callback_query.data.split(":")[1])
    
    channel = db.get_channels()[channel_index]
    channel_chat_id = channel[1]
    
    try:
        for product in products:
            media = []
            for photo_url in product['img_urls']:
                photo_path = str(photo_url)
                media.append(types.InputMediaPhoto(media=FSInputFile(photo_path)))
            
            media[-1].parse_mode = 'HTML'
            media[-1].caption = f'<b>❤️‍🔥размер:</b> {product["sizes"]}\n<b>❤️‍🔥цена:</b> {product["price"]}\n<b>❤️‍🔥❤️‍🔥❤️‍🔥</b>{product["details"]}'
            
            await bot.send_media_group(chat_id=channel_chat_id, media=media)
        
        await bot.answer_callback_query(callback_query.id, text=f"Документы отправлены в канал {channel[0]}")
    except Exception as e:
        await bot.answer_callback_query(callback_query.id, text=f"Ошибка при отправке документов в канал {channel[0]}: {e}")
        
@router.callback_query(lambda callback_query: callback_query.data == "send_all_channels")
async def send_all_channels_callback(callback_query: types.CallbackQuery):
    channels = db.get_channels()
    
    for channel in channels:
        channel_chat_id = channel[1]
        
        try:
            for product in products:
                media = []
                for photo_url in product['img_urls']:
                    photo_path = str(photo_url)
                    media.append(types.InputMediaPhoto(media=types.FSInputFile(photo_path)))
                
                media[-1].parse_mode = 'HTML'
                media[-1].caption = f'<b>❤️‍🔥размер:</b> {product["sizes"]}\n<b>❤️‍🔥цена:</b> {product["price"]}\n<b>❤️‍🔥❤️‍🔥❤️‍🔥</b>{product["details"]}'
                
                await bot.send_media_group(chat_id=channel_chat_id, media=media)
        except Exception as e:
            print(f"Ошибка при отправке документа в канал {channel[0]}: {e}")

    await bot.answer_callback_query(callback_query.id, text="Документ отправлен во все каналы и группы")   

@router.message(F.document)
async def handle_admin_files(message: types.Message):
    if message.document:
        global document
        document = message.document

        # Получение списка всех групп, в которых состоит бот из базы данных
        groups = db.get_channels()
        
        global products
        products = await pcsv.parse_csv("result.csv")

        keyboard_buttons = []
        for i, channel in enumerate(groups):
            button = types.InlineKeyboardButton(text=f"{i+1}. {channel[0]}", callback_data=f"send_to_channel:{i}")
            keyboard_buttons.append([button])

        keyboard_buttons.append([types.InlineKeyboardButton(text="Отправить во все группы/каналы", callback_data="send_all_channels")])

        keyboard = types.InlineKeyboardMarkup(inline_keyboard=keyboard_buttons, row_width=1)

        await message.reply("При нажатии на канал - в него будет отправлен документ", reply_markup=keyboard)
    else:
        await message.reply("Пожалуйста, прикрепите документ.")
        

# Обработчик Inline кнопок
@router.callback_query(lambda c: c.data.startswith('delete_channel'))
async def delete_channel_callback(callback_query: types.CallbackQuery):
    _, index = callback_query.data.split(':')
    channels = db.get_channels()

    if not channels:
        await callback_query.answer("Список каналов пуст.", show_alert=True)
        return

    try:
        index = int(index)
        channel = channels[index]
    except (ValueError, IndexError):
        await callback_query.answer("Неверный номер канала.", show_alert=True)
        return

    db.del_channel(channel[0])

    await bot.send_message(callback_query.from_user.id, f"Канал {channel[0]} удален.")


# Обработчик Inline кнопки "Вывести все группы/каналы"
@router.callback_query(lambda c: c.data == 'show_all_channels')
async def show_all_channels_callback(callback_query: types.CallbackQuery):
    channels = db.get_channels()

    if not channels:
        await callback_query.answer("Список каналов пуст.", show_alert=True)
        return

    text = "Список групп/каналов:\n\n"
    for i, channel in enumerate(channels):
        text += f"{i+1}. {channel[0]}\n"

    await bot.send_message(callback_query.from_user.id, text)