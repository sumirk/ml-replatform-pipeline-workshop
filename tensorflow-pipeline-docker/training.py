import os
import shutil
from utils import upload_to_s3
import tensorflow as tf
# from preprocessing import preprocess_data
import boto3
from botocore.exceptions import NoCredentialsError

# bucket_name = os.environ.get('BUCKET_NAME')
bucket_name = 'techsummit2023mlops'

local_folder = '/app/data'

def create_cnn_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    return model
        
def train_model(model, X_train, y_train, X_val, y_val, output_dir):
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    best_val_loss = float('inf')
    best_checkpoint_path = os.path.join(output_dir, 'best_checkpoint.h5')

    for epoch in range(10):
        history = model.fit(X_train, y_train, epochs=1, batch_size=64, validation_data=(X_val, y_val))

        # Print training metrics
        train_loss = history.history['loss'][0]
        train_accuracy = history.history['accuracy'][0]
        val_loss = history.history['val_loss'][0]
        val_accuracy = history.history['val_accuracy'][0]

        print(f"Epoch {epoch + 1}/{10} - "
              f"Train Loss: {train_loss:.4f} - Train Accuracy: {train_accuracy:.4f} - "
              f"Val Loss: {val_loss:.4f} - Val Accuracy: {val_accuracy:.4f}")

        # Save checkpoint periodically
        if epoch % 2 == 0:
            checkpoint_path = os.path.join(output_dir, f'checkpoint_epoch_{epoch}.h5')
            model.save_weights(checkpoint_path)
            print(checkpoint_path,bucket_name, f'checkpoints/checkpoint_epoch_{epoch}.h5' )
            # Upload checkpoint to S3
            s3 = boto3.client('s3')
            s3.upload_file(checkpoint_path, bucket_name, f'checkpoints/checkpoint_epoch_{epoch}.h5')
            # upload_to_s3(checkpoint_path,bucket_name,f'checkpoints/checkpoint_epoch_{epoch}.h5')
            # upload_to_s3(checkpoint_path, bucket_name, f'checkpoints/checkpoint_epoch_{epoch}.h5')

            # Update best checkpoint if necessary
            if val_loss < best_val_loss:
                best_val_loss = val_loss
                shutil.copyfile(checkpoint_path, best_checkpoint_path)

            # Delete local checkpoint after uploading
            os.remove(checkpoint_path)
            
    # Upload best checkpoint to S3
    # upload_to_s3(best_checkpoint_path, bucket_name, 'best_checkpoint.h5')
    s3 = boto3.client('s3')
    s3.upload_file(best_checkpoint_path, bucket_name, 'best_checkpoint.h5')
