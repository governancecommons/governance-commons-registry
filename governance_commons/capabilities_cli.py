"""CLI for capability provider discovery."""
from __future__ import annotations

import argparse
import json
import sys

from .capabilities import discover_capabilities


def discover_cmd() -> None:
    parser = argparse.ArgumentParser(
        prog="gc-discover",
        description="Discover validated Capability Contract v0.1 providers.",
    )
    parser.add_argument(
        "--capability",
        help="Return only providers of this exact capability ID.",
    )
    parser.add_argument(
        "--output",
        default="text",
        choices=["text", "json"],
        help="Output format (default: text).",
    )
    parser.add_argument(
        "roots",
        nargs="+",
        help="Repository roots or explicit capabilities.yaml files to scan.",
    )
    args = parser.parse_args()

    result = discover_capabilities(args.roots, args.capability)
    if args.output == "json":
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    else:
        query = args.capability or "all capabilities"
        print("GC Capability Discovery")
        print(f"  Query:     {query}")
        print(f"  Scanned:   {result.scanned_contracts} contract(s)")
        print("  Authority: not evaluated; discovery does not grant execution authority")
        print()
        if result.providers:
            for provider in result.providers:
                print(
                    f"  + {provider['capability_id']} {provider['capability_version']} "
                    f"by {provider['component_id']} ({provider['stability']})"
                )
                print(f"      source: {provider['source_file']}")
        else:
            print("  No providers found.")
        if result.invalid_contracts:
            print("\n  Invalid contracts:")
            for contract in result.invalid_contracts:
                print(f"  ! {contract.source_file}")
                for issue in contract.issues:
                    print(f"      [{issue.rule_id}] {issue.path}: {issue.message}")

    sys.exit(0 if result.valid else 1)
