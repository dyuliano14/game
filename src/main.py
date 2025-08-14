import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.ui.routes import route_manager

if __name__ == "__main__":
    route_manager()