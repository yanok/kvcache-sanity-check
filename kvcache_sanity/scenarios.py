from importlib import resources
from pathlib import Path

import yaml

from kvcache_sanity.models import Scenario
from kvcache_sanity.paths import user_data_dir

DEFAULT_SCENARIOS_FILE = resources.files("kvcache_sanity") / "data" / "scenarios" / "default.yaml"


def _read_file(path: Path) -> dict[str, Scenario]:
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    return {s["id"]: Scenario(**s) for s in data.get("scenarios", [])}


def load_scenarios(scenarios_file: str | Path | None = None) -> list[Scenario]:
    """Load scenarios.

    With an explicit scenarios_file, that file is used exclusively (full
    override). Otherwise, loads the bundled default.yaml and merges in every
    *.yaml file under the user scenarios directory (see paths.user_data_dir())
    if it exists — user scenarios win on a matching id.
    """
    if scenarios_file is not None:
        return list(_read_file(scenarios_file).values())

    merged = _read_file(DEFAULT_SCENARIOS_FILE)

    user_scenarios_dir = user_data_dir() / "scenarios"
    if user_scenarios_dir.is_dir():
        for path in sorted(user_scenarios_dir.glob("*.yaml")):
            merged.update(_read_file(path))

    return list(merged.values())
