import json
import os
import traceback

from typing import Any, Dict, Optional

from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types

app = APIGatewayRestResolver()

TASK_ROOT = os.environ["LAMBDA_TASK_ROOT"]

def build_timestamp():
    with open(os.path.join(TASK_ROOT, "BUILD_TIMESTAMP"),"r") as f:
        return f.read()
    # with open("BUILD_TIMESTAMP","r") as f:
    #     return f.read()

BT = build_timestamp()

@app.get(f"/")
def landing_page() -> Response:
    """Render the landing page"""
    return Response(status_code=200, content_type=content_types.TEXT_HTML, body=f"<pre>Hello, world! I was built at {BT}</pre>")

def handle(event: Dict[str, Any], context: Any) -> Optional[Response | Dict[str, Any]]:
    try:
        return app.resolve(event, context)
    except Exception:
        event_dump = json.dumps(event, sort_keys=True, default=str)
        context_dump = json.dumps(vars(context), sort_keys=True, default=str)
        error_dump = traceback.format_exc()
        body = f"""
<pre>
EVENT:

{event_dump}

CONTEXT:

{context_dump}

EXCEPTION:

{error_dump}
</pre>""".strip()
        return Response(status_code=500, content_type=content_types.TEXT_HTML, body=body)
