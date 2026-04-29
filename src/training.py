import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# =========================
# PATH DATASET (3 CLASS)
# =========================
train_dir = "3class/train"
val_dir   = "3class/valid"
test_dir  = "3class/test"

img_size = (224,224)
batch_size = 32
epochs = 30

# =========================
# DATA AUGMENTATION (AMAN)
# =========================
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=5,
    zoom_range=0.05,
    width_shift_range=0.02,
    height_shift_range=0.02,
    brightness_range=[0.95,1.05]
)

val_test_datagen = ImageDataGenerator(rescale=1./255)

# =========================
# GENERATOR
# =========================
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=True
)

val_generator = val_test_datagen.flow_from_directory(
    val_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=False
)

test_generator = val_test_datagen.flow_from_directory(
    test_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical',
    shuffle=False
)

# =========================
# INFO CLASS
# =========================
class_labels = list(train_generator.class_indices.keys())
num_classes = len(class_labels)

print("Class labels:", class_labels)
print("Num classes:", num_classes)

# =========================
# CLASS WEIGHT (LEBIH STABIL)
# =========================
y_train_labels = train_generator.classes
unique_classes = np.unique(y_train_labels)

class_weights = compute_class_weight(
    class_weight='balanced',
    classes=unique_classes,
    y=y_train_labels
)

class_weights = dict(zip(unique_classes, class_weights))

# 🔥 BOOST RINGAN SAJA (JANGAN OVER)
if "netral" in class_labels:
    idx = class_labels.index("netral")
    class_weights[idx] *= 1.5

print("Class weights:", class_weights)

# =========================
# LOAD MODEL
# =========================
base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224,224,3)
)

base_model.trainable = False

# =========================
# HEAD
# =========================
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)
outputs = Dense(num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=outputs)

# =========================
# LOSS
# =========================
loss_fn = tf.keras.losses.CategoricalCrossentropy(label_smoothing=0.03)

model.compile(
    optimizer=Adam(learning_rate=1e-4),
    loss=loss_fn,
    metrics=['accuracy']
)

# =========================
# CALLBACK
# =========================
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.3,
    patience=3,
    min_lr=1e-6
)

# =========================
# TRAINING STAGE 1
# =========================
history = model.fit(
    train_generator,
    epochs=epochs,
    validation_data=val_generator,
    class_weight=class_weights,
    callbacks=[early_stop, reduce_lr]
)

# =========================
# FINE TUNING
# =========================
base_model.trainable = True

for layer in base_model.layers[:-40]:
    layer.trainable = False

model.compile(
    optimizer=Adam(learning_rate=1e-5),
    loss=loss_fn,
    metrics=['accuracy']
)

history_finetune = model.fit(
    train_generator,
    epochs=10,
    validation_data=val_generator,
    class_weight=class_weights,
    callbacks=[early_stop, reduce_lr]
)

# =========================
# TESTING
# =========================
test_loss, test_acc = model.evaluate(test_generator)
print(f"\nTest Accuracy: {test_acc*100:.2f}%")

# =========================
# PREDICTION
# =========================
y_pred_probs = model.predict(test_generator)
y_pred = np.argmax(y_pred_probs, axis=1)
y_true = test_generator.classes

# =========================
# REPORT
# =========================
print("\nClassification Report:\n")
print(classification_report(y_true, y_pred, target_names=class_labels, digits=4))

# =========================
# CONFUSION MATRIX
# =========================
cm = confusion_matrix(y_true, y_pred)

plt.figure(figsize=(8,6))
sns.heatmap(cm, annot=True, fmt='d',
            xticklabels=class_labels,
            yticklabels=class_labels)

plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix")
plt.show()

# =========================
# SAVE MODEL
# =========================
model.save("mobilenetv2_3class_final.h5")
print("Model saved!")
