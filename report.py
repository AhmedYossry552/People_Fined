from flask import Blueprint,g ,request,session
from common_imports import *
from Model_methode import get_embedding, cropFaceFromImage, getClosetDistance
from database import get_connection
import base64

connect_str = "DefaultEndpointsProtocol=https;AccountName=findercloud;AccountKey=oDYl6DvJDTNuHtS70fEGF9vGmHH8paEjeUcY5o6uj39WIxa7QY/ntd7Yf4UJk+pgDUArXRKqfh0i+AStK8fD2w==;EndpointSuffix=core.windows.net"
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_name = "uploads"
container_client = blob_service_client.get_container_client(container_name)

report_bp = Blueprint('report', __name__)

@report_bp.before_request
def before_request():
    g.db = get_connection()




@report_bp.route('/search', methods=['POST'])
def lost():
    mysql =g.db
    try:
        print("1")
        # Get data from the request
        check_lost = request.form['check_lost']
        user_id=request.form['user_id']
        person_name = request.form['person_name']
        age = request.form['age']
        date_of_lost = request.form['date']
        phone_number = request.form['phone_number']
        email = request.form['email']
        image = request.files['image']
        lng = request.form['lng']
        lat = request.form['lat']
        gender = request.form['gender']
        print("2")
        # Save image and process
        unique_filename = str(uuid.uuid4()) + os.path.splitext(image.filename)[-1]
        nparr = np.frombuffer(image.read(), np.uint8)
        image1 = cv.imdecode(nparr, cv.IMREAD_COLOR)
        # Create a blob client using the file name as the blob name
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=unique_filename)
        
        # Upload the file to Azure Blob Storage
        #blob_client.upload_blob(image1, overwrite=True)
        
        _, buffer = cv.imencode(os.path.splitext(image.filename)[-1], image1)
        blob_client.upload_blob(buffer.tobytes(), overwrite=True, content_settings=ContentSettings(content_type='image/jpeg'))
        cropped =cropFaceFromImage(image1)
        print("3")
        if cropped is not None:
            vector_image = get_embedding(cropped)
            vector = pickle.dumps(vector_image)
        else:
            return jsonify({'error': 'Image does not contain exactly one face or No Face'})
        print("4")

        # Database operations
       
        #cursor = mysql.cursor()
        cursor = mysql.cursor()
        
        cursor.callproc('search', (date_of_lost, age, gender,check_lost))
        for result in cursor.stored_results():
            rows = result.fetchall()
        
        print("5")

        if(len(rows)>0):
          print("6")
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
                'vector_image':pickle.loads(row[7]).tolist(),
                'lng': row[8],
                'lat': row[9],
                'gender':row[10],
                'user_id': row[11],
                'city': row[12],
                'note': row[13],
             }
             print("7")
             results[row[0]]=result 
             print("8")           
          closed_dis= getClosetDistance(vector_image,results)
          print("9")
          for id, distance in closed_dis:
              if(distance<=0.7):
                  final_result.append(results[id])
                  print("10")
          if len(final_result)==0 :
                print("11")
                cursor.callproc('InsertPerson', (person_name, age, date_of_lost, phone_number, email, vector, lng, lat, gender, unique_filename, user_id, check_lost))
                mysql.commit()
                cursor.close()
                print("12")
                return jsonify({'message': 'Person not found'})
          else:
                for item in final_result:
                    image_path = item['png_ref']
                   
                    item['image_url'] = url_for('report.get_photo', filename=image_path)
                    del item['vector_image']
                print("13")

                return jsonify({'final_result': final_result})
                
        else:
            print("14")
            cursor.callproc('InsertPerson', (person_name, age, date_of_lost, phone_number, email, vector, lng, lat, gender, unique_filename,user_id, check_lost))
            mysql.commit()
            cursor.close()
            print("15")
            return jsonify({'message': 'Person not found'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@report_bp.route('/get_photo/<filename>', methods=['GET'])
def get_photo(filename):
    try:
        # Create a blob client using the filename
        blob_client = blob_service_client.get_blob_client(container="uploads", blob=filename)
        
        # Download the blob's content to a BytesIO object
        blob_data = blob_client.download_blob().readall()
        blob_stream = BytesIO(blob_data)
        
        # Serve the file to the client
        return send_file(blob_stream, mimetype='image/jpeg', as_attachment=False, download_name=filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@report_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400
    
    try:
        # Create a blob client using the file name as the blob name
        nparr = np.frombuffer(file.read(), np.uint8)
        image1 = cv.imdecode(nparr, cv.IMREAD_COLOR)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)
        
        # Upload the file to Azure Blob Storage
       # blob_client.upload_blob(image1.tobytes, overwrite=True)
        

         # Convert image to bytes and upload with content settings
        _, buffer = cv.imencode(os.path.splitext(file.filename)[-1], image1)
        blob_client.upload_blob(buffer.tobytes(), overwrite=True, content_settings=ContentSettings(content_type='image/jpeg'))
        return jsonify({"message": "File uploaded successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    

            

