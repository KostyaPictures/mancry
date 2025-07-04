from winreg import *
import re
from datetime import *
from time import sleep

today=datetime.today()


new_key = CreateKey(HKEY_CURRENT_USER, "SOFTWARE\ManCry")
try:
    last_cry, _ = QueryValueEx(new_key, "last")
except FileNotFoundError:
    SetValueEx(new_key, "last", 0, REG_SZ, "0")
    SetValueEx(new_key, "FirstAsk", 0, REG_SZ, "1")
    SetValueEx(new_key, "delay", 0, REG_SZ, "0")

    SetValueEx(new_key, "_won", 0, REG_SZ, "0")
    SetValueEx(new_key, "_lost", 0, REG_SZ, "0")
    SetValueEx(new_key, "_win-streak", 0, REG_SZ, "0")
    SetValueEx(new_key, "_months", 0, REG_SZ, "0")

won, _ = QueryValueEx(new_key, "_won")
lost, _ = QueryValueEx(new_key, "_lost")
win_streak, _ = QueryValueEx(new_key, "_win-streak")
months, _ = QueryValueEx(new_key, "_months")
won=int(won)
lost=int(lost)
win_streak=int(win_streak)
months=int(months)


def ask():
    global future_date, first_input
    first_ask, _ = QueryValueEx(new_key, "FirstAsk")
    if first_ask=="1":
        print("На протяжении скольки месяцев ты хочешь не плакать?")
        while True:
            first_input=input()
            garbage=re.search(r'[^0-9]', first_input)
            if garbage==None:
                if int(first_input)>0:
                    SetValueEx(new_key, "delay", 0, REG_SZ, str((int(first_input)*30)))
                    break
                else:
                    print("Чтобы доказать, что ты мужик, нужно выбрать период побольше.")
            else:
                print("Укажи только цифру!")
        SetValueEx(new_key, "FirstAsk", 0, REG_SZ, "0")
        
        curent_delta = timedelta(days=(int(first_input)*30))
        future_date = today + curent_delta

        SetValueEx(new_key, "last", 0, REG_SZ, str(today))
        print("Отлично. Теперь ты можешь плакать только после",future_date)
        sleep(3)
        print("\n\n\n\n")
ask()

print("Ты плакал сегодня? Да/Нет")
cryed_today=input()

delay, _ = QueryValueEx(new_key, "delay")
last_cry, _ = QueryValueEx(new_key, "last")

delay=timedelta(days=int(delay))
last_cry=datetime.strptime(last_cry,'%Y-%m-%d %H:%M:%S.%f')
allow=last_cry+delay
future_date=allow


def up_to_date(today_date:datetime, allowed_date:datetime):
    global future_date, lost, won, win_streak, months, first_input
    if today_date.timestamp()<allowed_date.timestamp():
        print("Ты провалил! Тебе нельзя было плакать до",future_date)
        SetValueEx(new_key, "last", 0, REG_SZ, str(today))
        SetValueEx(new_key, "FirstAsk", 0, REG_SZ, "1")
        lost+=1
        SetValueEx(new_key, "_win-streak", 0, REG_SZ, "0")
        win_streak=0
        print("\nКоличество твоих побед: "+str(won)+"\nКоличество проигрышей: "+str(lost)+"\nПобед подряд: "+str(win_streak)+"\nОбщее кол-во продержанных месяцев: "+str(months))
    else:
        print("Ты хорошо продержался и доказали свою силу воли. Ты настоящий мужчина.")
        SetValueEx(new_key, "last", 0, REG_SZ, str(today))
        SetValueEx(new_key, "FirstAsk", 0, REG_SZ, "1")
        won+=1
        win_streak+=1
        months+=first_input
        print("\nКоличество твоих побед: "+str(won)+"\nКоличество проигрышей: "+str(lost)+"\nПобед подряд: "+str(win_streak)+"\nОбщее кол-во продержанных месяцев: "+str(months))



while True:
    if cryed_today=="Да" or cryed_today=="Д" or cryed_today=="lf" or cryed_today=="Lf" or cryed_today=="да" or cryed_today=="д" or cryed_today=="yes" or cryed_today=="Yes" or cryed_today=="YES":
        up_to_date(today,allow)
        break
    if cryed_today=="Нет" or cryed_today=="Не" or cryed_today=="нет" or cryed_today=="Н" or cryed_today=="ytn" or cryed_today=="Ytn" or cryed_today=="не" or cryed_today=="н" or cryed_today=="no" or cryed_today=="NO" or cryed_today=="No":
        print("Молодец! Хорошо справляешься!\n\nКоличество твоих побед: "+str(won)+"\nКоличество проигрышей: "+str(lost)+"\nПобед подряд: "+str(win_streak)+"\nОбщее кол-во продержанных месяцев: "+str(months))
        break
    else:
        print("Ответ не совсем понятен. Нужно напечатать чётко \"Да\" или чётко \"Нет\"")
        break




SetValueEx(new_key, "_won", 0, REG_SZ, str(won))
SetValueEx(new_key, "_lost", 0, REG_SZ, str(lost))
SetValueEx(new_key, "_win-streak", 0, REG_SZ, str(win_streak))
SetValueEx(new_key, "_months", 0, REG_SZ, str(months))