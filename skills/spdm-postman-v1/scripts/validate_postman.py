#!/usr/bin/env python3
"""
Validation script for Postman Collection JSON files according to SPDM_POSTMAN_v1 rules.
Usage:
    python validate_postman.py <path_to_collection.json>
"""
import sys
import json
import os

def count_items(items, legacy_folder_names=None):
    if legacy_folder_names is None:
        legacy_folder_names = ["90 - Legacy / Not in current routes", "Legacy", "Legacy / Not in current routes"]

    active_count = 0
    legacy_count = 0
    empty_count = 0
    urls = []

    for item in items:
        name = item.get("name", "")
        # Check if item is a folder
        if "item" in item and isinstance(item["item"], list):
            is_legacy = any(leg.lower() in name.lower() for leg in legacy_folder_names)
            sub_act, sub_leg, sub_emp, sub_urls = count_items(item["item"], legacy_folder_names)
            if is_legacy:
                legacy_count += sub_act + sub_leg
            else:
                active_count += sub_act
                legacy_count += sub_leg
            empty_count += sub_emp
            urls.extend(sub_urls)
        else:
            # Request item
            req = item.get("request")
            if not req:
                empty_count += 1
                continue
            
            raw_url = ""
            if isinstance(req, dict):
                url_obj = req.get("url", "")
                if isinstance(url_obj, dict):
                    raw_url = url_obj.get("raw", "")
                elif isinstance(url_obj, str):
                    raw_url = url_obj
            
            if not raw_url.strip():
                empty_count += 1
            else:
                active_count += 1
                urls.append(raw_url)

    return active_count, legacy_count, empty_count, urls

def validate_collection(filepath):
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}", file=sys.stderr)
        return False

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in {filepath}: {e}", file=sys.stderr)
        return False
    except UnicodeDecodeError as e:
        print(f"[ERROR] Encoding error in {filepath}: {e}", file=sys.stderr)
        return False

    if not isinstance(data, dict):
        print(f"[ERROR] Root of collection must be a JSON object, got {type(data).__name__}", file=sys.stderr)
        return False

    info = data.get("info")
    if not isinstance(info, dict):
        print(f"[ERROR] 'info' field is required and must be an object", file=sys.stderr)
        return False

    name = info.get("name", "Unnamed")
    schema = info.get("schema", "")
    print(f"[INFO] Collection Name: {name}")
    print(f"[INFO] Schema: {schema}")

    items = data.get("item", [])
    if not isinstance(items, list):
        print(f"[ERROR] 'item' field must be an array, got {type(items).__name__}", file=sys.stderr)
        return False

    active_count, legacy_count, empty_count, urls = count_items(items)
    unique_urls = set(urls)
    potential_dupes = len(urls) - len(unique_urls)

    print("-" * 50)
    print(f"Total active requests: {active_count}")
    print(f"Legacy requests:       {legacy_count}")
    print(f"Empty/missing URLs:    {empty_count}")
    print(f"Duplicate URLs found:  {potential_dupes}")
    print("-" * 50)
    print("[SUCCESS] Collection structure is valid.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_postman.py <path_to_collection.json>")
        sys.exit(1)

    ok = validate_collection(sys.argv[1])
    sys.exit(0 if ok else 1)
