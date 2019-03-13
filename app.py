import requests
from flask import Flask, render_template, request, flash, abort, url_for
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'some_secret'



db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/' , methods=['GET', 'POST'])
@app.route('//')
def index():

    if request.method == 'POST':
        new_city = request.form.get('city')
        new_city = new_city.upper()
        if new_city:
            q = db.session.query(City).filter_by(name=new_city).all()
            url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
            response = requests.get(url.format(new_city))
            if response.status_code == 404:
                abort(404)
            if not q:
                new_city =new_city.upper()
                new_city_obj = City(name=new_city)
                db.session.add(new_city_obj)
                db.session.commit()
            else:
                flash('Oops!!!This city already exists! ')

    cities = City.query.all()



    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'

    weather_data = []

    for city in cities:

        response = requests.get(url.format(city.name))

        if response.status_code == 404:
            abort(404)

        else:

            r = response.json()
            print(r)

            weather = {
                'city' : city.name,
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon'],
                'lon':r['coord']['lon'],
                'lat':r['coord']['lat'],
            }

            weather_data.append(weather)


    return render_template('weather.html', weather_data=weather_data)


@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    # defining function
    return render_template("404.html"), 404



if __name__ == '__main__':
    app.run(port = 8000)