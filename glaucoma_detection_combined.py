# -*- coding: utf-8 -*-
"""glaucoma_detection_combined.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1svysfq0RoMtB0bqEx44fDBfed13XstB4
"""

from google.colab import drive
drive.mount('/content/drive')

# from google.colab import drive
# drive.flush_and_unmount()

"""# Importing necessary libraries"""

import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
from tensorflow import keras
import seaborn as sns
import random
from keras.models import load_model
from keras.preprocessing import image
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import cv2
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sb
import tensorflow as tf

from sklearn.metrics import classification_report,confusion_matrix
import seaborn as sb

"""# 1.Data collection & exploration

The datasets used in the project were discovered and collected using the information from an open source eye disease database.Three datasets (Drishti Rim-One and Acrima datasets) had fundus photographies which present glaucoma.

"""

# current_dir = os.getcwd()
# print(current_dir)

"""#1.1  DRISTHI
>The dataset comprises of 101 retinal fundus images with 31 normal images and 70 glaucomatous images acquired using a retinal fundus camera. The ground truth for comparison of implemented approaches comprises of the ‘normal/abnormal’ labels and soft segmented maps of ‘disc/cup’ generated by the researchers of the IIIT Hyderabad in alliance with Aravind eye hospital in Madurai, India. It also includes a .txt file for each retinal image comprising of CDR values, which is a significant diagnostic parameter for glaucoma. Further, the images in the data repository are gathered from people of varying age groups visiting the hospital, with images acquired under varying brightness and contrast.
Link to dataset: (https://cvit.iiit.ac.in/projects/mip/drishti-gs/mip-dataset2/Home.php)
"""

train_glaucoma_dir = "/content/drive/MyDrive/PROJECT/Glaucoma Final/archive/Training-20211018T055246Z-001/Training/Images/GLAUCOMA"
train_normal_dir = "/content/drive/MyDrive/PROJECT/Glaucoma Final/archive/Training-20211018T055246Z-001/Training/Images/NORMAL"
test_glaucoma_dir = "/content/drive/MyDrive/PROJECT/Glaucoma Final/archive/Test-20211018T060000Z-001/Test/Images/glaucoma"
test_normal_dir = "/content/drive/MyDrive/PROJECT/Glaucoma Final/archive/Test-20211018T060000Z-001/Test/Images/normal"
dristhi_glaucoma_images = os.listdir(train_glaucoma_dir)+os.listdir(test_glaucoma_dir)
dristhi_normal_images = os.listdir(train_normal_dir)+os.listdir(test_normal_dir)

# Look at the number of samples in each dataset
print("Dristhi dataset contains :")
print(f"\t{len(dristhi_glaucoma_images)} images representing an eye with glaucoma")
print(f"\t{len(dristhi_normal_images)} images representing a normal eye")

print("Sample Dristhi glaucoma images:")
plt.subplots(figsize=(15, 10))
for i in range(1, 5):
    plt.subplot(1, 4, i)
    plt.imshow(load_img(f"{os.path.join(train_glaucoma_dir, dristhi_glaucoma_images[i - 1])}"))
plt.show()

print("\nSample Dristhi normal images:")
plt.subplots(figsize=(15, 10))
for i in range(1, 5):
    plt.subplot(1, 4, i)
    plt.imshow(load_img(f"{os.path.join(train_normal_dir, dristhi_normal_images[i - 1])}"))
plt.show()

"""# 1.2 Rim-One

>The RIM-ONE DL image dataset consists of 313 retinographies from normal subjects and 172 retinographies from patients with glaucoma. These images were captured in three Spanish hospitals: Hospital Universitario de Canarias (HUC), in Tenerife, Hospital Universitario Miguel Servet (HUMS), in Zaragoza, and Hospital Clínico Universitario San Carlos (HCSC), in Madrid.

>This dataset has been divided into training and test sets, with two variants:
* Partitioned randomly: the training and test sets are built randomly from all the images of the dataset.
* Partitioned by hospital: the images taken in the HUC are used for the training set, while the images taken in the HUMS and HCSC are used for testing.
"""

rimOne_dir = '/content/drive/MyDrive/PROJECT/Glaucoma Final/RIM-ONE_DL_images/RIM-ONE_DL_images/partitioned_randomly/'
train_glaucoma_dir = rimOne_dir + "training_set/glaucoma"
train_normal_dir = rimOne_dir + "training_set/normal"
test_glaucoma_dir = rimOne_dir + "test_set/glaucoma"
test_normal_dir = rimOne_dir + "test_set/normal"
rimOne_glaucoma_images = os.listdir(train_glaucoma_dir)+os.listdir(test_glaucoma_dir)
rimOne_normal_images = os.listdir(train_normal_dir)+os.listdir(test_normal_dir)

# Look at the number of samples in each dataset
print("Rim One dataset contains :")
print(f"\t{len(rimOne_glaucoma_images)} images representing an eye with glaucoma")
print(f"\t{len(rimOne_normal_images)} images representing a normal eye")

print("Sample Rim-One glaucoma images:")
plt.subplots(figsize=(15, 10))
for i in range(1, 5):
    plt.subplot(1, 4, i)
    plt.imshow(load_img(f"{os.path.join(train_glaucoma_dir, rimOne_glaucoma_images[i - 1])}"))
plt.show()

print("\nSample Rim-One normal images:")
plt.subplots(figsize=(15, 10))
for i in range(1, 5):
    plt.subplot(1, 4, i)
    plt.imshow(load_img(f"{os.path.join(train_normal_dir, rimOne_normal_images[i - 1])}"))
plt.show()

"""# 1.3. ACRIMA dataset
* Country: Spain
* No. of patients: unknown
* No. of images: 705
* Diseases present: Glaucoma and healthy eyes
* Instrument used: TRC retina camera (Topcon, Japan)
* Image format: JPEG

>ACRIMA database is composed by 705 fundus images (396 glaucomatous and 309 normal images). They were collected at the FISABIO Oftalmología Médica in Valencia, Spain, from glaucomatous and normal patients with their previous consent and in accordance with the ethical standards laid down in the 1964 Declaration of Helsinki. All images from ACRIMA database were annotated by glaucoma experts with several years of experience. They were cropped around the optic disc and renamed.



>The image name has the following structure: First, the name starts with the two letters "Im", followed by an image number composed by three digits (starting from 001 until 705), followed by the label (this label is "g" if the image is pathological and "_" if the image is normal). Finally, all image names have the database name, "ACRIMA", at the end of their names. For example, a name for a glaucomatous image is "Im686_g_ACRIMA" and "Im001_ACRIMA" for a normal image.
"""

# acrima_dir = "/content/drive/MyDrive/PROJECT/Glaucoma Final/Database/Images"
# acrima_main_dir = '/content/drive/MyDrive/PROJECT/Glaucoma Final/Database/Images'

# os.makedirs(acrima_main_dir + '/glaucoma')
# os.makedirs(acrima_main_dir + '/normal')

# for f in os.listdir(acrima_dir):
#   if 'g' in (f.split('.')[0]):
#     file_path = os.path.join(acrima_dir,f)
#     img = cv2.imread(file_path)
#     cv2.imwrite('/content/drive/MyDrive/Glaucoma Datasets/Database/Database/glaucoma/' + f, img)
#   else:
#     file_path = os.path.join(acrima_dir,f)
#     img = cv2.imread(file_path)
#     cv2.imwrite('/content/drive/MyDrive/Glaucoma Datasets/Database/Database/normal/' + f, img)



# acrima_dir = current_dir + "/drive/MyDrive/datasets/acrima/Database"
glaucoma_dir = "/content/drive/MyDrive/PROJECT/Glaucoma Final/Database/glaucoma"
normal_dir = "/content/drive/MyDrive/PROJECT/Glaucoma Final/Database/normal"

normal_images = os.listdir(normal_dir)
glaucoma_images = os.listdir(glaucoma_dir)

# Look at the number of samples in each dataset
print("Acrima dataset contains : ")
print(f"\t{len(glaucoma_images)} images representing an eye with glaucoma")
print(f"\t{len(normal_images)} images representing a normal eye")

print("Sample glaucoma images:")
plt.subplots(figsize=(15, 10))
for i in range(1, 5):
    plt.subplot(1, 4, i)
    plt.imshow(load_img(f"{os.path.join(glaucoma_dir, glaucoma_images[i - 1])}"))
plt.show()

print("\nSample normal images:")
plt.subplots(figsize=(15, 10))
for i in range(1, 5):
    plt.subplot(1, 4, i)
    plt.imshow(load_img(f"{os.path.join(normal_dir, normal_images[i - 1])}"))
plt.show()

"""**Combining datasets**"""

## define your paths for glaucoma####
# g_path1 = '/content/drive/MyDrive/Glaucoma Datasets/archive/Test-20211018T060000Z-001/Test/Images/glaucoma'
# g_path2 = '/content/drive/MyDrive/Glaucoma Datasets/Database/Database/glaucoma'
# g_path3 ='/content/drive/MyDrive/Glaucoma Datasets/RIM-ONE_DL_images/RIM-ONE_DL_images/partitioned_randomly/training_set/glaucoma'
# g_path4='/content/drive/MyDrive/Glaucoma Datasets/RIM-ONE_DL_images/RIM-ONE_DL_images/partitioned_randomly/test_set/glaucoma'
# g_path5='/content/drive/MyDrive/Glaucoma Datasets/archive/Training-20211018T055246Z-001/Training/Images/GLAUCOMA'
# g_dest='/content/drive/MyDrive/Glaucoma Datasets/combined/glaucoma'

# os.makedirs(g_dest)
# g_list=[g_path1,g_path2,g_path3,g_path4,g_path5]

# for i in g_list:
#   shutil.copytree(i, g_dest, dirs_exist_ok=True)

##################################################
#normal
# n_path1='/content/drive/MyDrive/Glaucoma Datasets/Database/Database/normal'
# n_path2='/content/drive/MyDrive/Glaucoma Datasets/RIM-ONE_DL_images/RIM-ONE_DL_images/partitioned_randomly/training_set/normal'
# n_path3='/content/drive/MyDrive/Glaucoma Datasets/RIM-ONE_DL_images/RIM-ONE_DL_images/partitioned_randomly/test_set/normal'
# n_path4='/content/drive/MyDrive/Glaucoma Datasets/archive/Training-20211018T055246Z-001/Training/Images/NORMAL'
# n_path5='/content/drive/MyDrive/Glaucoma Datasets/archive/Test-20211018T060000Z-001/Test/Images/normal'
# n_dest='/content/drive/MyDrive/Glaucoma Datasets/combined/normal'
# os.makedirs(n_dest)
# n_list=[n_path1,n_path2,n_path3,n_path4,n_path5]

# for i in n_list:
#   shutil.copytree(i,n_dest, dirs_exist_ok=True)
# print(len(os.listdir(n_dest)))

"""# Combined"""

pip install pathlib

import pathlib

base_dir = '/content/drive/MyDrive/PROJECT/Glaucoma Final/combined'
base_dir = pathlib.Path(base_dir)

glaucoma = [fn for fn in os.listdir(f'/content/drive/MyDrive/PROJECT/Glaucoma Final/combined/glaucoma/')]
normal = [fn for fn in os.listdir(f'/content/drive/MyDrive/PROJECT/Glaucoma Final/combined/normal')]
data=[glaucoma,normal]
dataset_classes =['glaucoma','normal']

image_count = len(list(base_dir.glob('*/*.jpg')))+len(list(base_dir.glob('*/*.png')))
print(f'Total images: {image_count}')
print(f'Total number of classes: {len(dataset_classes)}')
count = 0
data_count = []
for x in dataset_classes:
  print(f'Total {x} images: {len(data[count])}')
  data_count.append(len(data[count]))
  count += 1

sns.set_style('darkgrid')
sns.barplot(x=dataset_classes, y=data_count)
plt.show()

"""Spliiting Ratio of Dataset 80:10:10 (Train:Test:Validation)


"""

!pip install split-folders
import splitfolders #to split dataset
import pathlib
base_ds = '/content/drive/MyDrive/PROJECT/Glaucoma Final/combined'
base_ds = pathlib.Path(base_ds)
img_height=256
img_width=256
batch_size=32
splitfolders.ratio(base_ds, output='images', seed=1321, ratio=(.8,.1,.1), group_prefix=None)

"""**Data augmentation done using Image Data Generator**

 The Keras ImageDataGenerator class is designed to provide real-time data augmentation. Meaning it is generating augmented images on the fly while your model is still in the training stage. That means it creates a pipeline, but does not create augmented images directly.

ImageDataGenerator class ensures that the model receives new variations of the images at each epoch. But it only returns the transformed images and does not add it to the original corpus of images. If it was, in fact, the case, then the model would be seeing the original images multiple times which would definitely overfit our model.

Link : https://www.analyticsvidhya.com/blog/2020/08/image-augmentation-on-the-fly-using-keras-imagedatagenerator/
"""

from keras.preprocessing.image import ImageDataGenerator
datagen = ImageDataGenerator(rescale=1./255,
shear_range = 0.15,
zoom_range = 0.15,
horizontal_flip = True)
train_ds = datagen.flow_from_directory(
    'images/train',
    target_size = (img_height, img_width),
    batch_size = batch_size,
    class_mode='categorical',
    shuffle=False)

val_ds = datagen.flow_from_directory(
    'images/val',
    target_size = (img_height, img_width),
    batch_size = batch_size,
    class_mode='categorical',
    shuffle=False)

test_ds = datagen.flow_from_directory(
    'images/test',
    target_size = (img_height, img_width),
    batch_size = batch_size,
    class_mode='categorical',
    shuffle=False)

# len(train_ds.classes)

"""### Important functions"""

def plot_train_history(history):
    plt.figure(figsize=(15,5))
    plt.subplot(1,2,1)
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')

    plt.subplot(1,2,2)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()

# plot_train_history(model_info)

def glaucoma_prediction(test_image):
  image = img_to_array(test_image)
  image = np.expand_dims(image, axis = 0)
  result = np.argmax(model.predict(image))
  return result

"""## CNN MODEL"""

from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense,Dropout
from keras.layers import BatchNormalization

# Initialising the CNN
classifier = Sequential()
# Step 1 - Adding Convolution layer
classifier.add(Conv2D(32, (3, 3), input_shape = (256,256, 3), activation = 'relu'))

# Step 2 - Adding MaxPooling layers
classifier.add(MaxPooling2D(pool_size = (2, 2)))
# Adding a second convolutional layer
classifier.add(Conv2D(32, (3, 3), activation = 'relu'))
classifier.add(MaxPooling2D(pool_size = (2, 2)))

# Step 3 - Flattening
classifier.add(Flatten())

# Step 4 - Full connection
classifier.add(Dense(units = 512, activation = 'relu'))
classifier.add(BatchNormalization()),
classifier.add(Dense(256,activation='relu')),
classifier.add(Dropout(0.25)),
classifier.add(Dense(units = 2, activation = 'softmax'))

# Compiling the CNN
classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])

classifier.summary()

model_info=classifier.fit(train_ds,
steps_per_epoch = int(round(1032/32)),
epochs = 150,
validation_data = val_ds,
validation_steps = int(round(128/32)))



plot_train_history(model_info)

classifier.save('/content/drive/MyDrive/Glaucoma Datasets/combined/combine_cnn.h5')

"""Loading Model"""

model=load_model('/content/drive/MyDrive/Glaucoma Datasets/combined/combine_cnn.h5')
print("Glaucoma detection model loaded")

# test_image = load_img('/content/drive/MyDrive/datasets/acrima/Database/glaucoma/Im310_g_ACRIMA.jpg', target_size = (256,256))
# prediction = glaucoma_prediction(test_image)
# if prediction == 0:
#  print("Glaucoma")
# else:
#  print("Not Glaucoma")

# test_image = load_img('/content/drive/MyDrive//datasets/acrima/Database/normal/Im001_ACRIMA.jpg', target_size = (256,256))
# prediction = glaucoma_prediction(test_image)
# if prediction == 0:
#  print("Glaucoma")
# else:
#  print("Not Glaucoma")

score=model.evaluate(test_ds)
print("Loss:",score[0],"Accuracy:",score[1])

"""Testing set confusion matrix"""

from sklearn.metrics import classification_report,confusion_matrix
import seaborn as sb

pred= np.round(model.predict(test_ds, verbose=1))
test_labels=test_ds.labels
test_pred_labels=[]
for i in range(len(pred)):
  test_pred_labels.append(np.argmax(pred[i]))
conf_matrix= confusion_matrix(test_pred_labels,test_labels)
print (conf_matrix)

sb.heatmap(conf_matrix,cmap='Purples', annot=True,xticklabels=['glaucoma','normal'],yticklabels=['glaucoma','normal'],linewidths=1,
                linecolor='green').plot()
plt.show()

test_report = classification_report(test_ds.labels,test_pred_labels, target_names=['glaucoma','normal'], output_dict=True)
test_df = pd.DataFrame(test_report).transpose()
test_df

"""## CNN 2nd"""

checkpoint = tf.keras.callbacks.ModelCheckpoint('best_weights.h5', save_best_only=True, save_weights_only=True, monitor='val_loss', mode='min', verbose=1)

from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense,Dropout
from keras.layers import BatchNormalization
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
keras.backend.clear_session()

# Initialize the CNN
classifier = Sequential()

# Step 1 - Add Convolution layer
classifier.add(Conv2D(64, (3, 3), input_shape=(256, 256, 3), activation='relu'))

# Step 2 - Add MaxPooling layers
classifier.add(MaxPooling2D(pool_size=(2, 2)))

# Adding a second convolutional layer
classifier.add(Conv2D(64, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))

# Adding a third convolutional layer for more complexity
classifier.add(Conv2D(128, (3, 3), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))

# Step 3 - Flatten
classifier.add(Flatten())

# Step 4 - Full connection
classifier.add(Dense(units=512, activation='relu'))
classifier.add(BatchNormalization())
classifier.add(Dropout(0.5))  # Increased dropout rate for regularization
classifier.add(Dense(units=256, activation='relu'))
classifier.add(Dropout(0.25))

# Output layer with 2 units for binary classification
classifier.add(Dense(units=2, activation='softmax'))

# Compile the CNN
classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

classifier.summary()

model_info=classifier.fit(train_ds,
steps_per_epoch = int(round(1032/32)),
epochs = 130,
validation_data = val_ds,
validation_steps = int(round(128/32)),
                          callbacks = [checkpoint]
)

plot_train_history(model_info)

score=classifier.evaluate(test_ds)
print("Loss:",score[0],"Accuracy:",score[1])



pred= np.round(classifier.predict(test_ds, verbose=1))
test_labels=test_ds.labels
test_pred_labels=[]
for i in range(len(pred)):
  test_pred_labels.append(np.argmax(pred[i]))
conf_matrix= confusion_matrix(test_pred_labels,test_labels)
print (conf_matrix)

sb.heatmap(conf_matrix,cmap='Purples', annot=True,xticklabels=['glaucoma','normal'],yticklabels=['glaucoma','normal'],linewidths=1,
                linecolor='green').plot()
plt.show()

test_report = classification_report(test_ds.labels,test_pred_labels, target_names=['glaucoma','normal'])
print(test_report)

"""## Resnet50"""

checkpoint = tf.keras.callbacks.ModelCheckpoint('best_weights_resnet50.h5', save_best_only=True, save_weights_only=True, monitor='val_accuracy', mode='max', verbose=1)

from keras.models import Model
from keras.layers import Input, Conv2D, MaxPooling2D, GlobalAveragePooling2D, Dense, BatchNormalization, Activation, Add
from keras.applications import ResNet50

keras.backend.clear_session()
# Load pre-trained ResNet-50 model
base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(256, 256, 3))

# Add custom top layers
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)
x = BatchNormalization()(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.25)(x)
predictions = Dense(2, activation='softmax')(x)

# Create the final model
resnet50_model = Model(inputs=base_model.input, outputs=predictions)

# Set the first layers to non-trainable (optional)

# Compile the model
resnet50_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Summary of the model
resnet50_model.summary()

resnet50_model_info=resnet50_model.fit(train_ds,
steps_per_epoch = int(round(1032/32)),
epochs = 50,
validation_data = val_ds,
validation_steps = int(round(128/32)),
                                       callbacks = [checkpoint])



plot_train_history(resnet50_model_info)

score=resnet50_model.evaluate(test_ds)
print("Loss:",score[0],"Accuracy:",score[1])

pred= np.round(resnet50_model.predict(test_ds, verbose=1))
test_labels=test_ds.labels
test_pred_labels=[]
for i in range(len(pred)):
  test_pred_labels.append(np.argmax(pred[i]))
conf_matrix= confusion_matrix(test_pred_labels,test_labels)
print (conf_matrix)

test_report = classification_report(test_ds.labels,test_pred_labels, target_names=['glaucoma','normal'])
print(test_report)

sb.heatmap(conf_matrix,cmap='Purples', annot=True,xticklabels=['glaucoma','normal'],yticklabels=['glaucoma','normal'],linewidths=1,
                linecolor='green').plot()
plt.show()

"""## mobilenetv2"""

checkpoint = tf.keras.callbacks.ModelCheckpoint('best_weights_resnet50.h5', save_best_only=True, save_weights_only=True, monitor='val_accuracy', mode='max', verbose=1)

from keras.applications import MobileNetV2
from keras.models import Sequential
from keras.layers import GlobalAveragePooling2D, Dense, Dropout, BatchNormalization
keras.backend.clear_session()
# Load pre-trained MobileNetV2 model
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(256, 256, 3))

# Add custom top layers
model = Sequential()
model.add(base_model)
model.add(GlobalAveragePooling2D())
model.add(Dense(512, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.25))
model.add(Dense(2, activation='softmax'))

# Set the first layers to non-trainable (optional)
for layer in model.layers[0].layers:
    layer.trainable = False

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Summary of the model
model.summary()

mobilenet_v2_model_info=model.fit(train_ds,
steps_per_epoch = int(round(1032/32)),
epochs = 50,
validation_data = val_ds,
validation_steps = int(round(128/32)),
                                  callbacks = [checkpoint])

score=model.evaluate(test_ds)
print("Loss:",score[0],"Accuracy:",score[1])

plot_train_history(mobilenet_v2_model_info)

pred= np.round(model.predict(test_ds, verbose=1))
test_labels=test_ds.labels
test_pred_labels=[]
for i in range(len(pred)):
  test_pred_labels.append(np.argmax(pred[i]))
conf_matrix= confusion_matrix(test_pred_labels,test_labels)
print (conf_matrix)

sb.heatmap(conf_matrix,cmap='Purples', annot=True,xticklabels=['glaucoma','normal'],yticklabels=['glaucoma','normal'],linewidths=1,
                linecolor='green').plot()
plt.show()

test_report = classification_report(test_ds.labels,test_pred_labels, target_names=['glaucoma','normal'])
print(test_report)

"""## VGG16"""

from keras.applications import VGG16
from keras.models import Sequential
from keras.layers import GlobalAveragePooling2D, Dense, Dropout, BatchNormalization
from keras.callbacks import ModelCheckpoint

keras.backend.clear_session()

# Load pre-trained VGG16 model
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(256, 256, 3))

# Add custom top layers
model = Sequential()
model.add(base_model)
model.add(GlobalAveragePooling2D())
model.add(Dense(512, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.25))
model.add(Dense(2, activation='softmax'))

# Set the first layers to non-trainable (optional)
for layer in model.layers[0].layers:
    layer.trainable = False

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Define a ModelCheckpoint callback
checkpoint = ModelCheckpoint('best_weights.h5', save_best_only=True, save_weights_only=True, monitor='val_loss', mode='min', verbose=1)

# mobilenet_v2_model_info=model.fit(train_ds,
# steps_per_epoch = int(round(1032/32)),
# epochs = 50,
# validation_data = val_ds,
# validation_steps = int(round(128/32)))

vgg16_model_info = model.fit(train_ds, epochs=50,steps_per_epoch = int(round(1032/32)),
 validation_data=val_ds,validation_steps = int(round(128/32)), callbacks=[checkpoint])

# Load the best weights
model.load_weights('best_weights.h5')

# Summary of the model
model.summary()

plot_train_history(vgg16_model_info)

pred= np.round(model.predict(test_ds, verbose=1))
test_labels=test_ds.labels
test_pred_labels=[]
for i in range(len(pred)):
  test_pred_labels.append(np.argmax(pred[i]))
conf_matrix= confusion_matrix(test_pred_labels,test_labels)
print (conf_matrix)

sb.heatmap(conf_matrix,cmap='Purples', annot=True,xticklabels=['glaucoma','normal'],yticklabels=['glaucoma','normal'],linewidths=1,
                linecolor='green').plot()
plt.show()



score=model.evaluate(test_ds)
print("Loss:",score[0],"Accuracy:",score[1])

test_report = classification_report(test_ds.labels,test_pred_labels, target_names=['glaucoma','normal'])
print(test_report)

"""## InceptionV3"""

from keras.applications import InceptionV3
from keras.models import Sequential
from keras.layers import GlobalAveragePooling2D, Dense, Dropout, BatchNormalization
from keras.callbacks import ModelCheckpoint

keras.backend.clear_session()

# Load pre-trained InceptionV3 model
base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(256, 256, 3))

# Add custom top layers
model = Sequential()
model.add(base_model)
model.add(GlobalAveragePooling2D())
model.add(Dense(512, activation='relu'))
model.add(BatchNormalization())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.25))
model.add(Dense(2, activation='softmax'))

# Set the first layers to non-trainable (optional)
for layer in model.layers[0].layers:
    layer.trainable = False

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Define a ModelCheckpoint callback
checkpoint = ModelCheckpoint('best_weights.h5', save_best_only=True, save_weights_only=True, monitor='val_loss', mode='min', verbose=1)

# Train the model with the callback

inception = model.fit(train_ds, epochs=50,steps_per_epoch = int(round(1032/32)),
 validation_data=val_ds,validation_steps = int(round(128/32)), callbacks=[checkpoint])

# Load the best weights
model.load_weights('best_weights.h5')

# Summary of the model
model.summary()

plot_train_history(inception)

# score=model.evaluate(test_ds)
# print("Loss:",score[0],"Accuracy:",score[1])

pred= np.round(model.predict(test_ds, verbose=1))
test_labels=test_ds.labels
test_pred_labels=[]
for i in range(len(pred)):
  test_pred_labels.append(np.argmax(pred[i]))
conf_matrix= confusion_matrix(test_pred_labels,test_labels)
print (conf_matrix)

sb.heatmap(conf_matrix,cmap='Purples', annot=True,xticklabels=['glaucoma','normal'],yticklabels=['glaucoma','normal'],linewidths=1,
                linecolor='green').plot()
plt.show()

test_report = classification_report(test_ds.labels,test_pred_labels, target_names=['glaucoma','normal'], output_dict=True)
test_df = pd.DataFrame(test_report).transpose()
test_df

