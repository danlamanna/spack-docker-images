import json
import os
import re
from datetime import datetime
from typing import Any

import gitlab
from kubernetes import client, config
from opensearch_dsl import Date, Document, connections

from django.conf import settings

config.load_config()
v1_client = client.CoreV1Api()


class JobLog(Document):
    timestamp = Date()

    class Index:
        name = "gitlab-job-logs-*"

    def save(self, **kwargs):
        # assign now if no timestamp given
        if not self.timestamp:
            self.timestamp = datetime.utcnow()

        # override the index to go to the proper timeslot
        kwargs["index"] = self.timestamp.strftime("gitlab-job-logs-%Y%m%d")
        return super().save(**kwargs)


def upload_job_log(job_input_data: dict[str, Any]) -> None:
    gl = gitlab.Gitlab(settings.GITLAB_ENDPOINT, settings.GITLAB_TOKEN)

    # job_input_data = {
    #    "build_id": 8923212,
    #    "project_id": 2,
    #    "project": {"web_url": "https://gitlab.spack.io/spack/spack"},
    # }

    print(job_input_data)
    # Retrieve project and job from gitlab API
    print("getting project")
    project = gl.projects.get(job_input_data["project_id"])
    print("getting job")
    job = project.jobs.get(job_input_data["build_id"])
    print("getting trace")
    job_trace: str = job.trace().decode()

    # TODO: this still leaves trailing ;m in the output
    job_trace = re.sub(
        r"\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|G|K]?", "", job_trace
    )

    # Upload to OpenSearch
    connections.create_connection(
        hosts=[settings.OPENSEARCH_ENDPOINT],
        http_auth=(
            settings.OPENSEARCH_USERNAME,
            settings.OPENSEARCH_PASSWORD,
        ),
    )
    print("making doc")
    doc = JobLog(
        **job_input_data,
        job_url=f'{job_input_data["project"]["web_url"]}/-/jobs/{job_input_data["build_id"]}',
        job_trace=job_trace,
    )
    print("saving doc")
    doc.save()
