import telebot
from telebot import types
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
import django
er='Red Rock'
# Set the correct path to your settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "erp.settings")
django.setup()

# Now you can import Django ORM modules
from login.models import CustomUser
from production.models import *


welcome_message = "Welcome to ERP!"
bot = telebot.TeleBot('6819700281:AAHPDNNdQ6LlQwBl6IPkZz8VhAJ25go9nOU')

# Placeholder functions for database interactions
def user_exists(user_id):
    try:
        user = get_object_or_404(CustomUser, telegram_id=user_id)
        return user
    except CustomUser.DoesNotExist:
        return False  # Placeholder, replace with actual logic

def get_user_orders(user_id):
    # Implement logic to fetch orders from the database based on user_id
    # Return a list of orders
    return [{'order_id': 1}, {'order_id': 2}]  # Placeholder, replace with actual logic

@bot.message_handler(commands=['start'])
def question(message):
    user_id = message.from_user.id
    # Check if user exists in the database
    if user_exists(user_id):
        bot.reply_to(message, f'Welcome To {er}')
    else:
        bot.reply_to(message, 'You are not registered in our system.')

@bot.message_handler(commands=['login'])
def question(message):
    user_id = message.from_user.id
    # Check if user exists in the database
    if user_exists(user_id):
        markup = types.InlineKeyboardMarkup(row_width=4)
        all=AllocatedMaterialProductionFlow.objects.filter(cutting=True,cutting_unit='Unit 1',cutting_status='Pending')
        no_ans=[]
        for i in all:
         
            no_ans=types.InlineKeyboardButton(f" Sales No-{i.sales_order.sale_number} --> Product {i.Material.material.name} -->  {i.Material.rowItem.product_name} ", callback_data=f'{i.pk}-det')
            markup.add(no_ans)
        bot.send_message(message.chat.id, 'Sales Order Details', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'You need to register before using this command.')
def send_tabular_data(tablefor,chat_id,tabular_data):

    markup = types.InlineKeyboardMarkup(row_width=len(tabular_data[0]))

    for row in tabular_data:
        buttons = [types.InlineKeyboardButton(cell, callback_data=cell) for cell in row]
        markup.row(*buttons)

    bot.send_message(chat_id, tablefor, reply_markup=markup)
def send_requirements(callback,kp):
    # bot.send_message(callback.message.chat.id, 'What is lighter?')
    resp=AllocatedMaterialProductionFlow.objects.get(pk=kp)
    header=['Material','Unit','Description','Quantity','Allocated']
    details=[resp.Material.material.name,resp.Material.unit,resp.Material.rowItem.product_description,resp.Material.order_quantity,resp.Material.allocated]
    send_tabular_data('Requirements Data:',callback.message.chat.id,[header,details])
def send_produced(callback,kp):
    # bot.send_message(callback.message.chat.id, 'What is lighter?')
    resp=AllocatedMaterialProductionFlow.objects.get(pk=kp)
    header=['sales_order','product','productionUnit','TotalQuantity','TotalLeft']
    details=[header]
    res=ProducedRow.objects.filter(alloca=resp)
    for r in res:
        details.append([r.sales_order.sale_number,r.product.name,r.productionUnit,str(r.TotalQuantity),str(r.TotalLeft)])
    send_tabular_data('Produced Data:',callback.message.chat.id,details)
def send_options(message,ids):
    markup = types.InlineKeyboardMarkup(row_width=4)
    change_status=types.InlineKeyboardButton(f"Change_status ", callback_data=f'{ids}-status')
    get_req=types.InlineKeyboardButton(f"Get Requirements", callback_data=f'{ids}-requirements')
    updateproduction=types.InlineKeyboardButton(f"Update Production", callback_data=f'{ids}-update')
    get_productionde=types.InlineKeyboardButton(f"Get Productions", callback_data=f'{ids}-produced')
    markup.add(change_status,get_req,updateproduction,get_productionde)
    bot.send_message(message.chat.id, 'Sales Order Details', reply_markup=markup)    
def save(message,pk,callback):
    if message is not None:
        resp=AllocatedMaterialProductionFlow.objects.get(pk=pk)
        if (resp.last_update_cutting+int(message.text))>resp.Material.rowItem.quantity:
            bot.reply_to(message, f'You Cant Produce quntity Greater than Left {resp.Material.rowItem.quantity-resp.last_update_cutting}')
            send_options(message,pk)
            return 
        resp.last_update_cutting+=int(message.text)
        resp.save()
        
        
        ProducedRow(
            alloca=resp,
            sales_order= resp.sales_order ,
            product= Product.objects.get(name=resp.Material.rowItem.product_name) ,
            unit = resp.Material.unit,
            productionUnit='Cutting',
            TotalprocessedNow= message.text,
            TotalProcessed=resp.last_update_cutting,
            TotalQuantity=resp.Material.rowItem.quantity,
            TotalLeft=resp.Material.rowItem.quantity-resp.last_update_cutting,
        ).save()
        send_options(message,pk)
        resp=AllocatedMaterialProductionFlow.objects.get(pk=pk)
        if resp.Material.rowItem.quantity-resp.last_update_cutting==0:
            bot.reply_to(message, f'Cutting for This Product Is Completed Please Change Status')
            change_status(callback,pk)
            send_options(message,pk)
            
            return
    else:
        pass
    
    
def start_form(callback):
    pk=callback.data.split('-')[0]
    send_requirements(callback,pk)
    handler_function = lambda message: save(message, pk,callback)
    bot.reply_to(callback.message, 'Enter The Quantity Cut')
    bot.register_next_step_handler(callback.message, handler_function)
    # send_requirements(callback,pk)
    
    
def change_status(callback,kp):
    alc=AllocatedMaterialProductionFlow.objects.get(id=kp)
    alc.cutting_status='Completed'
    alc.save()
    bot.reply_to(callback.message, f'Status Of Allocation {alc.Material}  is Changed to Completed')
    






@bot.callback_query_handler(func=lambda call: True)
def answer(callback):
    if callback.message:
        if callback.data:
            if callback.data.find('det')>-1:
                send_options(callback.message,callback.data)
            if callback.data.find('requirements')>-1:
                pk=callback.data.split('-')[0]
                send_requirements(callback,pk)
            if callback.data.find('update')>-1:
                start_form(callback)
            if callback.data.find('produced')>-1:
                pk=callback.data.split('-')[0]
                send_produced(callback,pk)
            if callback.data.find('status')>-1:
                pk=callback.data.split('-')[0]
                change_status(callback,pk)

bot.polling()
