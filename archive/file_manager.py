import pandas as pd
import os


loaded_files = {}

def load_csv(file_description, default_filename):
    """

    General-purpose CSV loader that checks file existence.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, f"../data/{default_filename}")

    if not os.path.exists(data_path):
        print(f"Error: {file_description} file not found at {data_path}")
        return None
    try:
        pf = pd.read_csv(data_path)
        print(f"{file_description} loaded successfully")
        return pf
    except pd.errors.EmptyDataError:
        print(f"Error: {file_description} file is empty or incorrectly formatted")
        return None
def upload_file(file_type):
    file_name = input(f"Enter the CSV filename for {file_type}: ")
    df = load_csv(file_type, file_name)
    if df is not None:
        loaded_files[file_type] = df
    return df