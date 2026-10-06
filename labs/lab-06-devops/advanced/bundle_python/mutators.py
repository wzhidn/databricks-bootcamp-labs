"""Organisation standards applied to every job at deploy time (lab 06 stretch)."""
from dataclasses import replace

from databricks.bundles.core import Bundle, job_mutator
from databricks.bundles.jobs import Job


@job_mutator
def add_standard_tags(bundle: Bundle, job: Job) -> Job:
    tags = dict(job.tags or {})
    tags.setdefault("cost_center", "bootcamp")
    tags["deployed_by"] = "bundle"
    tags["target"] = bundle.target
    return replace(job, tags=tags)
