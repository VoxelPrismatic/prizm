print('IMPORTING')
open('mix/loc','w').write('IMPORTING')
print('> NUMPY')
import numpy as np
print('> CV2')
import cv2
print('> SCIPY')
import scipy.io as sio
import scipy.misc as smi
print('> TENSOR')
import tensorflow as tf
print('> OTHERS')
import os
import PIL
from PIL import Image, ImageOps
import time
import datetime
import discord
import asyncio
from random import randint

print('LOGGING IN')
open('mix/loc','w').write('LOGGING IN')
print('running generator')
client = discord.Client()

print('SUCCESS\nGRABBING DATA')
open('mix/loc','w').write('GRABBING DATA')
content_image_path = 'mix/s1.jpg'
style_image_path = 'mix/s2.jpg'

vgg_path = 'mix/imagenet-vgg-verydeep-19.mat'

def size(path):
    ratio_h = 1
    ratio_w = 1
    image_w, image_h = Image.open(path).size
    if image_w > 800: ratio_w = image_w/800
    image_h /= ratio_w
    image_w /= ratio_w
    if image_h > 600: ratio_h = image_h/600
    image_h /= ratio_h
    image_w /= ratio_h
    return int(image_w), int(image_h)

def mini(path):
    ratio_h = 1
    ratio_w = 1
    image_w, image_h = Image.open(path).size
    if image_w > 160: ratio_w = image_w/160
    image_h /= ratio_w
    image_w /= ratio_w
    if image_h > 120: ratio_h = image_h/120
    image_h /= ratio_h
    image_w /= ratio_h
    return int(image_w), int(image_h)

img = Image.open(content_image_path)
img = img.resize(size(content_image_path),PIL.Image.ANTIALIAS)
img.save(content_image_path.replace('jpg','png'))

img = Image.open(style_image_path)
img = img.resize(size(style_image_path),PIL.Image.ANTIALIAS)
img.save(style_image_path.replace('jpg','png'))

content_image_path = content_image_path.replace('jpg','png')
style_image_path = style_image_path.replace('jpg','png')

image_w, image_h = size(content_image_path)

channels = 3
num_iterations = int(open('mix/iter','r').read())
alpha = 10

beta = 40
NOISE_RATIO = 0.5

MEAN_VALUES = np.array([123.68, 116.779, 103.939]).reshape((1, 1, 1, 3))
STYLE_LAYERS = [('conv1_1', 0.2), ('conv2_1', 0.2), ('conv3_1', 0.2),
                ('conv4_1', 0.2), ('conv5_1', 0.2)]

print('DEFINE')
open('mix/loc','w').write('FUNCTIONS')
def load_vgg_model(path):
    model = sio.loadmat(path)
    model_layers = model['layers']
    def _weights_biases(layer, expected_layer_name):
        W = model_layers[0][layer][0][0][2][0][0]
        b = model_layers[0][layer][0][0][2][0][1]

        layer_name = model_layers[0][layer][0][0][0][0]

        return (W, b)
    def _conv2d_relu(prev_layer, layer, layer_name):
        (W, b) = _weights_biases(layer, layer_name)

        W = tf.constant(W)
        b = tf.constant(np.reshape(b, b.size))

        _conv2d = tf.nn.conv2d(prev_layer, filter=W, strides=[1, 1, 1,
                               1], padding='SAME') + b
        _relu = tf.nn.relu(_conv2d)

        return _relu
    def _avgpool(prev_layer):
        return tf.nn.avg_pool(prev_layer, ksize=[1, 2, 2, 1],
                              strides=[1, 2, 2, 1], padding='SAME')

    graph = {}
    graph['input'] = tf.Variable(np.zeros((1, image_h, image_w,
                                 channels)), dtype='float32')

    graph['conv1_1'] = _conv2d_relu(graph['input'], 0, 'conv1_1')
    graph['conv1_2'] = _conv2d_relu(graph['conv1_1'], 2, 'conv1_2')
    graph['avgpool1'] = _avgpool(graph['conv1_2'])

    graph['conv2_1'] = _conv2d_relu(graph['avgpool1'], 5, 'conv2_1')
    graph['conv2_2'] = _conv2d_relu(graph['conv2_1'], 7, 'conv2_2')
    graph['avgpool2'] = _avgpool(graph['conv2_2'])

    graph['conv3_1'] = _conv2d_relu(graph['avgpool2'], 10, 'conv3_1')
    graph['conv3_2'] = _conv2d_relu(graph['conv3_1'], 12, 'conv3_2')
    graph['conv3_3'] = _conv2d_relu(graph['conv3_2'], 14, 'conv3_3')
    graph['conv3_4'] = _conv2d_relu(graph['conv3_3'], 16, 'conv3_4')
    graph['avgpool3'] = _avgpool(graph['conv3_4'])

    graph['conv4_1'] = _conv2d_relu(graph['avgpool3'], 19, 'conv4_1')
    graph['conv4_2'] = _conv2d_relu(graph['conv4_1'], 21, 'conv4_2')
    graph['conv4_3'] = _conv2d_relu(graph['conv4_2'], 23, 'conv4_3')
    graph['conv4_4'] = _conv2d_relu(graph['conv4_3'], 25, 'conv4_4')
    graph['avgpool4'] = _avgpool(graph['conv4_4'])

    graph['conv5_1'] = _conv2d_relu(graph['avgpool4'], 28, 'conv5_1')
    graph['conv5_2'] = _conv2d_relu(graph['conv5_1'], 30, 'conv5_2')
    graph['conv5_3'] = _conv2d_relu(graph['conv5_2'], 32, 'conv5_3')
    graph['conv5_4'] = _conv2d_relu(graph['conv5_3'], 34, 'conv5_4')
    graph['avgpool5'] = _avgpool(graph['conv5_4'])

    return graph

def generate_noise_image(content_image, noise_ratio=NOISE_RATIO):
    noise_image = np.random.uniform(-20, 20, (1, image_h, image_w,
                                    channels)).astype('float32')
    input_image = noise_image * noise_ratio + content_image * (1
            - noise_ratio)

    return input_image


def load_image(path):
    image = cv2.imread(path)
    image = cv2.resize(image, (image_w, image_h))

    image = np.reshape(image, (1, ) + image.shape)
    image = image - MEAN_VALUES
    return image
def save_image(path, image):

    image = image + MEAN_VALUES
    image = image[0]

    image = np.clip(image, 0, 255).astype('uint8')
    cv2.imwrite(path, image)

def compute_content_cost(a_C, a_G):
    (m, n_H, n_W, n_C) = a_G.get_shape().as_list()

    a_C_unrolled = tf.transpose(tf.reshape(a_C, [n_H * n_W, n_C]))
    a_G_unrolled = tf.transpose(tf.reshape(a_G, [n_H * n_W, n_C]))

    J_content = tf.reduce_sum(tf.square(tf.subtract(a_C_unrolled,
                              a_G_unrolled))) / (4 * n_H * n_W * n_C)

    return J_content


def gram_matrix(A):
    GA = tf.matmul(A, tf.transpose(A))
    return GA

def compute_layer_style_cost(a_S, a_G):
    (m, n_H, n_W, n_C) = a_G.get_shape().as_list()

    a_S = tf.transpose(tf.reshape(a_S, [n_H * n_W, n_C]))
    a_G = tf.transpose(tf.reshape(a_G, [n_H * n_W, n_C]))

    GS = gram_matrix(a_S)
    GG = gram_matrix(a_G)

    J_style_layer = tf.reduce_sum(tf.square(tf.subtract(GS, GG))) / (4
            * n_C ** 2 * (n_W * n_H) ** 2)

    return J_style_layer


def compute_style_cost(model, STYLE_LAYERS):
    J_style = 0

    for (layer_name, coeff) in STYLE_LAYERS:
        out = model[layer_name]

        a_S = sess.run(out)
        a_G = out

        J_style_layer = compute_layer_style_cost(a_S, a_G)
        J_style += coeff * J_style_layer

    return J_style


def total_cost(
    J_content,
    J_style,
    alpha,
    beta,
    ):
    J = alpha * J_content + beta * J_style
    return J



def model_nn(sess, input_image, num_iterations):
    print('--------------------')
    try:
        sess.run(tf.global_variables_initializer())
        sess.run(model['input'].assign(input_image))

        for i in range(num_iterations):
            open('mix/loc','w').write(str(i))
            _ = sess.run(train_step)
            generated_image = sess.run(model['input'])

            (Jt, Jc, Js) = sess.run([J, J_content, J_style])
            print('Iteration ' + str(i)+'/'+str(num_iterations) + ' :')
            print('total cost = ' + str(Jt))
            print('content cost = ' + str(Jc))
            print('style cost = ' + str(Js))

            save_image('mix/now.png', generated_image)
            
        open('mix/loc','w').write('FINISHING')
        save_image('mix/now.png', generated_image)

        return generated_image
    except:
        print('oops')

print('SESSION')
open('mix/loc','w').write('SESSION')
sess = tf.InteractiveSession()

print('] GRABBING MODELS')
open('mix/loc','w').write('GRABBING MODELS')
model = load_vgg_model(vgg_path)
content_image = load_image(content_image_path)
style_image = load_image(style_image_path)

print('GENERATION')
open('mix/loc','w').write('STARTING...')
generated_image = generate_noise_image(content_image)
sess.run(model['input'].assign(content_image))
out = model['conv4_2']
a_C = sess.run(out)
a_G = out

J_content = compute_content_cost(a_C, a_G)

sess.run(model['input'].assign(style_image))
J_style = compute_style_cost(model, STYLE_LAYERS)

J = total_cost(J_content, J_style, alpha, beta)
optimizer = tf.train.AdamOptimizer(2.0)
train_step = optimizer.minimize(J)

model_nn(sess, generated_image, num_iterations)
open('mix/status','w').write('DONE')
open('mix/loc','w').write('DONE')
sess.close()
