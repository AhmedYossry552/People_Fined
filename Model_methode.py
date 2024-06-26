from flask import Blueprint, jsonify
from common_imports import *
Model_bp = Blueprint('Model_methode', __name__)

embedder = FaceNet()




def getClosetDistance(input_vector, results_map):
    embedder.metadata['distance_metric'] = 'euclidean'
    distances_map = {}

    for id, details in results_map.items():
        distance = embedder.compute_distance(input_vector, details['vector_image'])
        print(f"Distance between test img and {id} = {distance}")
        distances_map[id] = distance
 
    return sorted(distances_map.items(), key=lambda x: x[1])

def cropFaceFromImage(image):
        """
        Detect one face in the given image and crop it with a border.
        Return the cropped face with a suitable size for feeding to FaceNet Model.

        :param image_path: Path to the input image
        :return: Cropped face with suitable size if conditions are met
        """

        face_detector = dlib.get_frontal_face_detector()
        #nparr = np.frombuffer(img.read(), np.uint8)
        #image = cv.imdecode(nparr, cv.IMREAD_COLOR)
        # Check if the image was loaded successfully
        if image is None:
            raise FileNotFoundError("Error: Could not open or find the image.")

        # Convert the image to RGB (dlib expects RGB images)
        rgb_img =cv.cvtColor(image, cv.COLOR_BGR2RGB)

        # Detect faces in the image
        faces = face_detector(rgb_img)

        # Check if exactly one face was detected
        if len(faces) != 1:
            return None
        else :
        # Crop the face with a border
          x, y, w, h = faces[0].left(), faces[0].top(), faces[0].width(), faces[0].height()
          border = 10
          cropped_face = rgb_img[y-border:y+h+border, x-border:x+w+border]

        # Resize the cropped face to 160x160 pixels to make it suitable for FaceNet modeling
          resized_face = cv.resize(cropped_face, (160, 160))

        # Convert the cropped face to BGR format and add a border
          cropped_face_bgr = cv.cvtColor(cropped_face, cv.COLOR_RGB2BGR)
          border_color = (0, 255, 0)  # green border
          border_thickness = 5
          final_face = cv.copyMakeBorder(cropped_face_bgr, border_thickness, border_thickness, border_thickness, border_thickness, cv.BORDER_CONSTANT, value=border_color)
          return final_face


def get_embedding(face_img):
    face_img = face_img.astype('float32') # 3D(160x160x3)
    face_img = np.expand_dims(face_img, axis=0)
    # 4D (Nonex160x160x3)
    yhat= embedder.embeddings(face_img)
    return yhat[0] # 512D image (1x1x512)


