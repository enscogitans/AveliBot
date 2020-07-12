import asyncio
import logging
import typing as tp
from asyncio import gather
from datetime import datetime
from random import choice

import pytz
from aiogram import Dispatcher, types
from sqlalchemy import desc, func

from models import Chat, ChatMember, WolfWinner, db


async def _get_user_name(chat: types.Chat, user_id: int, is_mention: bool = False) -> str:
    chat_member = await chat.get_member(user_id)
    winner_user = chat_member.user
    name = winner_user.username or winner_user.first_name
    if not is_mention:
        return name
    return chat_member.user.get_mention(name, as_html=True)


async def _generate_game_messages(chat: types.Chat, winner_id: int) -> tp.List[str]:
    phrases_1 = [
        "Осторожно! <b>Волчара дня</b> активирован!",
        "Итак... кто же сегодня <b>волчара дня</b>?",
        "Что тут у нас?",
        "Инициирую поиск <b>волчары дня</b>...",
        "Сейчас поколдуем...",
        "Кто сегодня счастливчик?",
        "Зачем вы меня разбудили...",
        "Система взломана. Нанесён урон. Запущено планирование контрмер.",
        "Опять в эти ваши игрульки играете? Ну ладно...",
        "### RUNNING 'VOLCHARA.SH'...",
    ]
    phrases_2 = [
        "Где-же он...",
        "Интересно...",
        "Шаманим-шаманим...",
        "Хм...",
        "Военный спутник запущен, коды доступа внутри...",
        "Выезжаю на место...",
        "Машины выехали",
        "Сонно смотрит на бумаги",
        "Ведётся поиск в базе данных",
        "Сканирую...",
    ]
    phrases_3 = [
        "Так-так, что же тут у нас...",
        "В этом совершенно нет смысла...",
        "Ох...",
        "КЕК!",
        "Доступ получен. Аннулирование протокола.",
        "Я в опасности, системы повреждены!",
        "Что с нами стало...",
        "Ведётся захват подозреваемого...",
        "Не может быть!",
        "Проверяю данные...",
        "Ого-го...",
        "Высокий приоритет мобильному юниту.",
    ]
    phrases_4 = [
        "<b>Волчара дня</b> обыкновенный, 1шт. - {}",
        "Ого, вы посмотрите только! А <b>волчара дня</b>-то - {}",
        "Ну ты и <b>волчара</b>, {}",
        "Кто бы мог подумать, но <b>волчара дня</b> - {}",
        "И прекрасный человек дня сегодня... а нет, ошибка, всего лишь <b>волчара</b> - {}",
        "Анализ завершен. Ты <b>волчара</b>, {}",
        "Ага! Поздравляю! Сегодня ты <b>волчара</b>, {}",
        "Что? Где? Когда? А ты <b>волчара дня</b>, {}",
        "Стоять! Не двигаться! Вы объявлены <b>волчарой дня</b>, {}",
        "Кажется, <b>волчара дня</b> - {}",
    ]

    winner_name = await _get_user_name(chat, winner_id, is_mention=True)
    return [
        choice(phrases_1),
        choice(phrases_2),
        choice(phrases_3),
        choice(phrases_4).format(winner_name),
    ]


async def wolf(message: types.Message) -> None:
    chat = message.chat
    db_chat = db.query(Chat).get(chat.id)
    if db_chat is None:
        logging.error(f"Chat {chat.id} not found in database")
        return

    tz = pytz.timezone(db_chat.timezone)
    time = tz.fromutc(datetime.utcnow())
    date = time.date()

    winner = db.query(WolfWinner).get({"chat_id": chat.id, "date": date})
    if winner is not None:
        winner_name = await _get_user_name(message.chat, winner.user_id)
        await message.answer(
            "Согласно моей информации, по результатам сегодняшнего "
            f"розыгрыша <b>волчара дня</b> - {winner_name}!",
            parse_mode="HTML"
        )
        return

    known_members = [mem for mem in db_chat.members if not mem.has_left]
    if not known_members:
        logging.error(f"No users found in chat {chat.id}")
        return

    winner_id = choice(known_members).user_id
    db.add(WolfWinner(chat_id=chat.id, date=date, user_id=winner_id))
    db.commit()

    answers = await _generate_game_messages(message.chat, winner_id)
    for ans in answers[:-1]:
        await message.answer(ans, parse_mode="HTML")
        await asyncio.sleep(3)
    await message.answer(answers[-1], parse_mode="HTML")


async def wolf_stats(message: types.Message) -> None:
    current_members = db.query(ChatMember.user_id) \
        .filter((ChatMember.chat_id == message.chat.id) & ~ChatMember.has_left) \
        .subquery()
    query = db \
        .query(WolfWinner.user_id, func.count(WolfWinner.date).label("cnt")) \
        .filter(WolfWinner.chat_id == message.chat.id) \
        .join(current_members, WolfWinner.user_id == current_members.c.user_id) \
        .group_by(WolfWinner.user_id) \
        .order_by(desc("cnt")) \
        .all()
    if not query:
        await message.answer("В этом чате пока ещё нет <b>волчар</b>!", parse_mode="HTML")
        return

    user_ids, win_counts = zip(*query)
    tasks = [_get_user_name(message.chat, user_id) for user_id in user_ids]
    names = await gather(*tasks)

    answer_lines = [
        "Топ <b>волчар</b> за всё время:",
        "",
    ] + [
        f"{i + 1}. {name} — {cnt} раз(а)" for i, (name, cnt) in enumerate(zip(names, win_counts))
    ] + [
        "",
        f"Всего розыгрышей — {sum(win_counts)}"
    ]
    await message.answer("\n".join(answer_lines), parse_mode="HTML")


def register(dp: Dispatcher) -> None:
    dp.register_message_handler(wolf,
                                types.ChatType.is_group_or_super_group,
                                commands=["wolf"],
                                is_user=True)
    dp.register_message_handler(wolf_stats,
                                types.ChatType.is_group_or_super_group,
                                commands=["wolfstats"],
                                is_user=True)
