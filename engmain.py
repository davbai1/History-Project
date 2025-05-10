from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
import logging

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7729059470:AAHOp3bJ5nyLg7Z-4EyptjFHOmdJDeZ-Fpc"

CONTENT = {
    "start": (
        "👋 *Welcome to the «Era of Peter the Great» bot! We offer to get to know it better with us!*\n\n"
        "▫️ Use /menu for the main menu\n"
        "▫️ /help for assistance"
    ),
    "menu": "📜 *Main Menu*",
    "reforms": (
        "⚡️ *Military Reforms of Peter the Great*\n\n"
        "1. Introduction of conscription (1705)\n"
        "2. Creation of a regular army\n"
        "3. Establishment of the Navy"
    ),
    "conflicts": (
        "🔥 *Popular Uprisings*\n\n"
        "1. Astrakhan Rebellion (1705–1706)\n"
        "2. Bulavin Rebellion (1707–1708)\n"
        "3. Bashkir Rebellion (1704–1711)"
    ),
    "historians": (
        "📚 *Historians' Opinions*\n\n"
        "• Klyuchevsky: 'Reforms were carried out by force'\n"
        "• Anisimov: 'The cost of reforms was too high'"
    ),
    "sources": (
        "📖 *Recommended Reading*\n\n"
        "1. Anisimov E.V. «Peter I: Benefit or Misfortune for Russia»\n"
        "2. Kamenetsky A.B. «The Russian Empire in the 18th Century»"
    ),
}

QUESTIONS = [
    {
        "question": "Which tax did Peter I introduce instead of household taxation?",
        "options": ["Poll Tax", "Window Tax", "Obrok"],
        "correct": 0
    },
    {
        "question": "What was the main goal of the 'Grand Embassy' in 1697–1698?",
        "options": [
            "Finding allies against Sweden",
            "Studying European technologies",
            "Both options are correct"
        ],
        "correct": 2
    }
]

# Global constants
TEST_PREFIX = "test_"
BACK_BUTTON = "🔙 Back"


def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📌 Reforms", callback_data="reforms")],
        [
            InlineKeyboardButton("⚔️ Uprisings", callback_data="conflicts"),
            InlineKeyboardButton("🎓 Historians", callback_data="historians"),
        ],
        [
            InlineKeyboardButton("📝 Quiz", callback_data="test"),
            InlineKeyboardButton("📚 Sources", callback_data="sources"),
        ],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(CONTENT["start"], parse_mode="Markdown")


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        CONTENT["menu"],
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "🔍 *Available Commands:*\n"
        "/start - initial message\n"
        "/menu - main menu\n"
        "/help - this help"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "menu":
        await show_menu(update)
    elif data == "test":
        await start_test(update, context)
    elif data in CONTENT:
        await show_content(update, data)


async def show_menu(update: Update) -> None:
    query = update.callback_query
    await query.edit_message_text(
        CONTENT["menu"],
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown"
    )


async def show_content(update: Update, content_key: str) -> None:
    query = update.callback_query
    await query.edit_message_text(
        CONTENT[content_key],
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(BACK_BUTTON, callback_data="menu")]
        ])
    )


async def start_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.clear()
    context.user_data.update({
        "correct": 0,
        "current_question": 0,
        "test_message_id": None,
        "test_active": True
    })
    await send_question(update, context)


async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.user_data.get("test_active"):
        return

    question_num = context.user_data["current_question"]
    try:
        question = QUESTIONS[question_num]
    except IndexError:
        await finish_test(update, context)
        return

    keyboard = [
        [InlineKeyboardButton(opt, callback_data=f"{TEST_PREFIX}{question_num}_{i}")]
        for i, opt in enumerate(question["options"])
    ]

    text = (
        f"❓ *Question {question_num + 1}/{len(QUESTIONS)}*\n"
        f"{question['question']}"
    )

    if context.user_data["test_message_id"]:
        await edit_message(update, context, text, keyboard)
    else:
        msg = await update.callback_query.message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )
        context.user_data["test_message_id"] = msg.message_id


async def handle_test_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if not context.user_data.get("test_active"):
        return

    data = query.data[len(TEST_PREFIX):].split("_")
    question_num = int(data[0])
    answer_idx = int(data[1])

    if question_num != context.user_data["current_question"]:
        return

    if answer_idx == QUESTIONS[question_num]["correct"]:
        context.user_data["correct"] += 1

    context.user_data["current_question"] += 1
    await send_question(update, context)


async def edit_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, keyboard: list) -> None:
    await context.bot.edit_message_text(
        chat_id=update.callback_query.message.chat_id,
        message_id=context.user_data["test_message_id"],
        text=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


async def finish_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    correct = context.user_data["correct"]
    total = len(QUESTIONS)
    text = (
        f"📊 *Quiz Results*\n"
        f"Correct answers: {correct} out of {total}\n\n"
        f"{'🎉 Perfect score!' if correct == total else '💪 Keep practicing!'}"
    )

    await edit_message(
        update,
        context,
        text,
        [[InlineKeyboardButton(BACK_BUTTON, callback_data="menu")]]
    )
    context.user_data.clear()


def main() -> None:
    app = Application.builder().token(TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(
        CallbackQueryHandler(handle_main_menu, pattern="^(menu|test|reforms|conflicts|historians|sources)$"))
    app.add_handler(CallbackQueryHandler(handle_test_answer, pattern=f"^{TEST_PREFIX}"))

    app.run_polling()


if __name__ == "__main__":
    main()
