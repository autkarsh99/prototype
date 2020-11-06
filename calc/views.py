import datetime
import json
import random
import urllib.request
#from google import beautifulsoup4
import wikipedia
from PyDictionary import PyDictionary
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from googlesearch import search as gsearch
import string
from .models import employee
import requests
import randfacts
import smtplib
from translate import Translator

dictionary=PyDictionary()
'''import random
from models import Joke
from controllers.utils import send_message'''

# Create your views here.
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('addrel99@gmail.com', 'Dhananjay@123')
    server.sendmail('addrel99@gmail.com', to, content)
    server.close()
def home(request):
    return render(request,'home.html',{'name':'Kiran'});
def signup(request):
    if request.method=='POST':
        name=request.POST['un']
        mobile=request.POST['mo']
        email=request.POST['em']
        x=employee(name=name,mobile=mobile,email=email)
        x.save()
        print("User Created")
        return redirect('/search')


    else:
        return render(request,'b.html')

def search(request):
    if request.method=='POST':
        srch=request.POST['srh']
        if srch:
            match=employee.objects.filter(Q(name__icontains=srch)|
            Q(email__icontains=srch))

            if match:
                return render(request,'search.html',{'sr':match})
            else:
                return HttpResponse("no result found")
        else:
            return HttpResponse('/search/')
    return render(request,'search.html')


def add(request):

    val1 = int(request.GET['num1'])
    val2 = int(request.GET['num2'])
    res = val1 + val2

    return render(request,'result.html',{'result':res})

@csrf_exempt
def ranger(request):
    resp = json.loads(request.body)
    user_id = str(resp["message"]["chat"]["id"])
    message = resp["message"]["text"]
    response = chatbot(message)
    urllib.request.urlopen("https://api.telegram.org/bot1256419034:AAFCS-K4_JFxHhqnitL-QrdxNQzy32K3fsg/sendMessage?chat_id="+user_id+"&text="+urllib.parse.quote(str(response)))
    return HttpResponse('Success')

@csrf_exempt
def sendBotMessage(request):
    response = chatbot(request.POST['message'])
    return HttpResponse(response)


@csrf_exempt
def chatbot(message):
    original_message = message
    message = original_message.split()
    # Break message by space, if [0] == "/sum" sum = [1]+[2]
    if message[0] == "/sum":
        numbers=original_message.replace('/sum','').split()
        s=0
        for x in numbers:
            c=int(x)
            s+=c
        j=' '.join(numbers)
        response="Sum of Given Number "+str(s)

    elif message[0] == "/diff":
        response = int(message[2]) - int(message[1])

    elif message[0] == "/multi":
        response = int(message[1]) * int(message[2])

    elif message[0] =="/power":
        response = int(message[1])**int(message[2])

    elif message[0] =="/sqrt":
        response = int(message[1])**(1/2)

    elif message[0] =="/cbrt":
        response = int(message[1])**(1/3)

    elif message[0] == "/fact":
        #try:
        factorial = 1
        num = int(message[1])
        if num < 0:
            response="Sorry, factorial does not exist for negative numbers"
        elif num == 0:
            response="The factorial of 0 is 1"
        else:
            for i in range(1,num + 1):
                factorial = factorial*i
                response="The factorial of "+str(num)+" is "+str(factorial)

        #except:
        #    response= "Error"
    elif message[0]=="/reword":
        l=message[0]
        r=l[::-1]
        if l==r:
            response="Word is Palindrome!"
        else:
            response="Word in not Palindrome!"
    elif message[0]=="/dict":
        response="Meaning: "+ str(dictionary.meaning(message[1]))+"<br><br>"+"Synonyms: "+str(dictionary.synonym(message[1]))+"<br><br>"+"Antonyms: "+str(dictionary.antonym(message[1]))

    elif message[0]=="/translate":
        try:
            tmessage=original_message.replace('/translate','').splitlines()
            omessage=tmessage[1]
            translator= Translator(to_lang="hi")
            translation = translator.translate(omessage)
            response="Your Translation: "+ str(translation)
        except:
            response="Failed to translate"

    elif message[0]=="/wiki":
        #c=message[1].lower()
        message.pop(0)
        message="".join(message)
        response=str(wikipedia.summary(message, sentences=5))
    elif message[0]=="/search":
        message.pop(0)
        message="".join(message)
        '''def search(message,tld='com',lang='en',num=10,start=0,stop=None,pause=2.0):
            try:
                from googleseach import search
            except ImportError:
                response = "No module named 'google' found"'''
        response = ""
        for j in gsearch(message, tld="co.in", num=10, stop=10, pause=2):
            response=str(response)+str(j)+str("\n")
    elif message[0]=="/jokes":
        url=urllib.request.urlopen("https://official-joke-api.appspot.com/jokes/random")
        response=url.read().decode()
    elif message[0]=="/gen":
        message="".join(message)
        n=message[0]
        password_characters = string.punctuation
        n1=string.digits
        p1=''.join(random.choice(n1) for j in range(7))
        p = ''.join(random.choice(password_characters) for i in range(4))
        c=n[0].upper()+p+n[1:]+p1
        response=str(c)

    elif message[0]=="/time":
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        response="Sir Time is: "+str(strTime)

    #/addcontact
    #name
    #phone
    #email
    elif message[0]=="/addcontact":
        try:
            contact_details = original_message.replace('/addcontact', '').splitlines()
            name=contact_details[1]
            mobile=contact_details[2]
            email=contact_details[3]
            x=employee(name=name,mobile=mobile,email=email)
            x.save()
            response = "Contact added!"
        except:
            response = "Please send details in correct format as below:"
            response += "<br>/addcontact<br>Name<br>Phone<br>Email"


    elif message[0] == "/searchcontact":
        srch = message[1]
        if srch:
            match=employee.objects.filter(Q(name__icontains=srch)|
            Q(email__icontains=srch))

            if match:
                response = "I got following results - <br><br>"
                for each_match in match:
                    response += each_match.name + "<br>"
                    response += each_match.mobile + "<br>"
                    response += each_match.email + "<br><br>"
            else:
                response = "No contact found"

    elif message[0]=="/sendmail":
        try:
            email_detail=original_message.replace('/sendmail','').splitlines()
            to=email_detail[1]
            content= email_detail[2]
            sendEmail(to, content)
            response = "Mail sent"
        except Exception as e:
            print(e)
            response="Not able to send email Sorry!"

    elif message[0]=="/help":
        response = "Here the things I can do" +"<br>"+ "/dict <word>: to find any word meaning with antonyms and Synonyms "+"<br>"+"/translate: to translate any sentence in Hindi language"+"<br>"+"/wiki <word>: to find any information on Wikipedia"+"<br>"+"/search <word>: to find any information on google.com"+"<br>"+"/addcontact: to add any contact detail on server"+"<br>"+"/searchcontact: to search any contact detail on server"+"<br>"+"/jokes: to get any randrom jokes"+"<br>"+"/facts: to get interesting random facts"+"<br>"+"/weather <City Name>: To get any details of Weather of any city"+"<br>"+"/gen: to generate random password"+"<br>"+"/sendmail: Used to send message through mail"+"<br>"+"/time: it can also show current time"

    elif message[0] == "/weather":
        api_key = "ac9ae5f24855de6ba928d40fc22af036"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = message[1].capitalize()
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        r = requests.get(complete_url)
        x = r.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            current_tempc = float(current_temperature) - 273.15 
            response = "Temperature (in Celcius) = "+str(current_tempc)+"<br> Atmospheric Pressure (in hPa unit) = "+str(current_pressure)+"<br> Humidity (in percent) = "+str(current_humidity)+"<br> Description = "+str(weather_description)
        else:
            response = "City Not Found"

    elif message[0]=="/facts":
        x= randfacts.getFact()
        response = str(x)

    elif message[0]=="/prime":
        try:
            num = int(message[1])
            if num > 1:
                for i in range(2,num):
                    if (num % i) == 0:
                        response=str(num)+" is not a prime number"
                        response=str(i)+" times "+str(num//i)+" is "+str(num)
                        break
                    else:
                        response=str(num)+" is a prime number"
            ##else:
                #response=num+" is not a prime number"
        except:
            response = "Please enter correct format" # don't run next condition

    elif message[0].lower() == "hi" or message[0].lower() == "hello" or message[0].lower() == "hey":
        response = "Hello there! I'm Anjan's bot, type /help to see list of commands :)"
    else:
        response = "Hi, I don't know this command"

    return response