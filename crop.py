import tensorflow as tf
import numpy as np
import cv2
# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def draw_rect( box,original_image):
    # print(box)
    height,width,_=original_image.shape
    y_min = int(max(1, (box[0] * height)))
    x_min = int(max(1, (box[1] * width)))
    y_max = int(min(height, (box[2] * height)))
    x_max = int(min(width, (box[3] * width)))
    
    # draw a rectangle on the image

    cv2.rectangle(original_image, (x_min, y_min), (x_max, y_max), (255, 255, 255), 2)
    cropped_image=original_image[y_min:y_max,x_min:x_max]
    
    return cropped_image

def cropp(img):
    new_img = cv2.resize(img, (384,384))

    interpreter.set_tensor(input_details[0]['index'], [new_img])

    interpreter.invoke()
    scores = interpreter.get_tensor(
        output_details[0]['index'])
    rects = interpreter.get_tensor(
        output_details[1]['index'])



    for index, score in enumerate(scores[0]):
        if score > 0.5:
            temp_image=draw_rect(rects[0][index],img)
            return temp_image
            