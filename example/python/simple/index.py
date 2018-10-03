import requests

def handler_name(event, context):
    return {
        "ok": requests.__name__
    }
