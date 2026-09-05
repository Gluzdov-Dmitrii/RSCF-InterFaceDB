# Data workspace

This directory separates immutable inputs from reviewed research products.

| Directory | Purpose | Git policy |
| --- | --- | --- |
| `external/` | snapshots from public databases | data files ignored |
| `raw/` | source-native exports and machine extractions | data files ignored |
| `interim/` | parsed but not scientifically reviewed records | data files ignored |
| `processed/` | normalized and deduplicated records | data files ignored |
| `curated/` | human-approved release candidates | data files ignored |
| `schemas/` | machine-readable contracts | tracked |

Never modify a raw input in place. Every transformation must record its input hash,
software version, parameters and output location. Only schemas, small synthetic fixtures,
checksums and DVC pointer files belong in Git. A public release must contain only records
whose redistribution status has been verified.
