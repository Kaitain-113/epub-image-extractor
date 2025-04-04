import os
import uuid
import zipfile


def generate_uuid_string(prefix='') -> str:
    """
    Generate a UUID string with a prefix.
    """
    return prefix.replace(' ', '') + str(uuid.uuid4())


def file_compressor(
    target_folder: str,
    file_targets: list,
    compressed_file_name=generate_uuid_string(),
    file_type='zip',
) -> None:
    compressed_file_header = {
        'zip': 'application/zip',
    }

    compressed_file = f'{target_folder}/{compressed_file_name}.{file_type}'

    with zipfile.ZipFile(compressed_file, 'w') as zipf:
        for file in file_targets:
            zipf.write(file, os.path.basename(file))

    return compressed_file, compressed_file_name, compressed_file_header[file_type]
