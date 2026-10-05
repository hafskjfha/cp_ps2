"""Select the verified, exactly score-preserving runtime variant of checkpoint 055."""
import hashlib
import json
from pathlib import Path

from checkpoint import validate_benchmark
from check_submission import inspect_source

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf8"))


def main():
    source = ROOT / "solvers/experiments/seven_fast_runtime.py"
    data = source.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    assert inspect_source(source)["valid"]
    parent = read("results/checkpoints/best_055_254652429.benchmark.json")
    names = {"benchmark": "stable", "readiness": "readiness", "stress": "stress",
             "periodic": "periodic", "reproduction": "reproduction"}
    evidence = {key: read(f"results/seven_fast_{value}.json") for key, value in names.items()}
    benchmark = evidence["benchmark"]
    assert validate_benchmark(benchmark) == validate_benchmark(parent)
    assert benchmark["manifest_sha256"] == parent["manifest_sha256"]
    assert benchmark["total_score"] == parent["total_score"] == 254652429
    old = {row["id"]: row for row in parent["results"]}
    for row in benchmark["results"]:
        assert row["score"] == old[row["id"]]["score"]
        assert row["output_sha256"] == old[row["id"]]["output_sha256"]
    for key, report in evidence.items():
        assert report["solver_sha256"] == digest
        assert 0 <= report["max_runtime_sec"] <= 5
        if key != "benchmark":
            assert report.get("passed", report.get("valid"))
            rows = report["cases"] if key in ("readiness", "stress") else report["results"]
            expected = {"readiness": 38, "stress": 36, "periodic": 14, "reproduction": 47}[key]
            assert len(rows) == expected
            assert all(row["valid"] and 0 <= row["runtime_sec"] <= 5 for row in rows)
            assert report["max_runtime_sec"] + 1e-9 >= max(row["runtime_sec"] for row in rows)
    stable = {row["id"]: row for row in benchmark["results"]}
    reproduced_ids = set()
    for row in evidence["reproduction"]["results"]:
        assert row["reproduced"] and row["id"] not in reproduced_ids
        reproduced_ids.add(row["id"])
        for field in ("score", "matches", "input_sha256", "output_sha256"):
            assert row[field] == stable[row["id"]][field]
    baseline = read("results/checkpoints/runtime_053_254103898.benchmark.json")
    starting = {row["id"]: row for row in baseline["results"]}
    assert reproduced_ids == {key for key, row in stable.items() if row["score"] != starting[key]["score"]}
    assert evidence["reproduction"]["cases"] == 47
    assert evidence["readiness"]["cases_total"] == 38
    assert evidence["stress"]["cases_total"] == 36
    assert evidence["periodic"]["cases_total"] == 14
    # All evidence is checked before any selection or immutable-file mutation.
    stem = "runtime_055_254652429"
    destination = ROOT / "submissions" / (stem + ".py")
    paths = {key: ROOT / "results/checkpoints" / (stem + "." + key + ".json") for key in evidence}
    assert not destination.exists() and not any(path.exists() for path in paths.values())
    variants = read("results/runtime_variants.json")
    assert not any(row["id"] == 55 for row in variants)
    parent_source = ROOT / "submissions/best_055_254652429.py"
    assert hashlib.sha256(parent_source.read_bytes()).hexdigest() == parent["solver_sha256"]
    worst = max(report["max_runtime_sec"] for report in evidence.values())
    record = dict(id=55, kind="verified_runtime_variant", strict_score_improvement=False,
                  total_score=benchmark["total_score"], avg_score=benchmark["avg_score"],
                  runtime_sec=benchmark["runtime_sec"], max_runtime_sec=benchmark["max_runtime_sec"],
                  worst_verified_runtime_sec=worst, source_bytes=len(data),
                  description="All 320 checkpoint055 outputs preserved exactly; private cluster states copy bytearrays and update only consumed score planes. Expanded runtime checks passed.",
                  file=destination.relative_to(ROOT).as_posix(), solver_sha256=digest,
                  score_checkpoint=parent_source.relative_to(ROOT).as_posix(),
                  score_checkpoint_sha256=parent["solver_sha256"],
                  manifest_sha256=benchmark["manifest_sha256"])
    for key, path in paths.items():
        with path.open("x", encoding="utf8") as stream:
            json.dump(evidence[key], stream, indent=2)
            stream.write("\n")
        record[key] = path.relative_to(ROOT).as_posix()
    with destination.open("xb") as stream:
        stream.write(data)
    variants.append(record)
    (ROOT / "results/runtime_variants.json").write_text(json.dumps(variants, indent=2) + "\n", encoding="utf8")
    (ROOT / "results/best.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf8")
    (ROOT / "solvers/current.py").write_bytes(data)
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
