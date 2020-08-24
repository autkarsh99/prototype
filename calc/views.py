import json
import urllib.request
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import wikipedia
from googlesearch import search
import webbrowser
import random
import string
'''import random
from models import Joke
from controllers.utils import send_message'''

# Create your views here.
def home(request):
    return render(request,'home.html',{'name':'Kiran'});

def add(request):

    val1 = int(request.GET['num1'])
    val2 = int(request.GET['num2'])
    res = val1 + val2
    
    return render(request,'result.html',{'result':res})

@csrf_exempt
def ranger(request):
    resp = json.loads(request.body)
    message = resp["message"]["text"].split()
    # Break message by space, if [0] == "/sum" sum = [1]+[2]
    if message[0] == "/sum":
        response = int(message[1]) + int(message[2])
    
    elif message[0] == "/diff":
        response = int(message[2]) - int(message[1])
    
    elif message[0] == "/multi":
        response = int(message[1]) * int(message[2])

    elif message[0] == "/fact":
        factorial = 1
        num=int(message[1])
        if num < 0:
            response="Sorry, factorial does not exist for negative numbers"
        elif num == 0:
            response="The factorial of 0 is 1"
        else:
            for i in range(1,num + 1):
                factorial = factorial*i
            response="The factorial of "+str(num)+" is "+str(factorial)
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
                response="No module named 'google' found"
            for j in search(message,tld="co.in",num=10,stop=10,pause=2):
                response= response+str(j)'''
        response=""
        for j in search(message,tld="co.in",num=10,stop=10,pause=2):
                response=str(response)+str(j)
    elif message[0]=="/jokes":
        url=urllib.request.urlopen("https://official-joke-api.appspot.com/jokes/random")
        response=url.read().decode()
    elif message[0]=="/gen":
        response="Enter Your Favourite Subject:"
        message.pop(0)
        message="".join(message)
        #n=message[1]
        password_characters = string.punctuation
        n1=string.digits
        p1=''.join(random.choice(n1) for j in range(3))
        p = ''.join(random.choice(password_characters) for i in range(1))
        c=n[0].upper()+p+n[1:]+p1
        response=str(c)
   
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
            else:
                response=num+" is not a prime number"
        except:
            response = "Please enter correct format" # don't run next condition
        
    elif message[0].lower() == "hi" or message[0].lower() == "hello" or message[0].lower() == "hey":
        response = "Hello there! I'm Anjan's bot, type / to see list of commands :)"
    else:
        response = "Hi, I don't know this command"
    
    urllib.request.urlopen("https://api.telegram.org/bot1256419034:AAFCS-K4_JFxHhqnitL-QrdxNQzy32K3fsg/sendMessage?chat_id=967409586&text="+urllib.parse.quote(str(response)))
    return HttpResponse('Success')