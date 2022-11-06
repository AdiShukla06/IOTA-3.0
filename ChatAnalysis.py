import regex
import pandas as pd
import numpy as np
import emoji
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import tkinter
from tkinter import *

frame=tkinter.Tk()
frame.title("Chat Analysis")
frame.geometry('600x600')
inputt=tkinter.Text(frame,height=5,width=10)
def date_time(s):
    pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
    result = regex.match(pattern, s)
    if result:
        return True
    return False

def find_author(s):
    s = s.split(":")
    if len(s)==2:
        return True
    else:
        return False

def getDatapoint(line):
    splitline = line.split(' - ')
    dateTime = splitline[0]
    date, time = dateTime.split(", ")
    message = " ".join(splitline[1:])
    if find_author(message):
        splitmessage = message.split(": ")
        author = splitmessage[0]
        message = " ".join(splitmessage[1:])
    else:
        author= None
    return date, time, author, message

data = []
conversation = 'WhatsApp Chat with Digant Bennett.txt'

with open(conversation, encoding="utf-8") as fp:
    fp.readline()
    messageBuffer = []
    date, time, author = None, None, None
    while True:
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        if date_time(line):
            if len(messageBuffer) > 0:
                data.append([date, time, author, ' '.join(messageBuffer)])
            messageBuffer.clear()
            date, time, author, message = getDatapoint(line)
            messageBuffer.append(message)
        else:
            messageBuffer.append(line)

df = pd.DataFrame(data, columns=["Date", 'Time', 'Author', 'Message'])
df['Date'] = pd.to_datetime(df['Date'])

# print(df.info())
# print(df.Author.unique())

total_messages = df.shape[0]


media_messages = df[df["Message"]=='<Media omitted>'].shape[0]


def split_count(text):
    emoji_list = []
    data = regex.findall(r'\X',text)
    for word in data:
        if any(char in emoji.EMOJI_DATA for char in word):
            emoji_list.append(word)
    return emoji_list
df['emoji'] = df["Message"].apply(split_count)


URLPATTERN = r'(https?://\S+)'
df['urlcount'] = df.Message.apply(lambda x: regex.findall(URLPATTERN, x)).str.len()
links = np.sum(df.urlcount)


media_messages_df = df[df['Message'] == '<Media omitted>']
messages_df = df.drop(media_messages_df.index)
messages_df['Letter_Count'] = messages_df['Message'].apply(lambda s : len(s))
messages_df['Word_Count'] = messages_df['Message'].apply(lambda s : len(s.split(' ')))
messages_df["MessageCount"]=1

l = ["Aditya Shukla", conversation[19:-4]]

total_emojis_list = list(set([a for b in messages_df.emoji for a in b]))
total_emojis = len(total_emojis_list)

total_emojis_list = list([a for b in messages_df.emoji for a in b])
emoji_dict = dict(Counter(total_emojis_list))
emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)


emoji_df = pd.DataFrame(emoji_dict, columns=['emoji', 'count'])
import plotly.express as px



text = " ".join(review for review in messages_df.Message)


def display_cloud():

    text = " ".join(review for review in messages_df.Message)
    stopwords = set(STOPWORDS)
    # Generate a word cloud image
    wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
    # Display the generated image:
    # the matplotlib way:
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    l = ["Aditya Shukla", conversation[19:-4]]
    for i in range(len(l)):
        dummy_df = messages_df[messages_df['Author'] == l[i]]
        text = " ".join(review for review in dummy_df.Message)
        stopwords = set(STOPWORDS)
        # Generate a word cloud image
        print('Author name', l[i])
        wordcloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)
        # Display the generated image
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")

        plt.show()
def display_stats():
    name1=mystring.get()
    newWindow=Toplevel(frame)
    newWindow.title("Statistics")
    newWindow.geometry("600x600")
    lbl = ImageLabel(newWindow)
    lbl.pack()
    lbl.load('background gif 2.gif')

    def date_time(s):
        pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
        result = regex.match(pattern, s)
        if result:
            return True
        return False

    def find_author(s):
        s = s.split(":")
        if len(s) == 2:
            return True
        else:
            return False

    def getDatapoint(line):
        splitline = line.split(' - ')
        dateTime = splitline[0]
        date, time = dateTime.split(", ")
        message = " ".join(splitline[1:])
        if find_author(message):
            splitmessage = message.split(": ")
            author = splitmessage[0]
            message = " ".join(splitmessage[1:])
        else:
            author = None
        return date, time, author, message

    data = []
    conversation = 'WhatsApp Chat with Digant Bennett.txt'

    with open(conversation, encoding="utf-8") as fp:
        fp.readline()
        messageBuffer = []
        date, time, author = None, None, None
        while True:
            line = fp.readline()
            if not line:
                break
            line = line.strip()
            if date_time(line):
                if len(messageBuffer) > 0:
                    data.append([date, time, author, ' '.join(messageBuffer)])
                messageBuffer.clear()
                date, time, author, message = getDatapoint(line)
                messageBuffer.append(message)
            else:
                messageBuffer.append(line)

    df = pd.DataFrame(data, columns=["Date", 'Time', 'Author', 'Message'])
    df['Date'] = pd.to_datetime(df['Date'])
    l= Label(newWindow,text=df.tail(20),justify=LEFT,bg="#233dff",fg='White',font=("Courier 8 bold")).place(x=0,y=20)

    # l1=Label(newWindow,text="Total messages in this conversation: ",justify=LEFT,bg="#233dff",fg='White',font=("Arial 8 bold")).place(x=0, y=340)
    # l2 = Label(newWindow, text=df.shape[0], justify=LEFT,bg="#233dff",fg='White',font=("Arial 8 bold")).place(x=300, y=340)
    # l3 = Label(newWindow, text=df[df["Message"] == '<Media omitted>'].shape[0], justify=LEFT,bg="#233dff",fg='White',font=("Arial 8 bold")).place(x=300, y=360)
    #l4=Label(newWindow,text="Total number of media messages: ",justify=LEFT,bg="#233dff",fg='White',font=("Arial 8 bold")).place(x=0, y=360)
    #l5=Label(newWindow,text="Number of emojis in a conversation: ",justify=LEFT,bg="#233dff",fg='White',font=("Arial 8 bold")).place(x=0, y=380)

    def split_count(text):
        emoji_list = []
        data = regex.findall(r'\X', text)
        for word in data:
            if any(char in emoji.EMOJI_DATA for char in word):
                emoji_list.append(word)
        return emoji_list

    df['emoji'] = df["Message"].apply(split_count)

    emojis = sum(df['emoji'].str.len())

    total_messages = df.shape[0]
    balee2=145
    #print("Total messages in this conversation: ", total_messages)



    media_messages = df[df["Message"] == '<Media omitted>'].shape[0]
    #print("Total number of media messages: ", media_messages)

    def split_count(text):
        emoji_list = []
        data = regex.findall(r'\X', text)
        for word in data:
            if any(char in emoji.EMOJI_DATA for char in word):
                emoji_list.append(word)
        return emoji_list

    df['emoji'] = df["Message"].apply(split_count)

    emojis = sum(df['emoji'].str.len())
    #print("Number of emojis in a conversation: ", emojis)
    #l6 = Label(newWindow, text=sum(df['emoji'].str.len()), justify=LEFT,bg="#233dff",fg='White',font=("Arial 8 bold")).place(x=300, y=380)
    print(" ")
    print(" ")

    URLPATTERN = r'(https?://\S+)'
    df['urlcount'] = df.Message.apply(lambda x: regex.findall(URLPATTERN, x)).str.len()
    links = np.sum(df.urlcount)
    l7=Label(newWindow,text="Chats between You and ",justify=LEFT,bg="#233dff",fg='White',font=("Arial 12 bold")).place(x=0, y=340)
    l8=Label(newWindow,text=name1,justify=LEFT,bg="#233dff",fg='White',font=("Arial 12 bold")).place(x=190, y=340)
    #print("Chats between You and ", name1)
    l9=Label(newWindow,text="Total Messages: ",justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=0, y=370)
    l10=Label(newWindow,text=total_messages,justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=300, y=370)
    l11=Label(newWindow,text="Number of Media Shared: ",justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=0, y=390)
    l12=Label(newWindow,text= media_messages,justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=300, y=390)
    l13=Label(newWindow,text="Number of Emojis Shared",justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=0, y=410)
    l14=Label(newWindow,text=emojis,justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=300, y=410)
    l15=Label(newWindow,text="Number of Links Shared",justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=0, y=430)
    l16=Label(newWindow,text=links,justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=300, y=430)
    #print("Total Messages: ", total_messages)
    #print("Number of Media Shared: ", media_messages)
    #print("Number of Emojis Shared", emojis)
    #print("Number of Links Shared", links)

    #print(" ")
    #print(" ")

    media_messages_df = df[df['Message'] == '<Media omitted>']
    messages_df = df.drop(media_messages_df.index)
    messages_df['Letter_Count'] = messages_df['Message'].apply(lambda s: len(s))
    messages_df['Word_Count'] = messages_df['Message'].apply(lambda s: len(s.split(' ')))
    messages_df["MessageCount"] = 1

    l = ["Aditya Shukla", conversation[19:-4]]

    total_emojis_list = list(set([a for b in messages_df.emoji for a in b]))
    total_emojis = len(total_emojis_list)

    total_emojis_list = list([a for b in messages_df.emoji for a in b])
    emoji_dict = dict(Counter(total_emojis_list))
    emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
    # for i in emoji_dict:
    #     print(i)

    for i in range(len(l)):
        # Filtering out messages of particular user
        if (i == 0):

            req_df = messages_df[messages_df["Author"] == l[0]]

            # print(f'Stats of {l[0]} -')
            #
            # print('Messages Sent', req_df.shape[0])

            words_per_message = (np.sum(req_df['Word_Count'])) / req_df.shape[0]
            # print('Average Words per message', words_per_message)

            media = media_messages_df[media_messages_df['Author'] == l[i]].shape[0]
            # print('Media Messages Sent', media)

            emojis = sum(req_df['emoji'].str.len())
            # print('Emojis Sent', emojis)

            links = sum(req_df["urlcount"])
            # print('Links Sent', links)
            l26 = Label(newWindow, text=f'Stats of {l[0]} -', justify=LEFT,bg="#233dff",fg='White',font=("Arial 12 bold")).place(x=580, y=150)
            l27 = Label(newWindow, text='Messages Sent', justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=580, y=190)
            l28 = Label(newWindow, text=req_df.shape[0], justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=790, y=190)
            l29 = Label(newWindow, text='Average Words per message', justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=580, y=210)
            l30 = Label(newWindow, text=words_per_message, justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=790, y=210)
            l31 = Label(newWindow, text='Media Messages Sent', justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=580, y=230)
            l32 = Label(newWindow, text=media, justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=790, y=230)
            l33 = Label(newWindow, text='Emojis Sent', justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=580, y=250)
            l34 = Label(newWindow, text=emojis, justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=790, y=250)
        elif (i==1):
            req_df = messages_df[messages_df["Author"] == l[1]]

            # print(f'Stats of {l[1]} -')
            #
            # print('Messages Sent', req_df.shape[0])

            words_per_message = (np.sum(req_df['Word_Count'])) / req_df.shape[0]
            # print('Average Words per message', words_per_message)

            media = media_messages_df[media_messages_df['Author'] == l[i]].shape[0]
            # print('Media Messages Sent', media)

            emojis = sum(req_df['emoji'].str.len())
            # print('Emojis Sent', emojis)

            links = sum(req_df["urlcount"])
            # print('Links Sent', links)
            l17=Label(newWindow,text=f'Stats of {l[1]} -',justify=LEFT,bg="#233dff",fg='White',font=("Arial 12 bold")).place(x=580, y=20)
            l18=Label(newWindow,text='Messages Sent',justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=580, y=60)
            l19 = Label(newWindow, text= req_df.shape[0], justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=790, y=60)
            l20 = Label(newWindow, text='Average Words per message', justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=580, y=80)
            l21 = Label(newWindow, text=words_per_message, justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=790, y=80)
            l22 = Label(newWindow, text='Media Messages Sent', justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=580, y=100)
            l23 = Label(newWindow, text=media, justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=790, y=100)
            l24 = Label(newWindow, text='Emojis Sent', justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=580, y=120)
            l25 = Label(newWindow, text=emojis, justify=LEFT,bg="#233dff",fg='White',font=("Arial 10 bold")).place(x=790, y=120)


        print(" ")
        print(" ")

    text = " ".join(review for review in messages_df.Message)
    lb35=Label(newWindow,text="There are {} words in all the messages.".format(len(text)),justify=LEFT,bg="#233dff",fg='White',font=("Arial 11 bold")).place(x=580, y=300)

    # print("There are {} words in all the messages.".format(len(text)))
def display_chart():
    fig = px.pie(emoji_df, values='count', names='emoji')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.show()





import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle

class ImageLabel(tk.Label):

    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)

#demo :

lbl = ImageLabel(frame)
lbl.pack()
lbl.load('background gif.gif')

button_1=tkinter.Button(frame,text="Word Cloud",bg="White",fg="#233dff",width="12",height="1",font='Areal',command=display_cloud)
button_2=tkinter.Button(frame,text="Stats",bg="White",fg="#233dff",width="12",height="1",font='Areal',command=display_stats)
button_3=tkinter.Button(frame,text="Pie Chart",bg="White",fg="#233dff",width="12",height="1",font='Areal',command=display_chart)
mystring = StringVar()

Entry(frame, textvariable = mystring).place(x=32, y=305)
button_1.place(x=24,y=506)
button_2.place(x=232,y=506)
button_3.place(x=436,y=506)



frame.mainloop()