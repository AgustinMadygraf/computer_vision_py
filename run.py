"""
Path: run.py
"""

import sys
import os
import uvicorn

from src.shared.config import get_config
from src.composition_root import get_app


if __name__ == "__main__":
    debug = "--debug" in sys.argv
    if debug:
        os.environ["CV_DEBUG"] = "DEBUG"
    config = get_config()
    app = get_app()
    uvicorn.run(
        "src.composition_root:get_app",
        host="0.0.0.0",
        port=5001,
        reload=True,
        factory=True
    )
