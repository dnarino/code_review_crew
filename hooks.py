

def read_file_hook(inputs):
    filename = inputs.get('file_path')
    if not filename:
        raise ValueError("Missing 'file_path' in inputs")
    try:
        with open(filename, 'r') as f:
            file_contents = f.read()
    except Exception as e:
        raise RuntimeError(f"Failed to read file {filename}: {e}")

    inputs["code_changes"] = file_contents

    return inputs

