from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YourSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:!Qazxsw2@localhost/my_hotel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Example room data (in a real application, this would come from a database)
rooms = [
    ('101', 'Single Room'),
    ('102', 'Double Room'),
    ('103', 'Deluxe Room')
]

class Guest(db.Model):
    guest_id = db.Column(db.Integer, primary_key=True)
    guest_name = db.Column(db.String(255), nullable=False)
    contact_info = db.Column(db.String(255))

class Room(db.Model):
    room_number = db.Column(db.String(10), primary_key=True)
    # other room fields...

class Booking(db.Model):
    booking_id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.guest_id'), nullable=False)
    room_number = db.Column(db.Integer, db.ForeignKey('room.room_number'), nullable=False)
    check_in_date = db.Column(db.Date, nullable=False)
    check_out_date = db.Column(db.Date, nullable=False)
    # other booking fields...

class BookingForm(FlaskForm):
    guest_name = StringField('Guest Name', validators=[DataRequired()])
    room_number = SelectField('Room Number', choices=rooms, validators=[DataRequired()])
    check_in_date = DateField('Check-In Date', format='%Y-%m-%d', validators=[DataRequired()])
    check_out_date = DateField('Check-Out Date', format='%Y-%m-%d', validators=[DataRequired()])
    contact_info = StringField('Contact Information', validators=[DataRequired()])
    submit = SubmitField('Book Now')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    form = BookingForm()
    if form.validate_on_submit():
        for field in form:
            print(f"{field.name}: {field.data}")

        new_guest = Guest(guest_name=form.guest_name.data, contact_info=form.contact_info.data)
        db.session.add(new_guest)
        db.session.flush()  # Flush to get the ID of the new guest

        new_booking = Booking(
            guest_id = new_guest.guest_id,
            room_number = form.room_number.data,
            check_in_date = form.check_in_date.data,
            check_out_date = form.check_out_date.data
        )
        db.session.add(new_booking)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('booking.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)


# 在 app.py 中的 index 路由下方增加
@app.route('/check')
def check():
    # 此處你需要根據實際情況從資料庫中檢索預定資訊
    # 這裡假設使用 Booking 表格
    booking_data = Booking.query.all()

    # 根據實際情況，從 booking_data 中提取需要的資訊，組成列表
    data = [(booking.check_in_date, booking.check_out_date, booking.booking_id,
             booking.guest.guest_name, booking.guest.contact_info) for booking in booking_data]

    return render_template('check.html', data=data)
