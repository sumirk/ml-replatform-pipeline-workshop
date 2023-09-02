import os
import json
import shutil
import tensorflow as tf
from training import create_cnn_model, train_model
from preprocessing import preprocess_data
from utils import upload_to_s3, download_data_from_s3

# bucket_name = os.environ.get('BUCKET_NAME') 
bucket_name = 'techsummit2023mlops'
# local_folder = './app/data'
# output_dir = './checkpoints'
local_folder = '/app/data'
output_dir = '/app/checkpoints'
remote_folder = "raw_data"

def evaluate_model(model, X_test, y_test):
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test accuracy: {accuracy:.4f}")

    evaluation_metrics = {
        "test_accuracy": accuracy,
        "test_loss": loss
    }

    # Save evaluation metrics as JSON
    metrics_file_path = "evaluation_metrics.json"
    with open(metrics_file_path, "w") as metrics_file:
        json.dump(evaluation_metrics, metrics_file)

    # Upload evaluation metrics JSON to S3
    upload_to_s3(metrics_file_path, "evaluation_metrics.json", bucket_name)

def main():
    # local_folder = "data"  # Local folder to save downloaded data
    # bucket_name = "your-s3-bucket-name"
    print("Data DpownloadStarted")
    download_data_from_s3(bucket_name, remote_folder, local_folder)
    print("Data Dpownload Complete")
    
    print("Data Preprocessing Started")

    X_train, X_val, y_train, y_val, X_test, y_test = preprocess_data(local_folder)
    #Just to show the data type
    # print("type of data type for X_train, X_val, y_train, y_val, X_test, y_test" )
    # for i in [X_train, X_val, y_train, y_val, X_test, y_test]:
    #     print(type(i))
    print("Data Preprocessing Complete")

    model = create_cnn_model()
    train_model(model, X_train, y_train, X_val, y_val, output_dir)
    print("Data Model Training Complete")

    evaluate_model(model, X_test, y_test)
    print("Data Evaluation Complete")

    # Clean up local files
    os.remove("evaluation_metrics.json")

if __name__ == "__main__":
    main()
