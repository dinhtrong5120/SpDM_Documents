#!/usr/bin/env python3
"""Validate structural invariants of SPDM draw.io flowcharts."""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def fail(message: str) -> None:
    raise ValueError(message)


def validate(path: Path) -> tuple[int, int, int]:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        fail(f"XML không hợp lệ: {exc}")

    if root.tag != "mxfile":
        fail("Root element phải là mxfile")

    diagrams = root.findall("diagram")
    if not diagrams:
        fail("Không có diagram nào")

    total_nodes = 0
    total_decisions = 0
    total_terminators = 0
    total_processes = 0

    for diagram in diagrams:
        name = diagram.get("name", "<không tên>")
        cells = diagram.findall("./mxGraphModel/root/mxCell")
        ids = [cell.get("id") for cell in cells]
        if any(identifier is None for identifier in ids):
            fail(f"{name}: có mxCell thiếu id")
        if len(ids) != len(set(ids)):
            fail(f"{name}: mxCell id bị trùng")

        by_id = {cell.get("id"): cell for cell in cells}
        edges = [cell for cell in cells if cell.get("edge") == "1"]
        vertices = [cell for cell in cells if cell.get("vertex") == "1"]
        total_nodes += len(vertices)

        for edge in edges:
            if edge.get("source") not in by_id:
                fail(f"{name}: edge {edge.get('id')} có source không tồn tại")
            if edge.get("target") not in by_id:
                fail(f"{name}: edge {edge.get('id')} có target không tồn tại")

        swimlanes = [cell for cell in vertices if "swimlane;" in cell.get("style", "")]
        lane_names = {cell.get("value") for cell in swimlanes}
        expected_lanes = {"Data input", "Data processing", "Business logic"}
        if not expected_lanes.issubset(lane_names):
            missing = ", ".join(sorted(expected_lanes - lane_names))
            fail(f"{name}: thiếu swimlane: {missing}")

        decisions = [cell for cell in vertices if "rhombus;" in cell.get("style", "")]
        terminators = [
            cell for cell in vertices
            if "rounded=1" in cell.get("style", "") and "swimlane;" not in cell.get("style", "")
        ]
        processes = [
            cell for cell in vertices
            if "rounded=0" in cell.get("style", "") and "rhombus;" not in cell.get("style", "")
        ]
        total_decisions += len(decisions)
        total_terminators += len(terminators)
        total_processes += len(processes)

        for decision in decisions:
            labels = sorted(
                edge.get("value", "")
                for edge in edges
                if edge.get("source") == decision.get("id")
            )
            if labels != ["NO", "YES"]:
                fail(
                    f"{name}: decision {decision.get('id')} phải có đúng "
                    f"hai nhánh YES/NO, hiện có {labels}"
                )

    if not total_terminators:
        fail("Flowchart thiếu Terminator")
    if not total_processes:
        fail("Flowchart thiếu Process")
    if not total_decisions:
        fail("Flowchart thiếu Decision")

    return len(diagrams), total_nodes, total_decisions


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SPDM draw.io flowchart")
    parser.add_argument("path", type=Path, help="Đường dẫn tới file .drawio")
    args = parser.parse_args()

    if not args.path.is_file():
        print(f"Không tìm thấy file: {args.path}", file=sys.stderr)
        return 2

    try:
        diagrams, nodes, decisions = validate(args.path)
    except ValueError as exc:
        print(f"KHÔNG HỢP LỆ: {exc}", file=sys.stderr)
        return 1

    print(
        f"HỢP LỆ: {diagrams} diagram, {nodes} vertex, "
        f"{decisions} decision; tất cả decision có YES/NO."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
