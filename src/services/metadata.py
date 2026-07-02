from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class ProjectMetadata:
    project_name: str = "CricketAnalytics"
    version: str = "1.0.0"
    generated_at: str = datetime.now(timezone.utc).isoformat()
    data_source: str = "IPL ball-by-ball and match datasets"
    deployment_target: str = "Streamlit Cloud / local"


def get_project_metadata() -> ProjectMetadata:
    return ProjectMetadata()


def get_project_metadata_summary() -> dict[str, str]:
    metadata = get_project_metadata()
    return {
        "project_name": metadata.project_name,
        "version": metadata.version,
        "generated_at": metadata.generated_at,
        "data_source": metadata.data_source,
        "deployment_target": metadata.deployment_target,
    }
