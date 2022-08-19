import requests
import json
import time
import telebot
bot = telebot.TeleBot('5785089092:AAHUoBZleK-H3ZbdporV_d57QE_H68ru7MA');

#def
def search_data():#Функция ищет и приобразут базу даных в список
	response = requests.get("https://topdeck.ru/apps/toptrade/auctions")
	text=response.text
	for i in range(0,len(text)):
		if (text[(i-len('JSON.parse("')):i]=='JSON.parse("') and ('new ActiveAuctionsVM(' in text[(i-50):i]):
			break
	i1=0
	data='"'
	while True:
		if text[i+i1]=='"':break
		data+=text[i+i1]
		i1+=1
	data=data+'"'
	response = requests.get("https://topdeck.ru/apps/toptrade/auctions")
	data = json.loads(json.loads(data))
	return data

def auction_search(name,karteg):#Функция ищет в базе данных подходящие лоты
	auctions=[]
	for i in range(0,len(karteg)):
		if name.lower() in karteg[i]['lot'].lower():
			auctions.append(karteg[i])
	return auctions

def listconvers(list, data):#Функция преобразования списка с названиями карт в список с обектами касса card
	list_convert=[]
	for i in range(0,len(list)):
		list_convert.append(card(list[i], data))
	return list_convert

def id_search(list):#Функция составляет список с действующими id аукционов
	id_list=[]
	for i in range(0,len(list)):
		id_list.append([])
		for i1 in range(0,len(list[i].auctions_print())):
			id_list[i].append(list[i].auctions_print()[i1]['id'])
	print(id_list)
	return id_list

def text_start(list):#Вывод отслежываемых лотов
	text='Вот отслеживаемые карты:'+'\n'
	for i in range(0,len(list)):
		text+=str(i+1)+'-'+list[i]+'\n'
	return text

def lot_start(list):#Вывод первоночальной информации о лотах
	text=''
	for i in range(0,len(list)):
		text+=str(i+1)+'-'+list[i].name_print()+'\n'
		if len(list[i].auctions_print())==0:
			text+='Лотов нет'+'\n'
		else:
			for i1 in range(0,len(list[i].auctions_print())):
				if int(list[i].auctions_print()[i1]['current_bid'])>0:text+='/'+str(i1+1)+':'+list[i].auctions_print()[i1]['lot']+'\n'+'Ставка:'+list[i].auctions_print()[i1]['current_bid']+'\n'+'До окончания:'+list[i].auctions_print()[i1]['time_left']+'\n'+'Продавец:'+list[i].auctions_print()[i1]['seller']['name']+'('+list[i].auctions_print()[i1]['seller']['refs']+')'+'\n'+'Город:'+list[i].auctions_print()[i1]['seller']['city']+'\n'+'https://topdeck.ru/apps/toptrade/auctions/'+list[i].auctions_print()[i1]['id']+'\n'
				else:text+='/'+str(i1+1)+':'+list[i].auctions_print()[i1]['lot']+'\n'+'Ставка:'+'Нет ставок'+'\n'+'До окончания:'+list[i].auctions_print()[i1]['time_left']+'\n'+'Продавец:'+list[i].auctions_print()[i1]['seller']['name']+'('+list[i].auctions_print()[i1]['seller']['refs']+')'+'\n'+'Город:'+list[i].auctions_print()[i1]['seller']['city']+'\n'+'https://topdeck.ru/apps/toptrade/auctions/'+list[i].auctions_print()[i1]['id']+'\n'
		text+='\n'
	return text

def changes_cheak(list,list_new):#Функция проверяет на изменение действующих аукционов
	changes_list=[[],[]]#Лист куда записываются id.В первый лист аукционы переставшие действовать, а во второй появившиеся
	for i in range(0,len(list)):
		for  i1 in range(0,len(list[i])):
			if not(list[i][i1] in list_new[i]):
				changes_list[0].append(list[i][i1])
		for  i1 in range(0,len(list_new[i])):
			if not(list_new[i][i1] in list[i]):
				changes_list[1].append(list_new[i][i1])
	return changes_list

def present_auction(id, list):#Выводит информацию о аукционе
	for i in range(0,len(list)):
		for i1 in range(0,len(list[i].auctions_print())):
			if list[i].auctions_print()[i1]['id']==id:
				return list[i].auctions_print()[i1]['lot']+'\n'+'Ставка:'+list[i].auctions_print()[i1]['current_bid']+'\n'+'Продавец:'+list[i].auctions_print()[i1]['seller']['name']+'('+list[i].auctions_print()[i1]['seller']['refs']+')'+'\n'+'Город:'+list[i].auctions_print()[i1]['seller']['city']+'\n'+'https://topdeck.ru/apps/toptrade/auctions/'+list[i].auctions_print()[i1]['id']+'\n'
	return ''			

#class
class card(object):
	def __init__(self, name, data):
		self.name=name
		self.auctions=auction_search(self.name, data)#Все Лоты удовлетворяющие названию
	def auctions_print(self):
		return self.auctions
	def name_print(self):
		return self.name

#main 
cards_name=['Demonic Tutor','Rystic study','Force of Will','Force of Negation','Imposter Mech']#СПИСОК КАРТ ДЛЯ МОНИТОРИНГА

data=search_data()
cards=listconvers(cards_name, data)
idcard=id_search(cards)

time_sleep=10    #Периуд цикла

@bot.message_handler(content_types=['text'])#Основной цикл бота telegram
def get_text_messages(message):
	global data, cards, idcard, cards_name, time_sleep
	if message.text == "/start":
		bot.send_message(message.from_user.id, text_start(cards_name))
		bot.send_message(message.from_user.id, lot_start(cards))
		while True:
			time.sleep(time_sleep)														#!!!Главный цикл!!!
			new_data=search_data()
			new_cards=listconvers(cards_name, new_data)
			new_idcard=id_search(new_cards)
			changes_list=changes_cheak(idcard,new_idcard)

			if len(changes_list[0])>0:
				for i in range(0,len(changes_list[0])):
					bot.send_message(message.from_user.id, 'Этот лот перестал существовать:'+'\n'+present_auction(changes_list[0][i], cards))
			if len(changes_list[1])>0:
				for i in range(0,len(changes_list[1])):
					bot.send_message(message.from_user.id, 'Появился новый лот:'+'\n'+present_auction(changes_list[1][i],new_cards))
			data=new_data
			cards=new_cards
			idcard=new_idcard

bot.polling(none_stop=True, interval=1)	
