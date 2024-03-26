import telebot
from telebot import types
import markovify
import random
from hugchat import hugchat
from hugchat.login import Login


class HuggingChat:  # достаем модель через хаггинг чат
    def __init__(
            self,
            email: str,
            password: str,
            system_prompt: str = "",
            cookie_path_dir: str = "./cookies_snapshot",
            model: str = "mistralai/Mixtral-8x7B-Instruct-v0.1",  # выбираем Миктраль
    ):
        self.sign = Login(email, password)
        cookies = self.sign.login()
        self.sign.saveCookiesToDir(cookie_path_dir)
        self.chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
        self.models = {
            "mistralai/Mixtral-8x7B-Instruct-v0.1": 0,
        }
        self.system_prompt = system_prompt
        self.model = self.models[model]
        self.chatbot = hugchat.ChatBot(cookies=cookies.get_dict(), system_prompt=self.system_prompt)
        self.chatbot.switch_llm(self.model)
        self.chatbot.new_conversation(switch_to=True, system_prompt=self.system_prompt)

    def prompt(self, prompt: str) -> str:
        return str(self.chatbot.query(prompt))

    def delete_conversations(self) -> None:
        """
        Deletes all conversations in a user's profile
        """
        self.chatbot.delete_all_conversations()
        self.chatbot.new_conversation(switch_to=True, system_prompt=self.system_prompt)

    def switch_model(self, model: str) -> None:
        self.model = self.models[model]
        self.chatbot.switch_llm(self.model)
        self.chatbot.new_conversation(switch_to=True, system_prompt=self.system_prompt)

    def switch_system_prompt(self, system_prompt: str) -> None:
        self.system_prompt = system_prompt
        self.chatbot.new_conversation(switch_to=True, system_prompt=self.system_prompt)


mistral_hugginchat = HuggingChat("stasik1219", "Psestutetri188", model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                                 system_prompt="Ты знаток русской литературы. Я дам тебе предложение, а тебе нужно будет угадать из какого оно произведения: из Обломова или из Преступления и наказания. В ответ запиши только название произведения.")
# записываем промпт для модели

with open('pin.txt') as f:  # смотрим текст Преступления и наказания
    text_pin = f.read()

# Создание модели марковской цепи
text_model_pin = markovify.Text(text_pin)  # создаем Марковскую модель по Преступлению и наказанию

with open('oblomov.txt', encoding='utf-8') as f:
    text_oblomov = f.read()

# Создание модели марковской цепи
text_model_oblomov = markovify.Text(text_oblomov)

# Инициализация бота
bot = telebot.TeleBot('Your token')  # выводим токен бота


@bot.message_handler(commands=['start'])  # по команде старт начинаем игру
def main(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id,
                     f'{message.from_user.first_name}! Как твои дела? Ты хорошо знаешь произведения русских классиков? Сейчас проверим тебя. Нажми /generate, чтобы начать. Если нужна помощь, нажми /help.',
                     reply_markup=markup)


@bot.message_handler(commands=['help'])  # по команде хелп выводим пользователю информацию об игре
def helper(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(message.chat.id,
                     f'Это бот, который проверит твои знания по русской литературе. Твоя задача - угадать, с помощью чего сгенерирован текст: на основе Преступления и наказания или Обломова. Для генерации предложения нажми /generate.',
                     reply_markup=markup)


# Реагирует на любой текст
@bot.message_handler(content_types=['text'])  # если пользователь вводит текст, начинаем угадывать
def generate_message(message):
    pin_answer = text_model_pin.make_sentence()  # Генерация фразы
    pin_answer = [pin_answer, 1]
    oblomov_answer = text_model_oblomov.make_sentence()
    oblomov_answer = [oblomov_answer, 2]
    answers = [pin_answer, oblomov_answer]
    random_choose = random.choice(answers)  # рандомно выбираем предложение из одного из произведений
    model_answer = mistral_hugginchat.prompt(
            f'Из какого произведения это предложение? {random_choose[0]}')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == "/generate":
        bot.send_message(message.chat.id, text=f"На основе какого произведения сгенерировано это предложение? "
                                               f"{random_choose[0]}")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Преступление и наказание')
        btn2 = types.KeyboardButton('Обломов')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text="Попробуй отгадать", reply_markup=markup)

    if message.text == "Преступление и наказание" and random_choose[1] == 1:
        bot.send_message(message.chat.id, text="Правильно, это Преступление и наказание.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        winner = open('./winner.jpg', 'rb')
        bot.send_photo(message.chat.id, winner, reply_markup=markup)
        bot.send_message(message.chat.id, text=f"Ответ модели Mixtral: {model_answer}")
        bot.send_message(message.chat.id, text="Если вы хотите продолжить, нажмите /generate. Чтобы вывести облако частотных слов (тех слов, из которых составлялось задание) одного из произведений, нажмите ПиН-облако или Обломов-облако, соответственно")
        btn1 = types.KeyboardButton('ПиН-облако')
        btn2 = types.KeyboardButton('Обломов-облако')
        btn3 = types.KeyboardButton('/generate')
        markup.add(btn1, btn2)
        markup.add(btn3)
        bot.send_message(message.chat.id, text="Выбери подходящий вариант", reply_markup=markup)
    elif message.text == "Обломов" and random_choose[1] == 2:
        bot.send_message(message.chat.id, text="Правильно. Это Обломов.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        winner = open('./winner.jpg', 'rb')
        bot.send_photo(message.chat.id, winner, reply_markup=markup)
        bot.send_message(message.chat.id, text=f"Ответ модели Mixtral: {model_answer}")
        bot.send_message(message.chat.id, text="Если вы хотите продолжить, нажмите /generate. Чтобы вывести облако частотных слов (тех слов, из которых составлялось задание) одного из произведений, нажмите ПиН-облако или Обломов-облако, соответственно")
        btn1 = types.KeyboardButton('ПиН-облако')
        btn2 = types.KeyboardButton('Обломов-облако')
        btn3 = types.KeyboardButton('/generate')
        markup.add(btn1, btn2)
        markup.add(btn3)
        bot.send_message(message.chat.id, text="Выбери подходящий вариант", reply_markup=markup)
    elif message.text == "Преступление и наказание" and random_choose[1] == 2:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, text="Нет, Это Обломов.")
        lost = open('./lost.jpg', 'rb')
        bot.send_photo(message.chat.id, lost, reply_markup=markup)
        bot.send_message(message.chat.id, text=f"Ответ модели Mixtral: {model_answer}")
        bot.send_message(message.chat.id, text="Если вы хотите продолжить, нажмите /generate. Чтобы вывести облако частотных слов (тех слов, из которых составлялось задание) одного из произведений, нажмите ПиН-облако или Обломов-облако, соответственно")
        btn1 = types.KeyboardButton('ПиН-облако')
        btn2 = types.KeyboardButton('Обломов-облако')
        btn3 = types.KeyboardButton('/generate')
        markup.add(btn1, btn2)
        markup.add(btn3)
        bot.send_message(message.chat.id, text="Выбери подходящий вариант", reply_markup=markup)
    elif message.text == "Обломов" and random_choose[1] == 1:
        bot.send_message(message.chat.id, text="Нет, Это Преступление и наказание.")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        lost = open('./lost.jpg', 'rb')
        bot.send_photo(message.chat.id, lost, reply_markup=markup)
        bot.send_message(message.chat.id, text=f"Ответ модели Mixtral: {model_answer}")
        bot.send_message(message.chat.id, text="Если вы хотите продолжить, нажмите /generate. Чтобы вывести облако частотных слов (тех слов, из которых составлялось задание) одного из произведений, нажмите ПиН-облако или Обломов-облако, соответственно")
        btn1 = types.KeyboardButton('ПиН-облако')
        btn2 = types.KeyboardButton('Обломов-облако')
        btn3 = types.KeyboardButton('/generate')
        markup.add(btn1, btn2)
        markup.add(btn3)
        bot.send_message(message.chat.id, text="Выбери подходящий вариант", reply_markup=markup)
    elif message.text == "Обломов-облако":
        cloud_oblomov = open('./wordcloud_oblomov.png', 'rb')
        bot.send_photo(message.chat.id, cloud_oblomov, reply_markup=markup)
        bot.send_message(message.chat.id, text=f"Это облако слов из произведения Обломов")
        bot.send_message(message.chat.id, text=f"Чтобы начать игру заново, нажмите /start.")
    elif message.text == "ПиН-облако":
        cloud_pin = open('./wordcloud_pin.png', 'rb')
        bot.send_photo(message.chat.id, cloud_pin, reply_markup=markup)
        bot.send_message(message.chat.id, text=f"Это облако слов из произведения Преступление и наказание")
        bot.send_message(message.chat.id, text=f"Чтобы начать игру заново, нажмите /start.")


# Запуск бота
bot.polling()
