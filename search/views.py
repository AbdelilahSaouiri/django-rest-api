from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from tensorflow.keras.applications import Xception
from tensorflow.keras.applications.xception import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
from .serializers import ImageUploadSerializer

model = Xception(weights="imagenet")

def classify_image(image_file):
    image = Image.open(image_file).resize((299, 299)) 
    image = img_to_array(image)  
    image = np.expand_dims(image, axis=0)  
    image = preprocess_input(image)  
    predictions = model.predict(image)  
    labels = decode_predictions(predictions)  
    return labels[0]

@api_view(['POST'])
def image_classification(request):
    if 'image' not in request.FILES:
        return Response({"error": "No image provided"}, status=400)

    serializer = ImageUploadSerializer(data=request.FILES)
    if serializer.is_valid():
        image_file = request.FILES['image']
        predictions = classify_image(image_file)
        result = [
            {"description": description, "score": score}
            for (_, description, score) in predictions
        ]
        return Response({"predictions": result})
    
    return Response(serializer.errors, status=400)
