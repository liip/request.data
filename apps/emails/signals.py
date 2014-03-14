import django.dispatch

notify_event = django.dispatch.Signal(providing_args=['request', 'comment', 'creator'])