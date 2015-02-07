from django.dispatch import Signal
photo_submit = Signal(providing_args=["url",'user', "summary","tags","is_staff"])