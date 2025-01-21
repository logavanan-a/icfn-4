from django.shortcuts import render

def validate_image(image):
    from django.core.exceptions import ValidationError
    file_size = image.file.size
    limit_mb = 1
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("Image size should not exceed more than %s MB" % limit_mb)