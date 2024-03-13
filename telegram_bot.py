import telebot
from telebot import types

TOKEN = ''  #put the token from the FatherBot in telegram 
bot = telebot.TeleBot(TOKEN)

# choosing
(
    TYPES_OF_FOOD,
    MILK_FOR_COFFEE,
    FLAVOUR_FOR_COFFEE,
    FOOD_SELECTION,
    CUSTOMIZING_ORDER,
    SIZE_OF_DRINK,
    YES_NO,
    MILK_FOR_MATCHA,
    SELECTION_DRINK,
    WAITING_PAYMENT_CONFIRMATION,
    FLAVOUR_FOR_MATCHA,
    TYPES_OF_SALAD,
    TYPES_OF_CAKE,
    TYPES_OF_MACARON
) = range(14)

user_states = {}
user_choice = {}

milkTypesByCoffe = {
    "cappuccino": ['Soy Milk', 'Coconut Milk'],
    "raf": ['Soy Milk', 'Coconut Milk', 'Cow Milk', 'Almond Milk'],
    "latte": ['Soy Milk', 'Coconut Milk', 'Cow Milk', 'Almond Milk']
}
milkTypesByMatcha = {
    "ice matcha": ['Soy Milk', 'Coconut', "Almond Milk", "Cow Milk", "Coconat Milk"],
    "hot matcha": ['Soy Milk', 'Coconut', "Almond Milk", "Cow Milk"],
    "matcha raf": ['Soy Milk', 'Coconut', "Almond Milk"]
}

flavorTypesByCoffee = {
    "cappuccino": ['Vanilla', 'Caramel', 'Hazelnut', 'No Flavour'],
    "raf": ['Vanilla', 'Caramel', 'Hazelnut', 'No Flavour', 'Brauni'],
    "latte": ['Vanilla', 'Caramel', 'Hazelnut', 'No Flavour', 'Brauni']
}
flavorTypesByMatcha = {
    "ice matcha": ['Vanilla', 'Caramel', 'Hazelnut', 'No Flavour'],
    "matcha raf": ['Vanilla', 'Caramel', 'Hazelnut', 'No Flavour', 'Brauni'],
    "hot matcha": ['Vanilla', 'Caramel', 'Hazelnut', 'No Flavour', 'Brauni']
}


@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    greeting_message = f"Welcome to PERK {user_name}! Would you like to drink or eat something today?"
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Yes', "No")
    bot.send_message(message.chat.id, greeting_message, reply_markup=markup)
    user_states[message.chat.id] = YES_NO  # after greeting this line will ask is a user wants to drink or not


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == YES_NO)
def yes_no_selection(message):
    match message.text.lower():
        case "yes":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('Tea', 'Lemonade', 'Coffee', 'Matcha')
            bot.send_message(message.chat.id, 'Please choose your drink:', reply_markup=markup)
            user_states[message.chat.id] = SELECTION_DRINK
        case "no":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('Salat', 'Cakes', 'Macaron')
            bot.send_message(message.chat.id, 'Great choice! Now please choose type of meal:', reply_markup=markup)
            user_states[message.chat.id] = FOOD_SELECTION


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == SELECTION_DRINK)
def drink_selection(message):
    match message.text.lower():
        case "coffee":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('Raf', 'Cappuccino', 'Americano', 'Espresso', 'Latte')
            bot.send_message(message.chat.id, 'Please choose type of coffee:', reply_markup=markup)
            user_states[message.chat.id] = MILK_FOR_COFFEE  # Update the state to select type of coffee
        case "matcha":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('Hot Matcha', "Ice Matcha", "Matcha Raf")
            bot.send_message(message.chat.id, 'Please choose type of Matcha', reply_markup=markup)
            user_states[message.chat.id] = MILK_FOR_MATCHA
        case "tea":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('Kazakh Tea', "Tashkent Tea", 'Blueberry Tea')
            bot.send_message(message.chat.id, 'Please choose type of Tea', reply_markup=markup)
            user_states[message.chat.id] = SIZE_OF_DRINK
        case "lemonade":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('Banana', "Blueberry")
            bot.send_message(message.chat.id, 'Please choose type of Matcha', reply_markup=markup)
            user_states[message.chat.id] = SIZE_OF_DRINK


# _________________________________Block for Matcha_________________________________
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == MILK_FOR_MATCHA)
def matcha_type_selection(message):
    user_choice[message.chat.id] = message.text.lower()
    types_of_milk = milkTypesByMatcha.get(user_choice[message.chat.id])
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for milk_type in types_of_milk:
        markup.add(milk_type)
    bot.send_message(message.chat.id, 'Please choose type of milk:', reply_markup=markup)
    user_states[message.chat.id] = FLAVOUR_FOR_MATCHA


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == FLAVOUR_FOR_MATCHA)
def flavour_matcha(message):
    flavour_for_matcha = flavorTypesByMatcha.get(user_choice[message.chat.id])  # Use the saved coffee choice
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for flavour_type in flavour_for_matcha:
        markup.add(flavour_type)
    bot.send_message(message.chat.id, 'Please choose type of flavour:', reply_markup=markup)
    user_states[message.chat.id] = SIZE_OF_DRINK


# ________________________________Block for Cofa________________________________________

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == MILK_FOR_COFFEE)
def coffee_type_selection(message):
    if message.text.lower() == "back":
        # Возвращаем пользователя к предыдущему шагу
        user_states[message.chat.id] = SELECTION_DRINK
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('Tea', 'Lemonade', 'Coffee', 'Matcha')
        bot.send_message(message.chat.id, 'Please choose your drink:', reply_markup=markup)
        return
    user_choice[message.chat.id] = message.text.lower()
    if message.text.lower() == "espresso" or message.text.lower() == "americano":
        user_states[message.chat.id] = SIZE_OF_DRINK
        size_of_drink(message)
        return
    milk_types = milkTypesByCoffe.get(user_choice[message.chat.id])
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for milk_type in milk_types:
        markup.add(milk_type)
    markup.add("Back")
    bot.send_message(message.chat.id, 'Please choose type of milk:', reply_markup=markup)
    user_states[message.chat.id] = FLAVOUR_FOR_COFFEE


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == FLAVOUR_FOR_COFFEE)
def flavour_selection(message):
    flavour_types = flavorTypesByCoffee.get(user_choice[message.chat.id])  # Use the saved coffee choice
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for flavour_type in flavour_types:
        markup.add(flavour_type)
    bot.send_message(message.chat.id, 'Please choose type of flavour:', reply_markup=markup)
    user_states[message.chat.id] = SIZE_OF_DRINK


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == SIZE_OF_DRINK)
def size_of_drink(message):
    if user_choice.get(message.chat.id) in ['americano', 'espresso']:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('0.2', '0.4')
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add('0.3', '0.5')
    bot.send_message(message.chat.id, 'Please choose a size for a coffee:', reply_markup=markup)
    user_states[message.chat.id] = TYPES_OF_FOOD


# ________________________________Food Selection____________________________________
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == TYPES_OF_FOOD)
def selecting_meal(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Salat', 'Cakes', 'Macaron', 'No Food')
    bot.send_message(message.chat.id, 'Great choice! Now please choose type of meal:', reply_markup=markup)
    user_states[message.chat.id] = FOOD_SELECTION


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == FOOD_SELECTION)
def food_selection(message):
    match message.text.lower():
        case "salat":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('Caesar', 'Fish Salat')
            bot.send_message(message.chat.id, 'Please choose type of salad:', reply_markup=markup)
            user_states[message.chat.id] = WAITING_PAYMENT_CONFIRMATION
        case "cakes":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('Napoleon', 'Medovik')
            bot.send_message(message.chat.id, 'Please choose type of cake', reply_markup=markup)
            user_states[message.chat.id] = WAITING_PAYMENT_CONFIRMATION
        case "macaron":
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add('Banana', "Caramel")
            bot.send_message(message.chat.id, 'Please choose type of macaron', reply_markup=markup)
            user_states[message.chat.id] = WAITING_PAYMENT_CONFIRMATION


#
#
# @bot.message_handler(func=lambda message: user_states.get(message.chat.id) == CUSTOMIZING_ORDER)
# def customizing_order(message):
#     user_states[message.chat.id] = WAITING_PAYMENT_CONFIRMATION
#     bot.send_message(message.chat.id, "Your order has been customized. Please confirm your payment.")


bot.polling()
