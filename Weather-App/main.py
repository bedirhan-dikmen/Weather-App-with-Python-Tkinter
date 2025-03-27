from tkinter import *
from PIL import ImageTk, Image
import requests

# OpenWeatherMap API URL ve Anahtar
token = '7806769197630ee3fc5205fbd12edee6'
url = 'https://api.openweathermap.org/data/2.5/weather'
iconUrl = 'https://openweathermap.org/img/wn/{}@2x.png'

def getWeather(city):
    """Girilen şehrin hava durumu bilgilerini API'den alır"""
    try:
        params = {'q': city, 'appid': token, 'lang': 'tr'}
        data = requests.get(url, params=params).json()
        
        if data.get('cod') == 200:  # API isteği başarılı mı kontrol et
            city = data['name'].capitalize()
            country = data['sys']['country']
            temp = int(data['main']['temp'] - 273.15)  # Kelvin'i Celsius'a çevir
            icon = data['weather'][0]['icon']
            condition = data['weather'][0]['description'].capitalize()
            return city, country, temp, icon, condition
    except requests.exceptions.RequestException:
        return None
    return None

def updateWeather(event=None):
    """Arama butonuna basıldığında veya Enter tuşuna basıldığında çağrılır."""
    city = cityEntry.get().strip()
    
    if not city:
        return  # Boş girişleri engelle
    
    weather = getWeather(city)
    if weather:
        LocationLabel['text'] = f'{weather[0]}, {weather[1]}'
        tempLabel['text'] = f'{weather[2]}°C'
        conditionLabel['text'] = weather[4]
        
        icon = ImageTk.PhotoImage(Image.open(requests.get(iconUrl.format(weather[3]), stream=True).raw))
        iconLabel.configure(image=icon)
        iconLabel.image = icon
    else:
        LocationLabel['text'] = 'Şehir bulunamadı'
        tempLabel['text'] = ''
        conditionLabel['text'] = ''
        iconLabel.configure(image='')
        iconLabel.image = None

# Arayüzü oluştur
app = Tk()
app.geometry('350x500')
app.title('BD Hava Durumu')
app.configure(bg='#87CEEB')  # Açık mavi arkaplan

# Başlık etiketi
headerLabel = Label(app, text='Hava Durumu Uygulaması', font=('Arial', 18, 'bold'), bg='#87CEEB', fg='white')
headerLabel.pack(pady=10)

# Şehir giriş kutusu
cityEntry = Entry(app, justify='center', font=('Arial', 14))
cityEntry.pack(fill=BOTH, ipady=10, ipadx=18, pady=5, padx=20)
cityEntry.focus()
cityEntry.bind("<Return>", updateWeather)  # Enter tuşu ile arama yapma

# Arama butonu
searchButton = Button(app, text='Arama', font=('Arial', 15), bg='#4CAF50', fg='white', command=updateWeather)
searchButton.pack(fill=BOTH, ipady=10, padx=20)

# Hava durumu ikon etiketi
iconLabel = Label(app, bg='#87CEEB')
iconLabel.pack(pady=10)

# Şehir ve ülke bilgisi etiketi
LocationLabel = Label(app, font=('Arial', 24, 'bold'), bg='#87CEEB', fg='white')
LocationLabel.pack()

# Sıcaklık etiketi
tempLabel = Label(app, font=('Arial', 40, 'bold'), bg='#87CEEB', fg='white')
tempLabel.pack()

# Hava durumu durumu etiketi
conditionLabel = Label(app, font=('Arial', 20), bg='#87CEEB', fg='white')
conditionLabel.pack()

app.mainloop()
