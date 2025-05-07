def mask_sensitive_data(data):
    sensitive_keys = ["Authorization", "x-api-key"]
    return {k: ("*****" if k in sensitive_keys else v) for k, v in data.items()}
