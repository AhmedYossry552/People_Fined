
from common_imports import *
from verification import verify ,generate_code
from database import  get_connection
from flask import Blueprint,  request, session, g

user_bp = Blueprint('user', __name__)
 
 # This runs before every request 
@user_bp.before_request
def before_request():
    g.db = get_connection()


 
@user_bp.route('/register', methods=['POST'])
def register():
    mysql =g.db
    email = request.json['email']
    cur = mysql.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cur.fetchone()
    if existing_user:
        return jsonify({'message': 'this email used before enter another email '})
    else :
        from verification import generate_code
        generate_code(email)
        return jsonify({'message': 'A verification code has been sent to your email.'})

@user_bp.route('/login', methods=['POST'])
def login():
    mysql =g.db
    email = request.json['email']
    password = request.json['password']

    cur = mysql.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    print(user[1])

    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            session['logged_in'] = True
            cur.close()
            return jsonify({'message': 'Login successful','id': user[0]})
        else:
            cur.close()
            return jsonify({'message': 'Invalid email or password'})
    else:
        cur.close()
        return jsonify({'message': 'Invalid email or password'})

# User Logout
@user_bp.route('/logout', methods=['POST'])
def logout():
    
    if 'logged_in' in session:
        session.pop('logged_in', None)
        return jsonify({'message': 'Logged out successfully'})
    else:
        return jsonify({'error': 'User not logged in'}), 401
    

@user_bp.route('/update_user', methods=['POST'])
def update_field():
    mysql =g.db
    try:
        id =  request.form['id']
        username =  request.form['username']
        phone_number =  request.form['phone_number']
        lang =  request.form['lng']
        lat =  request.form['lat']
        city =  request.form['city']
        notifiactions =  request.form['notifications']

        cursor = mysql.cursor()
        cursor.callproc('EditUserProfile', (id, username, lang, lat, city, phone_number, notifiactions,))
        mysql.commit()

        if cursor:
            return jsonify({'message': 'Stored procedure executed successfully.'}), 200
        else:
            return jsonify({'message': 'Error executing stored procedure.'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/profile_user', methods=['get'])
def user_profile():
   
    mysql =g.db
    try:
        id =  request.form['id']
        cursor =  mysql.cursor()
        cursor.callproc('GetUserProfile', (id,))
        #cursor.fetchall
        row=None
        for result in cursor.stored_results():
            row = result.fetchone()
        cursor.close()    
        if row :
                return jsonify(row)
        else:
                return jsonify({'message': 'User not found.'}), 404
        

    except Exception as e:
        return jsonify({'error': str(e)}), 500   



@user_bp.route('/forgot_password', methods=['POST'])
def forgot_password():
    mysql =g.db

    if request.method == 'POST':
        email = request.form.get('email')
        cur = mysql.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        if user:
         generate_code(email)
         return jsonify({'message': 'A verification code has been sent to your email.'})
        else:
            return jsonify({'message': 'Email address not found.'})

@user_bp.route('/set_new_password', methods=['POST'])
def set_new_password():
    mysql =g.db
    email = request.form['email']
    new_password = request.form['new_password']
    # Hash the new password
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    # Update the user's password in the database
    cur = mysql.cursor()
    cur.execute("UPDATE users SET password_hash = %s WHERE email = %s", (hashed_password, email))
    mysql.commit()
    cur.close()
    return jsonify({'message': 'Password has been reset successfully.'})
# Route for resetting password
