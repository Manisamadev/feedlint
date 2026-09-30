"""Allow running feedlint as `python -m feedlint`."""

import sys

from feedlint.cli import main

sys.exit(main())
