from typing import Any
from django.http import HttpRequest, HttpResponse
import json

from analytics.job_log_uploader import upload_job_log


def webhook_handler(request: HttpRequest) -> HttpResponse:
    job_input_data: dict[str, Any] = json.loads(request.body)

    if job_input_data.get("object_kind") != "build":
        raise ValueError("Not a build event")

    upload_job_log(job_input_data)

    return HttpResponse("OK", status=202)
