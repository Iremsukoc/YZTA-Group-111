#!/usr/bin/env python3
"""
Script to start MLflow UI server
"""
import subprocess
import sys
import yaml
import os

def start_mlflow_ui():
    """Start MLflow UI server"""
    try:
        # Load config to get tracking URI
        config_path = 'configs/config.yaml'
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            tracking_uri = config.get('mlflow', {}).get('tracking_uri', 'sqlite:///mlflow.db')
            print(f"Starting MLflow UI with tracking URI: {tracking_uri}")
            
            # Start MLflow UI
            cmd = [sys.executable, "-m", "mlflow", "ui", "--backend-store-uri", tracking_uri]
            subprocess.run(cmd)
        else:
            print("Config file not found, starting MLflow UI with default settings")
            cmd = [sys.executable, "-m", "mlflow", "ui"]
            subprocess.run(cmd)
            
    except KeyboardInterrupt:
        print("\nMLflow UI stopped by user")
    except Exception as e:
        print(f"Error starting MLflow UI: {e}")

if __name__ == "__main__":
    start_mlflow_ui() 