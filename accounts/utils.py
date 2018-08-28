import os
import uuid


def get_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('avatars/', filename)


DEFAULT_AVATAR_PATH = '/media/static/no_avatar.png'
