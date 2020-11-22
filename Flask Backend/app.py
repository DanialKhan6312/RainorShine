import os
from flask import Flask, request,jsonify
import pandas as pd
import requests
from flask_ngrok import run_with_ngrok
import sklearn
from google.cloud import vision
import pickle
app = Flask(__name__)
#run_with_ngrok(app)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="hackwestern-296303-1a10456e3ecc.json"
params = {
    'access_key': 'f335d3187d095ae269e0cd3f0f24bf27',
    'query': 'Toronto'
}
@app.route('/')
def home():
    return "hi"
@app.route('/weather',methods=['GET'])
def weather():
    api_result = requests.get('http://api.weatherstack.com/current', params)

    api_response = api_result.json()

    place = api_response['location']['name']
    temp = api_response['current']['temperature']
    precip_rain = api_response['current']['precip']
    precip_snow = 0
    wind = api_response['current']['wind_speed']
    weather = "sunny"

    # weather is given in a weird code
    weatherCode = api_response['current']['weather_code']
    # less than 113 is sunny
    if (weatherCode <= 113):
        weather = "sunny"
    # between 113 and 143 is cloudy
    elif (weatherCode <= 143):
        weather = "cloudy"
    # between 122 and 230 is snowing
    elif (weatherCode < 230):
        weather = "snow"
    # between 230 and 326
    elif (weatherCode < 326):
        weather = "rain"
    # everything above 326 is snow again
    else:
        weather = "snow"
    # set the precipitation to either snow or rain
    # default set to rain, but if its snowing then swap
    if (weather == "snow"):
        precip_snow = precip_rain
        precip_rain = 0
    import csv
    csv_columns = ['Wind Speed','average temperature','precipitation','snow fall']
    dict_data = [
        {'Wind Speed':wind, 'average temperature': temp, 'precipitation': precip_rain,'snow fall':25}
    ]
    csv_file = "Names.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print("I/O error")
    data = pd.read_csv("Names.csv")
    model= pickle.load(open('model.sav', 'rb'))
    output = model.predict(data)
    out= output.tolist()
    Temp_item = [["Shorts", "Tanktops", "T-shirts"], ["Shorts", "Tanktops", "T-shirts"],
                 ["Jeans", "T-shirts", "Sweatpants", "Full sleeved shirts"],
                 ["Hoodies", "Sweaters", "Light jackets"], ["Hoodies", "Sweaters", "Light jackets"],
                 ["Light jackets", "Wind breakers"],
                 ["Coats", "Jackets"], ["Winter jackets", "toques"], ["Winter jackets", "Toques", "Scarfs"],
                 ["Winter jackets", "Toques", "Scarfs", "Gloves"]]
    Rain_item = [[""],["Umbrella"], ["Umbrella", "Raincoat", "Waterproof boots/shoes"], ["Snow boots"],
                 ["Snow boots", "Snow pants", "Earmufs"]]
    wet =int((out[0]-out[0]%10)/10)
    warmth = (out[0]%10)
    rain = "there is no rain, "
    heat ="it is freezing outside "
    if warmth <2:
        heat= "It is very hot outside "
    elif warmth <4:
        heat = "It is fairly warm outside "
    elif warmth <6:
        heat ="It is fairly moderate outside "
    elif warmth <8:
        heat = "It is cold outside "
    if wet ==1:
        rain= "there is light rain, "
    elif wet ==2:
        rain= "there is heavy rain, "
    elif wet ==3:
        rain= "there is light snow, "
    elif wet ==4:
        rain= "there is heavy snow, "
    sending =heat+"and "+rain+"here are some recomendations: "
    for i in range(len(Temp_item[warmth])):
        if (i !=(len(Temp_item[warmth])-1)):
            sending +=Temp_item[warmth][i]+", "
        else:
            sending +=Temp_item[warmth][i]+" "
    for j in range(len(Rain_item[wet])):
        if (j !=(len(Rain_item[wet])-1)):
            sending +=Rain_item[wet][j]+", "
        else:
            sending +=Rain_item[wet][j]+" "
    return jsonify(sending)

@app.route('/image',methods=['POST'])
def imagecheck():
    ans = ""
    ans1 = "You are dressed perfectly for the temperature"
    warmth = 0
    wet = 0
    api_result = requests.get('http://api.weatherstack.com/current', params)
    api_response = api_result.json()
    temp = api_response['current']['temperature']
    precip_rain = api_response['current']['precip']
    precip_snow = 0
    wind = api_response['current']['wind_speed']
    weatherCode = api_response['current']['weather_code']
    # less than 113 is sunny
    if (weatherCode <= 113):
        weather = "sunny"
    # between 113 and 143 is cloudy
    elif (weatherCode <= 143):
        weather = "cloudy"
    # between 122 and 230 is snowing
    elif (weatherCode < 230):
        weather = "snow"
    # between 230 and 326
    elif (weatherCode < 326):
        weather = "rain"
    # everything above 326 is snow again
    else:
        weather = "snow"
    # set the precipitation to either snow or rain
    # default set to rain, but if its snowing then swap
    if (weather == "snow"):
        precip_snow = precip_rain
        precip_rain = 0
    import csv
    csv_columns = ['Wind Speed', 'average temperature', 'precipitation', 'snow fall']
    dict_data = [
        {'Wind Speed': wind, 'average temperature': temp, 'precipitation': precip_rain, 'snow fall': precip_snow}
    ]
    csv_file = "Names.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dict_data:
                writer.writerow(data)
    except IOError:
        print("I/O error")
    data = pd.read_csv("Names.csv")
    model = pickle.load(open('model.sav', 'rb'))
    output = model.predict(data)
    out = output.tolist()
    wetp = int((out[0] - out[0] % 10) / 10)
    warmp = (out[0] % 10)
    if request.method == 'POST':
        file = request.files['pic']
        file.filename = "image.jpg"
        file_name = file.filename
        file.save(file_name)
        with open('./image.jpg', 'rb') as image_file:
            content = image_file.read()
        client = vision.ImageAnnotatorClient()
        response = client.label_detection({'content': content})
        labels = response.label_annotations
        print('Labels:')
        for label in labels[0:8]:
            print(label.description)
            if (label.description == "Jacket" or label.description == "Coat"):
                warmth = warmth + 7
            if (label.description == "Sweater" or label.description == "Hoodie"):
                warmth = warmth + 5
            if (label.description == "Hat"):
                warmth += 1
                wet = 1
            if (label.description == "gloves"):
                wet = 3
            if (label.description == "Boots"):
                wet = 4
                warmth += 1
            if (label.description == "Hood" or label.description == "Hoodie"):
                wet = 1
            if (label.description == "Umbrella"):
                wet = 2

        if (wetp >2 and wet <3):
            ans = "also you might want to be careful of snow"
        elif (wetp >0 and wet<1):
            ans="also you might want to grab an umbrella"
        elif (wetp ==0 and wet >0 and wet<3):
            ans = "also you probably won't need that umbrella"
        if ((warmp-warmth)<-1):
            ans1="You may be overdressed for the weather"
        elif((warmp-warmth)>1):
            ans1 = "You may be underdressed for the weather"


    out = ans1+" "+ans
    return out
if __name__ == '__main__':
   app.run()