"""Metadata-driven resources: one ingestion job per source table (lab 06 stretch)."""
from databricks.bundles.core import Bundle, Resources
from databricks.bundles.jobs import Job

SOURCES = {
    "customers": "Daily",
    "products": "Weekly",
    "orders": "Hourly",
}


def load_resources(bundle: Bundle) -> Resources:
    resources = Resources()
    for table, cadence in SOURCES.items():
        resources.add_job(
            resource_name=f"ingest_{table}",
            job=Job.from_dict({
                "name": f"ingest_{table}",
                "description": f"{cadence} ingestion of {table} (generated from metadata)",
                "tasks": [{
                    "task_key": "ingest",
                    "notebook_task": {
                        "notebook_path": "src/notebooks/_setup.py",
                        "base_parameters": {"table": table},
                    },
                }],
                "tags": {"source_table": table},
            }),
        )
    return resources
