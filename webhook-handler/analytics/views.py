from typing import Any
from django.http import HttpRequest, HttpResponse
import json

import sentry_sdk

from analytics.job_log_uploader import upload_job_log


def webhook_handler(request: HttpRequest) -> HttpResponse:
    print("here")
    job_input_data: dict[str, Any] = json.loads(request.body)

    if job_input_data.get("object_kind") != "build":
        raise ValueError("Not a build event")

    try:
        upload_job_log(job_input_data)
    except Exception as e:
        sentry_sdk.capture_exception()
        print(e)
        raise

    return HttpResponse("OK", status=200)
