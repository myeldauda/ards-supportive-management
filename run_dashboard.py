import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.dashboard.dashboard import app

if __name__ == "__main__":
    app.run(debug=True)