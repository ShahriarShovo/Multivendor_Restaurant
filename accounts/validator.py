from django.core.exceptions import ValidationError

import os

def allow_only_image(value):
    extension=os.path.splitext(value.name)[1]
    print(extension)

    valid_extension=['.jpg','.png','.jpeg']
    if not extension.lower() in valid_extension:
        raise ValidationError('unsupported file extension. Allow Extension'+str(valid_extension))
    