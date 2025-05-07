import os
import json
import logging

def load_file(file_path, file_type="file"):
    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo {file_path} não encontrado.")
    with open(file_path, 'r') as f:
        return json.load(f)

def load_payload(file_path):
    return load_file(file_path, "payload")

def load_expected_body_file(file_path):
    return load_file(file_path, "expected_body_file")
