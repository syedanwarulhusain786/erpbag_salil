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
bot = telebot.TeleBot('6501204045:AAFd09yo-vWCA2bqDcNcF0boNJ4QCGdKNpg')

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
        markup = types.InlineKeyboardMarkup(row_width=4)
        all=ReadyToDispatch.objects.filter(status='Pending')
        # no_ans=[]
        # for i in all:
         
        #     no_ans=types.InlineKeyboardButton(f" Sales No-{i.sales_order.sale_number} --> Product {i.Material.material.name} -->  {i.Material.rowItem.product_name} ", callback_data=f'{i.pk}-det')
        readyPack=types.InlineKeyboardButton(f"Pack ", callback_data=f'pack')
        # readyDispatch=types.InlineKeyboardButton(f"Dispatch", callback_data=f'dispatch')
        
        markup.add(readyPack)
        bot.send_message(message.chat.id, 'Select Option', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'You need to register before using this command.')
def send_tabular_data(tablefor,chat_id,tabular_data):

    markup = types.InlineKeyboardMarkup(row_width=len(tabular_data[0]))

    for row in tabular_data:
        buttons = [types.InlineKeyboardButton(cell, callback_data=cell) for cell in row]
        markup.row(*buttons)

    bot.send_message(chat_id, tablefor, reply_markup=markup)
def send_requirements(callback):
    # bot.send_message(callback.message.chat.id, 'What is lighter?')
    resp=ReadyToDispatch.objects.filter(status='Pending')
    header=['Order','product','quantity','entry_date','Completed','status','Update']
    
    ded=[header]
    for red in resp:
        ded.append([red.sales_order.sale_number,red.product.name,red.quantity,str(red.entry_date),str(red.ledt),red.status,str(f'{red.pk}-update')])
    send_tabular_data('Requirements Data:',callback.message.chat.id,ded)
def send_produced_pack(callback,kp):
    # bot.send_message(callback.message.chat.id, 'What is lighter?')
    resp=ReadyToDispatch.objects.filter(status='Packed')
    header=['Order','product','quantity','entry_date','Completed','Dispatched','status','Update']
    
    ded=[header]
    for red in resp:
        ded.append([red.sales_order.sale_number,red.product.name,red.quantity,str(red.entry_date),str(red.ledt),str(red.disp_left),red.status,str(f'{red.pk}-dispatch')])
    send_tabular_data('Dispatched Data:',callback.message.chat.id,ded)
def send_options(message,ids):
    markup = types.InlineKeyboardMarkup(row_width=4)
    get_req=types.InlineKeyboardButton(f"Get Pack", callback_data=f'{ids}-det')
    # updateproduction=types.InlineKeyboardButton(f"Update Production", callback_data=f'{ids}-update')
    get_productionde=types.InlineKeyboardButton(f"Get Dispatch", callback_data=f'{ids}-produced')
    markup.add(get_req,get_productionde)
    bot.send_message(message.chat.id, 'Select Options', reply_markup=markup)    
def save(message,pk,callback):
    if message is not None:
        resp=ReadyToDispatch.objects.get(pk=pk)
        if (resp.ledt+int(message.text))>resp.quantity:
            bot.reply_to(message, f'You Cant Produce quntity Greater than Left {resp.quantity-resp.ledt}')
            send_options(message,pk)
            return 
        resp.ledt+=int(message.text)
        resp.save()
        
        
        # ReadyToDispatch.objects.get_or_create(
        # alloca = resp.alloca,
        # product_stock=resp.product_stock,
        # sales_order = resp.sales_order,
        # product =Product.objects.get(name=resp.product.name),
        # quantity = Decimal(message.text),
        # cost_of_single = Decimal(resp.cost_of_single),
        # status='Packed'
        # )
        
        resp=ReadyToDispatch.objects.get(pk=pk)
        if resp.quantity-resp.ledt==0:
            bot.reply_to(message, f'Packing for This Product Is Completed')
            resp.status='Packed'
            resp.save()
            # change_status(callback,pk)
            # send_options(callback.message,callback.data)
            
            return
    else:
        pass
    
def start_form(callback):
    pk=callback.data.split('-')[0]
    # send_requirements(callback,pk)
    handler_function = lambda message: save(message, pk,callback)
    bot.reply_to(callback.message, 'Enter The Quantity Packed')
    bot.register_next_step_handler(callback.message, handler_function)

def dispatch_save(message,pk,callback):
    if message is not None:
        resp=ReadyToDispatch.objects.get(pk=pk)
        if (resp.disp_left+int(message.text))>resp.quantity:
            bot.reply_to(message, f'You Cant Dispatch quntity Greater than Left {resp.quantity-resp.disp_left}')
            send_options(message,pk)
            return 
        resp.disp_left+=int(message.text)
        resp.save()
        
        
        # ReadyToDispatch.objects.get_or_create(
        # alloca = resp.alloca,
        # product_stock=resp.product_stock,
        # sales_order = resp.sales_order,
        # product =Product.objects.get(name=resp.product.name),
        # quantity = Decimal(message.text),
        # cost_of_single = Decimal(resp.cost_of_single),
        # status='Packed'
        # )
        
        resp=ReadyToDispatch.objects.get(pk=pk)
        if resp.quantity-resp.disp_left==0:
            bot.reply_to(message, f'This Product Is Dispatched')
            resp.status='Dispatched'
            resp.save()
            # change_status(callback,pk)
            # send_options(callback.message,callback.data)
            
            return
    else:
        pass
    
def dispatch_start_form(callback):
    pk=callback.data.split('-')[0]
    # send_requirements(callback,pk)
    handler_function = lambda message: dispatch_save(message, pk,callback)
    bot.reply_to(callback.message, 'Enter The Quantity To be Dispatched')
    bot.register_next_step_handler(callback.message, handler_function)





@bot.callback_query_handler(func=lambda call: True)
def answer(callback):
    if callback.message:
        if callback.data:
            send_options(callback.message,callback.data)
            if callback.data.find('det')>-1:
                send_requirements(callback)

            
            if callback.data.find('produced')>-1:
                pk=callback.data.split('-')[0]
                send_produced_pack(callback,pk)

            if callback.data.find('update')>-1:
                    start_form(callback)
            if callback.data.find('dispatch')>-1:
                    dispatch_start_form(callback)
bot.polling()
