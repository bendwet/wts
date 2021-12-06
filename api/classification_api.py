import tensorflow as tf
from keras.models import load_model
from matplotlib import pyplot as plt
from PIL import Image, ImageEnhance
import numpy as np
from flask import Flask, request
from flask_cors import CORS
import json


def prepare_data(test_image):
    """

    Preparing image to be sent into model
    """

    # print('Load test image')

    # open image
    image_open = Image.open(test_image)
    # sharpen image
    sharpen_img = ImageEnhance.Sharpness(image_open)
    sharpened_img = sharpen_img.enhance(1.0)
    # increase contrast of image
    contrast_img = ImageEnhance.Contrast(sharpened_img)
    contrasted_img = contrast_img.enhance(10.0)
    # convert image to rgb
    rgb_image = contrasted_img.convert('RGB')
    # todo : look into array as image portrayed on plot is near perfect image
    # convert image to array
    rgb_image_array = tf.keras.preprocessing.image.img_to_array(rgb_image)
    print(rgb_image_array.shape)

    # convert full sized image to grayscale
    gray_full_size_img = tf.image.rgb_to_grayscale(rgb_image_array)
    # squeeze to remove colour channel for plotting
    squeeze_gray_full_img = np.squeeze(gray_full_size_img)
    resized_img = tf.image.resize(gray_full_size_img, [28, 28])
    # squeeze resized grayscale image
    grayscale_image = np.squeeze(resized_img)

    # print('Contrasted image')
    plt.imshow(rgb_image_array, cmap='gray')
    plt.show()

    print('gray scale image')
    plt.imshow(squeeze_gray_full_img, cmap='gray')
    plt.show()

    print('gray scale resized image')

    plt.imshow(grayscale_image, cmap='gray')
    plt.show()

    # todo : detect if image is mostly white, and invert if required
    # invert image colors
    inverted_image = 255 - resized_img
    # apply ReLU to the image to set any pixel value below threshold to 0 (0 is black in this case)
    relu_layer = tf.keras.layers.ReLU(threshold=200)
    # apply the ReLU function to the image
    cleaned_inverted_image = relu_layer(inverted_image)

    # normalize values to scale them between 0-1
    cleaned_inverted_image = cleaned_inverted_image / 255

    # squeeze image for plotting
    cleaned_squeeze_image = np.squeeze(cleaned_inverted_image)

    print('Image after relu applied')

    plt.imshow(cleaned_squeeze_image, cmap='gray')
    plt.show()

    # add batch size of 1 to image
    cleaned_inverted_image = tf.expand_dims(cleaned_inverted_image, axis=0)

    return cleaned_inverted_image


def trained_model(predict_img):
    model = load_model('models/improved_dropout_model')
    model.summary()
    print(predict_img.shape)
    predict_img = tf.expand_dims(predict_img, axis=0)
    print(predict_img.shape)
    prediction_list = model.predict(predict_img)
    print(prediction_list)
    prediction = np.argmax(prediction_list)
    print(prediction)
    # convert to json object
    json_prediction = json.dumps(str(prediction))
    return json_prediction


app = Flask(__name__)
CORS(app)


@app.route('/', methods=['GET'])
def index():

    return 'this is a test message'


@app.route('/predict', methods=['POST', 'GET'])
def predict_output():
    # todo : detect upper or lower case eg file vs File vs FILE
    image_file = request.files.get('file')
    print(image_file)
    prepared_img = prepare_data(image_file)
    return trained_model(prepared_img[0])


if __name__ == '__main__':
    print(tf.__version__)
    # img = prepare_data()
    # trained_model(img)
    app.run(host="0.0.0.0")
