from flask import Blueprint,  request, session, g
from common_imports import *

from database import  get_connection
home_bp = Blueprint('home', __name__)

@home_bp.before_request
def before_request():
    g.db = get_connection() 
@home_bp.route('/home_lost', methods=['Get'])
def H_lost():
    mysql =g.db
    cur = mysql.cursor()
    cur.execute("SELECT * FROM lost_people ORDER BY id DESC LIMIT 5")
    rows = cur.fetchall()
   
        #return jsonify({'message': rows})
          
        # Convert rows to a list of dictionaries for JSON response
       
    if(len(rows)>0):
         
          results = {}
          final_result=[]
          for row in rows:
             result = {
                'person_name': row[1],
                'age': row[2],
                'date_of_lost': row[3],
                'phone_number': row[4],
                'email': row[5],
                'png_ref': row[6],
                'lng': row[8],
                'lat': row[9],
                'gender':row[10]
             }
             results[row[0]]=result
          for key, item in results.items():
    # Extract the image path from the item
             image_path = item['png_ref']
    # Construct the image URL and add it to the item
             item['image_url'] =url_for('report.get_photo', filename=image_path)

    mysql.commit()
         
             
    return jsonify(results)    

@home_bp.route('/home_find', methods=['Get'])
def H_find():
    mysql =g.db
    cur = mysql.cursor()
    cur.execute("SELECT * FROM find_people ORDER BY id DESC LIMIT 5")
   
    rows = cur.fetchall()
   
        #return jsonify({'message': rows})
          
        # Convert rows to a list of dictionaries for JSON response
       
    if(len(rows)>0):
         
          results = {}
          final_result=[]
          for row in rows:
             result = {
                'person_name': row[1],
                'age': row[2],
                'date_of_lost': row[3],
                'phone_number': row[4],
                'email': row[5],
                'png_ref': row[6],
                'lng': row[8],
                'lat': row[9],
                'gender':row[10]
             }
             results[row[0]]=result
          for key, item in results.items():
    # Extract the image path from the item
            image_path = item['png_ref']

    # Construct the image URL and add it to the item
            item['image_url'] = url_for('report.get_photo', filename=image_path)        
    return jsonify(results)  


#@home_bp.route('/home_1', methods=['POST'])

#def send_push_notification():
    #from pyfcm import FCMNotification
    #push_service = FCMNotification(api_key="AAAAOgpzEww:APA91bH5E6zMNhbVZHHyepP2m0MDzOCdYMV3P1prvL_fimLMujYj8r6AGTuJZX5R0HQeOZiEu-rjKcNsUO_MLmxtX-braubUv2_lL5zxvvdMoFsbM2izJWbYQPzdBsW88qTb6nFQ8Ta-")
   # result = push_service.notify_single_device(registration_id="ARVxEKGb7eejNLCFEtPXijiWHl02z638ySYRM9jUEVT3q21XtKh9rxqeCwX0yXeLXSwnLE", message_title="ahmedyossry", message_body="ahmedyossry")
   # return result



@home_bp.route('/send_notification', methods=['POST'])

def send_notification():
    from flask import Flask, request, jsonify
    import requests
    import json
    FCM_SERVER_KEY = 'AAAAOgpzEww:APA91bH5E6zMNhbVZHHyepP2m0MDzOCdYMV3P1prvL_fimLMujYj8r6AGTuJZX5R0HQeOZiEu-rjKcNsUO_MLmxtX-braubUv2_lL5zxvvdMoFsbM2izJWbYQPzdBsW88qTb6nFQ8Ta-'
    

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + FCM_SERVER_KEY
    }

    payload = {
        'to': 'eHrfoMsJQtuSld7sN0lkwV:APA91bHUpLAwKFS7uJW0hRr5xnYYR0OKxwOjR-PRgZEH5VJTKPobBNUckCfxLYFn047ns-ARVxEKGb7eejNLCFEtPXijiWHl02z638ySYRM9jUEVT3q21XtKh9rxqeCwX0yXeLXSwnLE',
        'notification': {
            'title': 'ahmedyossry',
            'body': 'ahmedyossry',
        }
    }

    response = requests.post('https://fcm.googleapis.com/fcm/send', headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return jsonify({'message': 'Notification sent successfully'}), 200
    else:
        return jsonify({'error': 'Failed to send notification'}), 400
