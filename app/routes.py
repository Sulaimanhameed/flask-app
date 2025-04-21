from flask import render_template, redirect, url_for, flash, request, Blueprint
from datetime import datetime
from app import db
from app.models import Car

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    cars = Car.query.order_by(Car.created_at.desc()).all()
    return render_template('index.html', cars=cars)

@bp.route('/car/<int:car_id>')
def view_car(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('view_car.html', car=car)

@bp.route('/car/add', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        try:
            # Get and validate form data
            make = request.form.get('make', '').strip()
            model = request.form.get('model', '').strip()
            year = request.form.get('year', '').strip()
            color = request.form.get('color', '').strip()
            price = request.form.get('price', '').strip()
            description = request.form.get('description', '').strip()

            if not all([make, model, year]):
                flash('Make, model and year are required!', 'danger')
                return redirect(url_for('main.add_car'))

            try:
                car = Car(
                    make=make,
                    model=model,
                    year=int(year),
                    color=color if color else None,
                    price=float(price) if price else None,
                    description=description if description else None
                )
                db.session.add(car)
                db.session.commit()
                flash('Car added successfully!', 'success')
                return redirect(url_for('main.index'))
            except ValueError as e:
                db.session.rollback()
                flash(f'Invalid input: {str(e)}', 'danger')
                return redirect(url_for('main.add_car'))
        except Exception as e:
            db.session.rollback()
            flash(f'Database error: {str(e)}', 'danger')
            return redirect(url_for('main.add_car'))

    current_year = datetime.now().year
    return render_template('car_form.html', car=None, current_year=current_year)

@bp.route('/car/edit/<int:car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    car = Car.query.get_or_404(car_id)

    if request.method == 'POST':
        try:
            # Get and validate form data
            make = request.form.get('make', '').strip()
            model = request.form.get('model', '').strip()
            year = request.form.get('year', '').strip()
            color = request.form.get('color', '').strip()
            price = request.form.get('price', '').strip()
            description = request.form.get('description', '').strip()

            if not all([make, model, year]):
                flash('Make, model and year are required!', 'danger')
                return redirect(url_for('main.edit_car', car_id=car.id))

            try:
                car.make = make
                car.model = model
                car.year = int(year)
                car.color = color if color else None
                car.price = float(price) if price else None
                car.description = description if description else None
                db.session.commit()
                flash('Car updated successfully!', 'success')
                return redirect(url_for('main.view_car', car_id=car.id))
            except ValueError as e:
                db.session.rollback()
                flash(f'Invalid input: {str(e)}', 'danger')
                return redirect(url_for('main.edit_car', car_id=car.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Database error: {str(e)}', 'danger')
            return redirect(url_for('main.edit_car', car_id=car.id))

    current_year = datetime.now().year
    return render_template('car_form.html', car=car, current_year=current_year)

@bp.route('/car/delete/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    try:
        car = Car.query.get_or_404(car_id)
        db.session.delete(car)
        db.session.commit()
        flash('Car deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting car: {str(e)}', 'danger')
    return redirect(url_for('main.index'))
