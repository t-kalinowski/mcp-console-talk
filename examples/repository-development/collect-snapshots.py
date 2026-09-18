"""Count actual tracked text lines in every first-parent snapshot of main."""
import csv
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def classify(path: str) -> str:
    if path.startswith(("tests/", "r/tests/", "python/tests/")) and path.lower().endswith((".yaml", ".yml")):
        return "Test transcripts"
    if path.startswith(("tests/snapshots/", "tests/transcripts/golden/")):
        return "Test code & fixtures"
    if path.startswith(("docs/", "design-sketches/", "examples/", "r/man/")) or path.endswith((".md", ".qmd", ".rst", ".Rd")):
        return "Docs & examples"
    if path.startswith(("tests/", "r/tests/", "python/tests/")):
        return "Test code & fixtures"
    if path.startswith(("src/", "python/mcp_console/", "r/R/", "r/src/")):
        return "Core code"
    return "Build & tooling"


def collect(repo: Path, revision: str, output_dir: Path) -> None:
    assert repo.is_dir()
    output_dir.mkdir(parents=True, exist_ok=True)
    command = ["git", "-C", str(repo)]
    head = subprocess.check_output(command + ["rev-parse", "--verify", revision], text=True).strip()
    history = subprocess.check_output(command + ["log", "--first-parent", "--reverse", "--format=%H%x00%cI%x00%s", head], text=True)
    commits = [line.split("\0", 2) for line in history.splitlines()]
    dates = [datetime.fromisoformat(row[1]) for row in commits]
    assert all(b >= a for a, b in zip(dates, dates[1:])), "Non-monotone first-parent commit times need explicit treatment."
    blobs = {}
    snapshots = []
    ignored = Counter()
    current_files = []
    with subprocess.Popen(command + ["cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE) as reader:
        assert reader.stdin is not None and reader.stdout is not None
        for index, (commit, timestamp, subject) in enumerate(commits):
            totals = {key: 0 for key in ("Core code", "Test code & fixtures", "Test transcripts", "Docs & examples", "Build & tooling")}
            paths = subprocess.check_output(command + ["ls-tree", "-r", "-z", commit]).split(b"\0")
            snapshot_files = []
            text_files = 0
            binary_files = 0
            text_bytes = 0
            for entry in paths:
                if not entry:
                    continue
                identity, raw_path = entry.split(b"\t", 1)
                mode, object_type, object_id = identity.decode("ascii").split()
                path = raw_path.decode("utf-8")
                if mode not in ("100644", "100755"):
                    ignored[mode] += 1
                    continue
                assert object_type == "blob"
                if object_id not in blobs:
                    reader.stdin.write(object_id.encode("ascii") + b"\n")
                    reader.stdin.flush()
                    returned_id, returned_type, size = reader.stdout.readline().decode("ascii").strip().split()
                    assert returned_id == object_id and returned_type == "blob"
                    data = reader.stdout.read(int(size))
                    assert len(data) == int(size) and reader.stdout.read(1) == b"\n"
                    binary = b"\0" in data[:8000]
                    lines = 0 if binary else data.count(b"\n") + int(bool(data) and not data.endswith(b"\n"))
                    blobs[object_id] = {"bytes": len(data), "binary": binary, "lines": lines}
                info = blobs[object_id]
                category = classify(path)
                totals[category] += info["lines"]
                text_files += int(not info["binary"])
                binary_files += int(info["binary"])
                text_bytes += info["bytes"] if not info["binary"] else 0
                snapshot_files.append({"path": path, "blob": object_id, "category": category, **info})
            snapshots.append({
                "sequence": index + 1, "commit": commit,
                "committed_at": datetime.fromisoformat(timestamp).astimezone(timezone.utc).isoformat(),
                "subject": subject, **totals, "total": sum(totals.values()),
                "text_files": text_files, "binary_files": binary_files, "text_bytes": text_bytes,
            })
            current_files = snapshot_files
            if (index + 1) % 50 == 0 or index == len(commits) - 1:
                print(f"Counted {index + 1}/{len(commits)} snapshots; {len(blobs)} distinct blobs", flush=True)
        reader.stdin.close()
        assert reader.wait() == 0
    (output_dir / "snapshot-counts.json").write_text(json.dumps(snapshots, indent=2) + "\n")
    (output_dir / "blob-counts.json").write_text(json.dumps(blobs, indent=2) + "\n")
    with (output_dir / "current-files.csv").open("w", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=list(current_files[0]))
        writer.writeheader()
        writer.writerows(current_files)
    metadata = {
        "repository": "t-kalinowski/mcp-console", "local_repository": str(repo),
        "requested_revision": revision, "pinned_main_head": head,
        "fetched_at": datetime.now(timezone.utc).isoformat(), "snapshots": len(snapshots),
        "distinct_blobs_counted": len(blobs), "ignored_mode_occurrences": dict(ignored),
        "measurement": "Physical lines in tracked regular text files, including blank lines and comments; a nonempty unterminated final line counts as one.",
        "binary_rule": "Files with a NUL byte in the first 8000 bytes are excluded from line counts.",
        "history": "Every first-parent commit on pinned origin/main, counted from the complete tree. Includes direct commits and merges; side branches are not counted separately.",
        "time": "Committer timestamp in UTC; all first-parent timestamps are nondecreasing.",
        "category_rule": "Test transcripts are .yaml/.yml files anywhere under tests/, r/tests/, or python/tests/, regardless of historical subdirectory. Non-YAML snapshot fixtures remain Test code & fixtures. CI/configuration YAML remains Build & tooling. Examples are included with Docs & examples.",
        "limitations": "Core files include inline tests and documentation comments. Binary content, Git metadata and untracked files are excluded. This is repository content, not code-only SLOC or disk usage.",
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps(snapshots[-1], indent=2))


if __name__ == "__main__":
    assert len(sys.argv) == 4, "Usage: collect-snapshots.py REPO REVISION OUTPUT_DIRECTORY"
    collect(Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]))
