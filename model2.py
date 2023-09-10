# %% [markdown]
# # Чат-бот, использующий модели Seq2Seq LSTM
# В этом блокноте модель seq2seq LSTM, используя функциональный API Keras, чтобы создать работающего чат-бота, который отвечал бы на задаваемые ему вопросы.

# %% [markdown]
# ## 1) Импорт библотек
# 
# Мы импортируем [TensorFlow](https://www.tensorflow.org ) и наш любимый [Keras](https://www.tensorflow.org/guide/keras ). Кроме того, мы импортируем другие модули, которые помогают в определении слоев модели.
# 
# 
# 
# 
# 

# %%

import numpy as np
import tensorflow as tf
import pickle
from tensorflow.keras import layers , activations , models , preprocessing


# %% [markdown]
# ## 2) Предварительная обработка данных

# %% [markdown]
# ### A) Создание датасета
# 
# Из приведённого файла, создаём папку data с .yml фаёлами, названий категорий со следующей структурой.
# 
# Название категории:
# - Вариант названия 1
# - Вариант названия 2
# 
# Разговоры:
# - Вопрос 1?
# - - Ответ
# - Вопрос 2?
# - - Ответ
# - Вопрос 3?
# - - Ответ

# %%

# %% [markdown]
# ### B) Считывание данных из файлов
# 
# Мы анализируем каждый из файлов `.yaml`.
# 
# * Соедините два или более предложений, если в ответе их два или более.
# * Удалите ненужные типы данных, которые образуются при синтаксическом анализе данных.
# * Добавьте `<START>` и `<END>` ко всем 'ответам'.
# * Создали `Токенизатор` и загрузили в него весь словарный запас (`вопросы` + `ответы`).

# %%

from tensorflow.keras import preprocessing , utils
import os
import yaml

dir_path = 'data_example'
files_list = os.listdir(dir_path + os.sep)

questions = list()
answers = list()

for filepath in files_list:
    stream = open( dir_path + os.sep + filepath , 'rb')
    docs = yaml.safe_load(stream)
    conversations = docs['conversations']
    for con in conversations:
        if len( con ) > 2 :
            questions.append(con[0])
            replies = con[ 1 : ]
            ans = ''
            for rep in replies:
                ans += ' ' + rep
            answers.append( ans )
        elif len( con )> 1:
            questions.append(con[0])
            answers.append(con[1])

answers_with_tags = list()
for i in range( len( answers ) ):
    if type( answers[i] ) == str:
        answers_with_tags.append( answers[i] )
    else:
        questions.pop( i )

answers = list()
for i in range( len( answers_with_tags ) ) :
    answers.append( '<START> ' + answers_with_tags[i] + ' <END>' )

tokenizer = preprocessing.text.Tokenizer()
tokenizer.fit_on_texts( questions + answers )
VOCAB_SIZE = len( tokenizer.word_index )+1
print( 'VOCAB SIZE : {}'.format( VOCAB_SIZE ))


# %% [markdown]
# 
# ### C) Подготовка данных для модели Seq2Seq
# 
# Для нашей модели требуются три массива, а именно `encoder_input_data`, `decoder_input_data` и `decoder_output_data`.
# 
# Для `encoder_input_data` :
# * Обозначьте токеном `questions`. Набеитие их до максимальной длины.
# 
# Для `decoder_input_data` :
# * Обозначьте токеном `answers`. Набитие их до максимальной длины.
# 
# Для `decoder_output_data` :
# 
# * Обозначьте токеном `answers`. Удаляем первый элемент из всех `tokenized_answers`. Это `<START>` элемент, который мы добавили ранее.
# 
# 

# %%

from gensim.models import Word2Vec
import re

vocab = []
for word in tokenizer.word_index:
    vocab.append( word )

def tokenize( sentences ):
    tokens_list = []
    vocabulary = []
    for sentence in sentences:
        sentence = sentence.lower()
        sentence = re.sub( '[^a-zA-Z]', ' ', sentence )
        tokens = sentence.split()
        vocabulary += tokens
        tokens_list.append( tokens )
    return tokens_list , vocabulary

#p = tokenize( questions + answers )
#model = Word2Vec( p[ 0 ] )

#embedding_matrix = np.zeros( ( VOCAB_SIZE , 100 ) )
#for i in range( len( tokenizer.word_index ) ):
    #embedding_matrix[ i ] = model[ vocab[i] ]

# encoder_input_data
tokenized_questions = tokenizer.texts_to_sequences( questions )
maxlen_questions = max( [ len(x) for x in tokenized_questions ] )
padded_questions = preprocessing.sequence.pad_sequences( tokenized_questions , maxlen=maxlen_questions , padding='post' )
encoder_input_data = np.array( padded_questions )
print( encoder_input_data.shape , maxlen_questions )

# decoder_input_data
tokenized_answers = tokenizer.texts_to_sequences( answers )
maxlen_answers = max( [ len(x) for x in tokenized_answers ] )
padded_answers = preprocessing.sequence.pad_sequences( tokenized_answers , maxlen=maxlen_answers , padding='post' )
decoder_input_data = np.array( padded_answers )
print( decoder_input_data.shape , maxlen_answers )

# decoder_output_data
tokenized_answers = tokenizer.texts_to_sequences( answers )
for i in range(len(tokenized_answers)) :
    tokenized_answers[i] = tokenized_answers[i][1:]
padded_answers = preprocessing.sequence.pad_sequences( tokenized_answers , maxlen=maxlen_answers , padding='post' )
onehot_answers = utils.to_categorical( padded_answers , VOCAB_SIZE )
decoder_output_data = np.array( onehot_answers )
print( decoder_output_data.shape )

encoder_inputs = tf.keras.layers.Input(shape=( maxlen_questions , ))
encoder_embedding = tf.keras.layers.Embedding( VOCAB_SIZE, 200 , mask_zero=True ) (encoder_inputs)
encoder_outputs , state_h , state_c = tf.keras.layers.LSTM( 200 , return_state=True )( encoder_embedding )
encoder_states = [ state_h , state_c ]

decoder_inputs = tf.keras.layers.Input(shape=( maxlen_answers ,  ))
decoder_embedding = tf.keras.layers.Embedding( VOCAB_SIZE, 200 , mask_zero=True) (decoder_inputs)
decoder_lstm = tf.keras.layers.LSTM( 200 , return_state=True , return_sequences=True )
decoder_outputs , _ , _ = decoder_lstm ( decoder_embedding , initial_state=encoder_states )
decoder_dense = tf.keras.layers.Dense( VOCAB_SIZE , activation=tf.keras.activations.softmax )
output = decoder_dense ( decoder_outputs )

model = tf.keras.models.Model([encoder_inputs, decoder_inputs], output )
model.compile(optimizer=tf.keras.optimizers.RMSprop(), loss='categorical_crossentropy')

model.summary()


# %% [markdown]
# ## 4) Обучение модели
# Мы обучаем модель для нескольких эпох с помощью оптимизатора `RMSProp` и функции потерь `categorical_crossentropy`.

# %%
model = tf.keras.models.load_model("model (1).h5")


# %% [markdown]
# ## 5) Определение моделей логического вывода
# Мы создали модели логического вывода, которые помогают предсказывать ответы.
# 
# **Модель вывода кодера** : Принимает вопрос в качестве входных данных и выводит состояния LSTM ( `h` и `c`).
# 
# **Модель вывода декодера** : Принимает 2 входных сигнала, один из которых - состояния LSTM ( выходные данные модели кодера ), второй - последовательности ввода ответа ( те, которые не имеют тега `<start>`). Он выведет ответы на вопрос, который мы ввели в модель кодера, и значения ее состояния.

# %%

def make_inference_models():

    encoder_model = tf.keras.models.Model(encoder_inputs, encoder_states)

    decoder_state_input_h = tf.keras.layers.Input(shape=( 200 ,))
    decoder_state_input_c = tf.keras.layers.Input(shape=( 200 ,))

    decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]

    decoder_outputs, state_h, state_c = decoder_lstm(
        decoder_embedding , initial_state=decoder_states_inputs)
    decoder_states = [state_h, state_c]
    decoder_outputs = decoder_dense(decoder_outputs)
    decoder_model = tf.keras.models.Model(
        [decoder_inputs] + decoder_states_inputs,
        [decoder_outputs] + decoder_states)

    return encoder_model , decoder_model


# %% [markdown]
# ## 6) Общение с нашим чат-ботом
# 
# Сначала мы определяем метод `str_to_tokens`, который преобразует вопросы `str` в целочисленные токены с заполнением.

# %%

def str_to_tokens( sentence : str ):
    words = sentence.lower().split()
    tokens_list = list()
    for word in words:
        tokens_list.append( tokenizer.word_index[ word ] )
    return preprocessing.sequence.pad_sequences( [tokens_list] , maxlen=maxlen_questions , padding='post')


# %% [markdown]
# 1. Сначала мы берем вопрос в качестве входных данных и прогнозируем значения состояния, используя `enc_model`.
# 2. Мы устанавливаем значения состояния в LSTM декодера.
# 3. Затем мы генерируем последовательность, которая содержит элемент `<start>`.
# 4. Мы вводим эту последовательность в `dec_model`.
# 5. Мы заменяем элемент `<start>` элементом, который был предсказан `dec_model`, и обновляем значения состояния.
# 6. Мы повторяем описанные выше шаги итеративно, пока не дойдем до тега `<end>` или максимальной длины ответа.

# %%

enc_model , dec_model = make_inference_models()

def ask(question):
    for _ in range(10):
        states_values = enc_model.predict( str_to_tokens( question ) )
        empty_target_seq = np.zeros( ( 1 , 1 ) )
        empty_target_seq[0, 0] = tokenizer.word_index['start']
        stop_condition = False
        decoded_translation = ''
        while not stop_condition :
            dec_outputs , h , c = dec_model.predict([ empty_target_seq ] + states_values )
            sampled_word_index = np.argmax( dec_outputs[0, -1, :] )
            sampled_word = None
            for word , index in tokenizer.word_index.items() :
                if sampled_word_index == index :
                    decoded_translation += ' {}'.format( word )
                    sampled_word = word

            if sampled_word == 'end' or len(decoded_translation.split()) > maxlen_answers:
                stop_condition = True

            empty_target_seq = np.zeros( ( 1 , 1 ) )
            empty_target_seq[ 0 , 0 ] = sampled_word_index
            states_values = [ h , c ]

    return(decoded_translation)