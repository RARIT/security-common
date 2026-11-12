# security-common

Shared Python library for the Security Platform scanners.

`security-common` contains all functionality that is shared across scanners, including:

- Azure Managed Identity authentication
- Azure Blob Storage access
- Reading platform assets
- Reading platform configuration
- Findings management
- Standardized logging

The library is intentionally scanner-agnostic and does not contain any scanner-specific logic.

## Purpose

Each scanner should focus only on collecting findings.

Examples:

- security-nuclei
- security-ssl
- security-nmap
- security-zap

Shared functionality should be implemented once in `security-common` and reused by all scanners.

---

# Directory Structure

```text
security_common/

├── __init__.py
├── config.py
├── logger.py
├── blob.py
├── assets.py
└── findings.py
```

---

# Environment Variables

| Variable | Description |
|-----------|-----------|
| ACCOUNT_NAME | Azure Storage Account name |
| CLIENT_ID | User Assigned Managed Identity Client ID |
| ASSETS_CONTAINER | Storage container containing platform configuration |
| FINDINGS_CONTAINER | Storage container containing scanner findings |
| SECURITY_ASSETS_FILE | Assets definition file |
| SECURITY_PLATFORMS_FILE | Platform configuration file |
| LOG_LEVEL | Logging level (INFO, DEBUG, WARNING, ERROR) |

Example:

```text
ACCOUNT_NAME=securityplatformstorage
CLIENT_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
ASSETS_CONTAINER=assets
FINDINGS_CONTAINER=findings
SECURITY_ASSETS_FILE=security-assets.json
SECURITY_PLATFORMS_FILE=security-platforms.json
LOG_LEVEL=INFO
```

---

# Blob Storage Layout

```text
assets/
│
├── security-assets.json
└── security-platforms.json

findings/
│
├── nuclei/
│   ├── latest.json
│   └── archive/
│
├── ssl/
├── nmap/
└── zap/
```

---

# Assets

## security-assets.json

```json
[
  {
    "title": "Example Website",
    "url": "https://example.com",
    "platform": "wordpress",
    "active": true
  }
]
```

## security-platforms.json

```json
{
  "wordpress": {
    "nuclei": true,
    "wpscan": true,
    "ssl": true
  }
}
```

---

# Usage

## Logging

```python
from security_common.logger import get_logger

logger = get_logger("nuclei")
logger.info("Starting scan")
```

## Assets

```python
from security_common.assets import AssetManager

scan_assets = AssetManager().get_assets_for_scanner(
    "nuclei"
)
```

## Findings

```python
from security_common.findings import FindingsManager

findings = FindingsManager()

findings.upload_latest(
    "nuclei",
    "/tmp/results.json"
)
```

```python
findings.upload_json(
    "ssl",
    data
)
```

```python
latest = findings.download_latest(
    "ssl"
)
```

---

# Design Principles

- No scanner-specific logic
- No platform-specific logic
- Shared authentication layer
- Shared storage layer
- Shared logging
- Shared findings management

Scanners are responsible for:

- Target collection
- Scanner execution
- Result parsing
- Result normalization

`security-common` is responsible for:

- Configuration
- Authentication
- Storage access
- Asset filtering
- Findings persistence
- Logging

---

# Versioning

```text
v1.0.0
v1.1.0
v2.0.0
```

Use semantic versioning when introducing changes.
