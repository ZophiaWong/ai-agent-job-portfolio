import re
from pathlib import Path


STATE_REL = Path(".local") / "interview-prep"
COMPETENCY_LEAF_COUNTS = {
    "C01": 3,
    "C02": 3,
    "C03": 3,
    "C04": 3,
    "C05": 4,
    "C06": 4,
    "C07": 4,
    "C08": 3,
    "C09": 3,
    "C10": 4,
    "C11": 3,
    "C12": 3,
    "C13": 3,
}


def reject_symlink_components(path, root):
    """Reject symlinks below a resolved repository root, including dangling links."""
    try:
        relative = path.absolute().relative_to(root)
    except ValueError as exc:
        raise ValueError(f"path is outside repository root: {path}") from exc
    current = root
    for component in relative.parts:
        current = current / component
        if current.is_symlink():
            raise ValueError(
                "symlink is not allowed because it can redirect outside the expected "
                f"private-state boundary: {current}"
            )


def ensure_within_boundary(path, boundary, root, label="path"):
    """Keep a non-symlink path inside the exact resolved boundary supplied by the caller."""
    reject_symlink_components(boundary, root)
    reject_symlink_components(path, root)
    resolved_boundary = boundary.resolve(strict=False)
    resolved_path = path.resolve(strict=False)
    try:
        resolved_path.relative_to(resolved_boundary)
    except ValueError as exc:
        raise ValueError(f"{label} resolves outside expected boundary {boundary}: {path}") from exc
    return path


def state_dir_for(root):
    state_dir = root / STATE_REL
    return ensure_within_boundary(
        state_dir, root, root, "interview prep state directory"
    )


def validate_single_line(value, label):
    if "\n" in value or "\r" in value:
        raise ValueError(f"{label} must not contain a newline")


def validate_competency_id(value):
    validate_single_line(value, "competency ID")
    match = re.fullmatch(r"(C(?:0[1-9]|1[0-3]))(?:\.(\d{2}))?", value)
    if match is None:
        raise ValueError(f"unknown competency ID: {value}")
    parent, leaf = match.groups()
    if leaf is not None and not 1 <= int(leaf) <= COMPETENCY_LEAF_COUNTS[parent]:
        raise ValueError(f"unknown competency ID: {value}")


def write_exclusive_with_suffix(directory, base_stem, build_text, root, attempts=1000):
    """Create a Markdown file without overwriting, adding a numeric suffix on collision."""
    for index in range(attempts):
        stem = base_stem if index == 0 else f"{base_stem}-{index + 1}"
        path = ensure_within_boundary(
            directory / f"{stem}.md", directory, root, "session file"
        )
        try:
            with path.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(build_text(stem))
        except FileExistsError:
            continue
        return path, stem
    raise RuntimeError(f"could not allocate a unique session file after {attempts} attempts")
