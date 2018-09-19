import json

from ui_helpers import get_static, render_page

def lambda_handler(event, context):
    print(event)
    if event["path"].lower() == "/favicon.ico":
        return get_static("static/favicon.ico")
    params = {
        "title":"Example index page!",
        "data_blob":"Here's the event that the lambda behind all this stuff received:\n\n" + json.dumps(event, indent=4, sort_keys=True)
    }
    return render_page(name="index.html", params=params)
