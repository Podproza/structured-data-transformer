import argparse
import json
from pathlib import Path

from structured_data_transformer.config.loader import load_transform_configs_from_file
from structured_data_transformer.config.transform_config import (
    wrap_configs_with_stable_anonymizer,
)
from structured_data_transformer.executor import apply_transforms


def parse_args():
    parser = argparse.ArgumentParser(
        description="Apply structured data transforms in place."
    )
    parser.add_argument(
        "--config",
        "-c",
        type=Path,
        required=True,
        help="Path to the JSON config file to load.",
    )
    parser.add_argument(
        "--base-dir",
        "-d",
        type=Path,
        required=True,
        help="Base directory containing the data to transform in place.",
    )
    parser.add_argument(
        "--cache-in",
        "-ci",
        type=Path,
        default=None,
        help="Optional path to input JSON cache file for stable anonymizer.",
    )
    parser.add_argument(
        "--cache-out",
        "-co",
        type=Path,
        default=None,
        help="Optional path to output JSON cache file for stable anonymizer.",
    )
    parser.add_argument(
        "--reverse-cache",
        "-r",
        action="store_true",
        help="Reverse keys and values in the input cache (for decoding instead of encoding).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    cache: dict[str, str] = {}

    if not args.base_dir.exists():
        raise FileNotFoundError(f"Base directory {args.base_dir} does not exist.")

    if args.cache_in:
        if not args.cache_in.exists():
            raise FileNotFoundError(f"Cache file {args.cache_in} does not exist.")
        cache = json.loads(args.cache_in.read_text())
        if args.reverse_cache:
            cache = {v: k for k, v in cache.items()}

    configs = load_transform_configs_from_file(args.config)

    cfgs = wrap_configs_with_stable_anonymizer(configs, cache)

    apply_transforms(configs=cfgs, base_dir=args.base_dir)

    if args.cache_out:
        args.cache_out.write_text(json.dumps(cache, indent=2))


if __name__ == "__main__":
    main()
