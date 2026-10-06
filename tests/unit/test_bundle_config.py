"""Static checks on the bundle configuration — run in CI before any deployment."""
import pathlib
import re

import yaml

ROOT = pathlib.Path(__file__).parents[2]
YAML_FILES = [ROOT / "databricks.yml", *sorted((ROOT / "resources").glob("*.yml"))]


def test_all_bundle_files_are_valid_yaml():
    for f in YAML_FILES:
        assert isinstance(yaml.safe_load(f.read_text()), dict), f


def test_no_secrets_or_hardcoded_workspace_urls():
    patterns = [r"dapi[0-9a-f]{32}", r"https://[a-z0-9-]+\.(cloud\.databricks\.com|azuredatabricks\.net)",
                r"(?i)client_secret\s*:"]
    for f in YAML_FILES:
        text = f.read_text()
        for p in patterns:
            assert not re.search(p, text), f"{f.name} matches forbidden pattern {p}"


def test_environments_are_isolated():
    """dev / staging / prod must never share a catalog or a workspace path."""
    cfg = yaml.safe_load((ROOT / "databricks.yml").read_text())
    targets = cfg["targets"]
    assert targets["dev"]["mode"] == "development"
    catalogs = {cfg["variables"]["catalog"]["default"]}
    for name in ("staging", "prod"):
        t = targets[name]
        assert t["mode"] == "production"
        assert "${bundle.target}" in t["workspace"]["root_path"]
        catalogs.add(t["variables"]["catalog"])
    assert len(catalogs) == 3, "each environment needs its own catalog"


def test_every_referenced_source_file_exists():
    for f in YAML_FILES:
        for ref in re.findall(r"(?:path|notebook_path):\s*(\.\./[^\s]+)", f.read_text()):
            assert (f.parent / ref).resolve().exists(), f"{f.name} references missing {ref}"
