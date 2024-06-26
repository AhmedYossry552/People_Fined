from database import  get_connection
from mail import mail
from flask import Blueprint,  request, session, g
from common_imports import *

verify_bp = Blueprint('verification', __name__)
@verify_bp.before_request
def before_request():
    g.db = get_connection()
def generate_verification_code():
    return str(random.randint(1000, 9999))

def generate_code(email):
    mysql =g.db
    cur = mysql.cursor()
    cur.execute("SELECT * FROM verification_codes WHERE email = %s", (email,))
    existing_user = cur.fetchone()
    if existing_user:
        cur.execute("DELETE FROM verification_codes WHERE email = %s", (email,))
        # Generate a verification code
    verification_code = generate_verification_code()
    # Store the verification code and email in the database
    cur = mysql.cursor()
    cur.execute("INSERT INTO verification_codes (email, code) VALUES (%s, %s)", (email, verification_code))
    mysql.commit()
    cur.close()
    # Send email with verification code
    msg = Message('Verification Code', sender='onlineshop500600@gmail.com', recipients=[email])
    msg.body = f"Your verification code is: {verification_code}"
    mail.send(msg)
    return redirect(url_for ('verification.verify_code'))


def verify(email, entered_code):
    
    mysql =g.db
    cur = mysql.cursor()
    cur.execute("SELECT * FROM verification_codes WHERE email = %s", (email,))
    stored_code = cur.fetchone()
    #return jsonify({'message': 'stpred'})
    if stored_code:  # Check if any rows were returned
       
        stored_code = stored_code[2]  # Access the 'code' column from the returned row
        print(stored_code)
        print(entered_code)
        if stored_code == entered_code:
            return True
    return False

# Route for verifying the code
@verify_bp.route('/verify_code', methods=['POST'])

def verify_code():
    mysql =g.db
    username =  request.form['username']
    password =  request.form['password']
    phone_number= request.form['phone_number']
    email = request.form['email']
    entered_code = request.form['code']
    token = request.form['token']
    city= request.form['city']
    lang = request.form['lng']
    lat = request.form['lat']
    notifications = request.form['notifications']
    print(phone_number)
    if verify(email, entered_code):
        # Perform actions for successful verification
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cur = mysql.cursor()
        cur.callproc('InsertUser',(username,  email,hashed_password, phone_number, token,lang, lat, city, notifications))
        mysql.commit()
        cur.close()
        return jsonify({'message': 'User registered successfully'})
    else:
        return jsonify({'message': 'the code is not correct.'})
        # Handle failed verification
@verify_bp.route('/verify_reset_code_password', methods=['GET', 'POST'])
def verify_reset_code_password():
    
    entered_code = request.form['code']
    email = request.form['email']
    if verify(email, entered_code):
        if request.method == 'POST':
          return jsonify({'message': 'Correct code.'})
    else:
        return jsonify({'message': 'Incorrect code try again.'})