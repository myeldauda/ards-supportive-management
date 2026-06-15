import os
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.dashboard.dashboard import app

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            8050
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
    )