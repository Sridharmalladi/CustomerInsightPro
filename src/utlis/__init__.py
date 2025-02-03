# src/utils/__init__.py
from .database import DatabaseConnection
from .logger import setup_logger
from .helpers import load_config, save_results

# src/utils/database.py
import sqlalchemy as db
from typing import Dict
import yaml
import os
from dotenv import load_dotenv

class DatabaseConnection:
    def __init__(self, config_path: str = 'config/database.yaml'):
        load_dotenv()
        self.config = self._load_config(config_path)
        self.engine = self._create_engine()
    
    def _load_config(self, config_path: str) -> Dict:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            env = os.getenv('ENVIRONMENT', 'development')
            return config[env]
    
    def _create_engine(self) -> db.Engine:
        conn_str = f"postgresql://{self.config['user']}:{self.config['password']}@" \
                  f"{self.config['host']}:{self.config['port']}/{self.config['database']}"
        return db.create_engine(conn_str)
    
    def execute_query(self, query: str) -> list:
        """Execute SQL query and return results."""
        with self.engine.connect() as conn:
            result = conn.execute(db.text(query))
            return [dict(row) for row in result]

# src/utils/logger.py
import logging
from datetime import datetime
import os

def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """Set up logger with specified configuration."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler if log_file specified
    if log_file:
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# src/utils/helpers.py
import yaml
import json
from typing import Dict, Any
from pathlib import Path
from datetime import datetime

def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def save_results(results: Dict[str, Any], 
                filename: str = None,
                directory: str = 'results') -> str:
    """Save analysis results to JSON file."""
    if filename is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'analysis_results_{timestamp}.json'
    
    # Create directory if it doesn't exist
    Path(directory).mkdir(parents=True, exist_ok=True)
    
    filepath = Path(directory) / filename
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=4, default=str)
    
    return str(filepath)

def format_currency(amount: float) -> str:
    """Format amount as currency string."""
    return f"${amount:,.2f}"

def format_percentage(value: float) -> str:
    """Format value as percentage string."""
    return f"{value:.2f}%"