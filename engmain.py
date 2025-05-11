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
        "Administrative Reforms of Peter the Great\n"
"1. Introduction of boards instead of orders (since 1717)\n"
"2. Establishment of the Senate (1711) — the highest governing body\n"
"3. Division of the country into governorates (1708), and then into provinces\n"
"\n"
"Military Reforms of Peter the Great\n"
"1. Creation of a regular army and navy\n"
"2. Introduction of conscription (1705)\n"
"3. Opening of military schools (Artillery School, Naval Academy)\n"
"\n"
"Economic Reforms of Peter the Great\n"
"1. Development of manufactories\n"
"2. Introduction of new taxes (e.g., poll tax instead of household tax)\n"
"3. Protectionist policy (import duties)\n"
"\n"
"Church Reforms of Peter the Great\n"
"1. Abolition of the patriarchate, establishment of the Holy Synod (1721)\n"
"2. Subordination of the church to the state\n"
"\n"
"Social and Cultural Reforms of Peter the Great\n"
"1. Compulsory education of nobles\n"
"2. Decree on shaving beards (1698)\n"
"3. Introduction of European clothing\n"
"4. Creation of a civil alphabet\n"
"\n"
"Educational Reforms of Peter the Great\n"
"1. Foundation of secular schools (School of Mathematical and Navigational Sciences)\n"
"2. Sending nobles abroad to study\n"
"3. First newspaper — Vedomosti\n"
    ),
    "conflicts": (
        "Uprisings during the reign of Peter I\n"
"\n"
"1. Streltsy Revolt of 1698\n"
"• Reasons: dissatisfaction of the Streltsy with the military reform and European innovations, hardships of service\n"
"• Result: the uprising was brutally suppressed, more than 1,000 Streltsy were executed, the Streltsy army was finally disbanded\n"
"\n"
"2. Astrakhan Uprising (1705-1706)\n"
"• Reasons: increased taxes, arbitrariness of the local administration, dissatisfaction with innovations\n"
"• Participants: Streltsy, Cossacks, urban poor\n"
"• Result: suppressed by Sheremetev's punitive corps, participants were cruelly punished\n"
"\n"
"3. Bashkir Uprisings (starting in 1704)\n"
"• Reasons: increased taxes, forced Christianization, oppression of the Bashkir nobility\n"
"• Features: were protracted, were supported by some Turkic peoples\n"
"• Result: brutal suppression, mass punitive expeditions, resettlements\n"
"\n"
"4. Bulavin Uprising (1707-1708)\n"
"• Leader: Kondraty Bulavin\n"
"• Reasons: dissatisfaction with the policy of recruitment and persecution of fugitive peasants\n"
"• Center: Don Cossacks\n"
"• Result: Bulavin is killed, the uprising is suppressed, but it became the largest manifestation of Cossack protest\n"
    ),
    "historians": (
"Historians who wrote about Peter I\n"
"\n"
"1. Nikolai Karamzin (1766-1826)\n"
"• Work: 'History of the Russian State'\n"
"• Attitude: was critical of Peter's reforms, believed that they destroyed the traditional way of life of Rus'\n"
"• Quote: 'Peter brought us greatness, but took away our soul.'\n"
"\n"
"2. Sergei Solovyov (1820-1879)\n"
"• Work: 'History of Russia from Ancient Times'\n"
"• Attitude: positive; saw Peter as a reformer who saved Russia from backwardness\n"
"\n"
"3. Vasily Klyuchevsky (1841-1911)\n"
"• Work: 'Course of Russian History'\n"
"• Attitude: balanced; emphasized both the advantages and the victims of Peter's reforms\n"
"• Quote: 'He accustomed Russia to state violence and a great goal.'\n"
    ),
    "sources": (
        "📖 *Recommended Reading*\n\n"
        "1. Anisimov E.V. «Peter I: Benefit or Misfortune for Russia»\n"
        "2. Kamenetsky A.B. «The Russian Empire in the 18th Century»\n"
        "3. Karamzin N.M. «History of the Russian State»\n"
        "4. Solovyov S.M. «History of Russia from Ancient Times – Sergei Solovyov»\n"
        "5. Robert K. Massie «Peter the Great: His Life and World»\n"
    ),
}

QUESTIONS = [
    {
        "question": "What tax did Peter I introduce instead of household taxation?",
        "options": ["Poll tax", "Window Tax", "Quit", "Corvee"],
        "correct": 0
    },
    {
        "question": "What governing body was created in 1711?",
        "options": [
            "State Duma",
            "Senate",
            "Collegiums",
            "Synod"
        ],
        "correct": 1
    },
    {
        "question": "Who led the uprising on the Don in 1707-1708?",
        "options": [
            "Stepan Razin",
            "Emelyan Pugachev",
            "Kondraty Bulavin",
            "Ivan Bolotnikov"
        ],
        "correct": 2
    },
    {
        "question": "When was the Holy Synod established?",
        "options": [
            "1700",
            "1711",
            "1721",
            "1725"
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
