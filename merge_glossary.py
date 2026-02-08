#!/usr/bin/env python3
"""
Merge glossary fragment files into master glossary/terms.json.
Adds 'detailed' and 'example' fields from fragments to existing terms.
"""

import json
from pathlib import Path

def main():
    # Define paths
    base_dir = Path(__file__).parent
    fragments_dir = base_dir / "glossary" / "fragments"
    master_file = base_dir / "glossary" / "terms.json"

    # Fragment files
    fragment_files = [
        "foundations.json",
        "monetary-economics.json",
        "cbdc.json",
        "payment-systems.json",
        "platform-economics.json",
        "market-microstructure.json",
        "regulatory-economics.json",
        "synthesis.json"
    ]

    # Step 1: Read and validate all fragment files
    print("Reading fragment files...")
    fragment_data = {}

    for fname in fragment_files:
        fpath = fragments_dir / fname
        print(f"  - {fname}")

        with open(fpath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Validate: must be array of objects with id, detailed, example
        if not isinstance(data, list):
            raise ValueError(f"{fname}: must be JSON array")

        for i, entry in enumerate(data):
            if not isinstance(entry, dict):
                raise ValueError(f"{fname} entry {i}: must be object")
            if not all(k in entry for k in ['id', 'detailed', 'example']):
                raise ValueError(f"{fname} entry {i}: missing required keys")
            if not all(isinstance(entry[k], str) and entry[k].strip() for k in ['id', 'detailed', 'example']):
                raise ValueError(f"{fname} entry {i}: all values must be non-empty strings")

            # Store in lookup dict
            term_id = entry['id']
            if term_id in fragment_data:
                raise ValueError(f"Duplicate ID '{term_id}' found in {fname}")
            fragment_data[term_id] = {
                'detailed': entry['detailed'],
                'example': entry['example']
            }

    print(f"\nTotal fragment entries: {len(fragment_data)}")

    # Step 2: Read master glossary
    print(f"\nReading master glossary: {master_file}")
    with open(master_file, 'r', encoding='utf-8') as f:
        master = json.load(f)

    original_count = len(master['terms'])
    print(f"Master glossary has {original_count} terms")

    # Step 3: Merge fragments into master
    print("\nMerging fragments into master...")
    merged_count = 0
    missing_ids = []

    for term in master['terms']:
        term_id = term['id']
        if term_id in fragment_data:
            term['detailed'] = fragment_data[term_id]['detailed']
            term['example'] = fragment_data[term_id]['example']
            merged_count += 1
        else:
            missing_ids.append(term_id)

    print(f"Merged {merged_count} terms")

    if missing_ids:
        print(f"\nWARNING: {len(missing_ids)} IDs in master not found in fragments:")
        for mid in missing_ids[:10]:  # Show first 10
            print(f"  - {mid}")
        if len(missing_ids) > 10:
            print(f"  ... and {len(missing_ids) - 10} more")

    # Check for extra fragment IDs not in master
    master_ids = {term['id'] for term in master['terms']}
    extra_ids = set(fragment_data.keys()) - master_ids
    if extra_ids:
        print(f"\nWARNING: {len(extra_ids)} fragment IDs not in master:")
        for eid in sorted(extra_ids)[:10]:
            print(f"  - {eid}")
        if len(extra_ids) > 10:
            print(f"  ... and {len(extra_ids) - 10} more")

    # Step 4: Validate all terms now have detailed and example
    print("\nValidating merged data...")
    validation_errors = []
    for i, term in enumerate(master['terms']):
        for field in ['detailed', 'example']:
            if field not in term or not term[field]:
                validation_errors.append(f"Term {i} ('{term.get('id', 'NO-ID')}'): missing '{field}'")

    if validation_errors:
        print(f"ERROR: {len(validation_errors)} validation failures:")
        for err in validation_errors[:20]:
            print(f"  {err}")
        if len(validation_errors) > 20:
            print(f"  ... and {len(validation_errors) - 20} more")
        return 1

    print("Validation passed: all terms have 'detailed' and 'example'")

    # Step 5: Update metadata
    master['metadata']['totalTerms'] = len(master['terms'])
    master['metadata']['generated'] = "2026-02-07"

    # Step 6: Write merged file
    print(f"\nWriting merged glossary to {master_file}")
    with open(master_file, 'w', encoding='utf-8') as f:
        json.dump(master, f, ensure_ascii=False, indent=2)

    print(f"\nSUCCESS!")
    print(f"  Total terms: {len(master['terms'])}")
    print(f"  Terms merged: {merged_count}")
    print(f"  Fragment entries used: {merged_count}/{len(fragment_data)}")

    return 0

if __name__ == '__main__':
    exit(main())
