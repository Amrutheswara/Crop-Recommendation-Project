from flask import Flask,render_template,request
import pickle
import requests,json
import numpy as np
import json

app=Flask(__name__)

@app.route('/getweather')
def getweather():
    city = request.args.get("cty")
    print("get weather is called")
    api_key = "db5fad12e57afac9a458953e957a8bdb"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]-273.15
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        msg=str(current_temperature)+","+str(current_humidity)
        d={"flag":"1","temp": current_temperature,"hum":current_humidity}
    else:
        d={"flag":"0","temp":0,"hum":0}
    jsonobj=json.dumps(d,indent=4)
    return jsonobj

@app.route('/fetchweather',methods=['POST','GET'])
def fetchweather():
    if request.method=='POST':
        city=request.form['city']
        print(city)
        api_key = "db5fad12e57afac9a458953e957a8bdb"
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + api_key + "&q=" + city
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            temp=current_temperature-273.15
            hum=current_humidity
            flag="1"
        else:
            flag="0"
            temp=0
            hum=0
        return render_template('crop.html',f=flag,t=temp,h=hum)


@app.route('/result',methods=['POST','GET'])
def result():
    if request.method=='POST':
        temp=float(request.form['temp'])
        humidity=float(request.form['humidity'])

        testdata=np.array([[temp,humidity]])

        file=open('knncrop.pkl','rb')
        model=pickle.load(file)

        pred=model.predict(testdata)

        msg=f"Recommended Crop Is : {pred[0]}"
        #return render_template('crop.html', res=msg, img=f"{pred[0]}.jpg",f="1")
        print(msg)
        return pred[0]




@app.route('/',methods=['POST','GET'])
def index():

    if request.method=='POST':
        username=request.form['username']



        password=request.form['password']

        if username=="admin" and password=="admin":
            return render_template('crop.html')
        else:
            return render_template('login.html',msg="Login failed")

    return render_template('login.html')

if __name__=='__main__':
   app.run(debug=True,host="0.0.0.0")

