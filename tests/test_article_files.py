import os


FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test_files',
    )


def get_files(xml_file_path):
    path = os.path.dirname(xml_file_path)
    return [
        path+'/'+item
        for item in os.listdir(path)
        if not item.endswith('.xml')
    ]
