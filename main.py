from unittest import result
from flask import Flask, render_template , request,redirect, url_for,flash

app = Flask(__name__)
app.secret_key=b'secret_key_for_session_management'

cars = [
    {'id': 1, 'brand': 'Toyota', 'model': 'Corolla', 'year': 2020, 'price': 1500000},
    {'id': 2, 'brand': 'Honda', 'model': 'Civic', 'year': 2019, 'price': 1200000},
    {'id': 3, 'brand': 'Ford', 'model': 'Mustang', 'year': 2021, 'price': 3500000}
]

@app.route('/')
def index():
  return render_template('index.html', title="Home Page", cars=cars)

@app.route('/cars')
def show_cars():
  return render_template('car/cars.html', title="Car Page", cars=cars)

@app.route('/car/new_car', methods=['GET', 'POST'])
def new_car():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        year = int(request.form['year'])
        price = int(request.form['price'])

        if cars:
            new_id = cars[-1]['id'] + 1
        else:
            new_id = 1


        car = {
            'id': new_id,
            'brand': brand,
            'model': model,
            'year': year,
            'price': price
        }
        cars.append(car)
        flash('New car added successfully!', 'success')

        return redirect(url_for('show_cars'))

    return render_template('car/new_car.html', title="New Car Page")


@app.route('/car/<int:car_id>/delete', methods=['GET', 'POST'])
def delete_car(car_id):
    for car in cars:
        if car['id'] == car_id:
            cars.remove(car)
            flash('Car deleted successfully!', 'success')
            break
    return redirect(url_for('show_cars'))

@app.route('/edit_car/<int:car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    for c in cars:
        if c['id'] == car_id:
            car = c
            break
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        year = int(request.form['year'])
        price = int(request.form['price'])

        for car in cars:
            if car['id'] == car_id:
                car['brand'] = brand
                car['model'] = model
                car['year'] = year
                car['price'] = price
                break
        flash('Update car added successfully!', 'success')

        return redirect(url_for('show_cars'))
    
    return render_template('car/edit_car.html', title="Edit Car", car=car)

@app.route('/car/search')
def search_car():
    brand = request.args.get('brand').lower()
    tmp_cars = []
    for car in cars:
        if brand in car['brand'].lower():
            tmp_cars.append(car)

    return render_template('car/search_car.html', title="Search Car Page", cars=tmp_cars)

            