from tkinter import *
from PIL import ImageTk, Image
import requests

url = 'https://api.openweathermap.org/data/2.5/weather'
api_key = '7806769197630ee3fc5205fbd12edee6'
iconUrl = 'https://openweathermap.org/img/wn/{}@2x.png'

def getWeather(city):
    params = {'q': city, 'appid': api_key, 'lang': 'tr'}
    data = requests.get(url, params=params).json()
    if 'main' in data:
        city = data['name'].capitalize()
        country = data['sys']['country']
        temp = int(data['main']['temp'] - 273.15)
        icon = data['weather'][0]['icon']
        condition = data['weather'][0]['description']
        return city, country, temp, icon, condition
    return None

def main():
    city = cityEntry.get()
    weather = getWeather(city)
    if weather:
        LocationLabel['text'] = '{}, {}'.format(weather[0], weather[1])
        tempLabel['text'] = '{}°C'.format(weather[2])
        conditionLabel['text'] = weather[4].capitalize()
        icon = ImageTk.PhotoImage(Image.open(requests.get(iconUrl.format(weather[3]), stream=True).raw))
        iconLabel.configure(image=icon)
        iconLabel.image = icon
        headerLabel = Label(app, text='SAAT', font=('Arial', 18, 'bold'), bg='#87CEEB', fg='white')
        headerLabel.pack(pady=10)

    else:
        LocationLabel['text'] = 'Şehir bulunamadı'
        tempLabel['text'] = ''
        conditionLabel['text'] = ''
        iconLabel.configure(image='')
        iconLabel.image = None

app = Tk()
app.geometry('350x500')
app.title('BD Hava Durumu')
app.configure(bg='#87CEEB')

headerLabel = Label(app, text='Hava Durumu Uygulaması', font=('Arial', 18, 'bold'), bg='#87CEEB', fg='white')
headerLabel.pack(pady=10)

cityEntry = Entry(app, justify='center', font=('Arial', 14))
cityEntry.pack(fill=BOTH, ipady=10, ipadx=18, pady=5, padx=20)
cityEntry.focus()

searchButton = Button(app, text='Arama', font=('Arial', 15), bg='#4CAF50', fg='white', command=main)
searchButton.pack(fill=BOTH, ipady=10, padx=20)

iconLabel = Label(app, bg='#87CEEB')
iconLabel.pack(pady=10)

LocationLabel = Label(app, font=('Arial', 24, 'bold'), bg='#87CEEB', fg='white')
LocationLabel.pack()

tempLabel = Label(app, font=('Arial', 40, 'bold'), bg='#87CEEB', fg='white')
tempLabel.pack()

conditionLabel = Label(app, font=('Arial', 20), bg='#87CEEB', fg='white')
conditionLabel.pack()

app.mainloop()
