# coding = utf-8

import mimetypes


class File:

    def __init__(self, file_name, content=None, content_type=None):
        self.name = file_name
        self.content = content
        self.size = len(content) if content is not None else None
        self.content_type = content_type
        if content_type is None and file_name is not None:
            self.content_type = mimetypes.guess_type(file_name)[0]

    def properties(self):
        return {
            'content_size': self.size,
            'content_type': self.content_type,
            'file_name': self.name,
        }
