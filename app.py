# -*- coding: utf-8 -*-
from flask import Flask, request, render_template
from runner import LyricGenRunner
from LSTMModel import LSTMModel
from data_reader import DataReader
import tensorflow as tf
import constants as c

app = Flask(__name__)

sess = tf.Session()
artist_name = 'all_lyrics'
data_reader = DataReader(artist_name)
vocab = data_reader.get_vocab()
model = LSTMModel(sess, vocab, c.BATCH_SIZE, c.SEQ_LEN, c.CELL_SIZE, c.NUM_LAYERS, test=True)

saver = tf.train.Saver(max_to_keep=None)
sess.run(tf.global_variables_initializer())

load_path = '/home/ubuntu/eight/encore.ai/save/models/test/all_lyrics.ckpt-25000'
saver.restore(sess, load_path)

@app.route('/')
def eight():
    with open('/home/ubuntu/eight/templates/valentine2.htm', 'r', encoding='cp1252') as f:
        return f.read()
    #return render_template('valentine2.htm')
    #return render_template('predict.html')

@app.route('/', methods=['POST'])
def eight_post():
    with open('/home/ubuntu/eight/templates/valentine2.htm', 'r', encoding='cp1252') as f:
        result = f.read()       
        first, second = result.split('See your result!')
        p = predict(request.form['text'])
        return first + p + '<br><br>' + second

@app.route('/predict/<seed>')
def predict(seed):
    words = ' '.join(seed.split('_'))
    return predict(words)


def predict(seed):
    return model.generate(prime=seed, num_out=40)


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=80)
