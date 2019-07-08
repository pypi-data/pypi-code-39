from uuid import uuid4

from ._base import FileMixin
from ..._utils.multipart_encoder import MultipartEncoder


class Thumb(FileMixin):
    def thumb(self, thumb):

        # thumb must be a path
        if self.is_data:
            self.value.append(MultipartEncoder.encode_file('thumb', thumb))

        return self


class ToInputMedia(FileMixin):
    media_types = {'photo', 'video'}

    def to_input_media(self):
        serialized = {
            'type': self.file_type,
            **self.args,
            **self.attributes
        }

        if self.is_data:
            files = []
            for file in self.value:

                # avoid conflicts
                field_name = uuid4().hex

                # if it's neither a photo nor a video it's a thumb
                if file[0] in self.media_types:
                    serialized['media'] = f'attach://{field_name}'
                else:
                    serialized[file[0]] = f'attach://{field_name}'

                files.append((field_name, file[1], file[2], file[3]))
            return serialized, files
        else:
            serialized['media'] = self.value
            return serialized, None
