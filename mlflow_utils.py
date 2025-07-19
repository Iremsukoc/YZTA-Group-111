import mlflow
import mlflow.pytorch
import yaml
import argparse
import os
from typing import Dict, Any, List
import pandas as pd
import matplotlib.pyplot as plt

def load_model_from_run(run_id: str, model_name: str = "best_model") -> Any:
    """Load a model from a specific MLflow run"""
    try:
        model = mlflow.pytorch.load_model(f"runs:/{run_id}/{model_name}")
        print(f"Successfully loaded model from run {run_id}")
        return model
    except Exception as e:
        print(f"Error loading model from run {run_id}: {e}")
        return None

def load_model_from_registry(model_name: str, version: str = "latest") -> Any:
    """Load a model from MLflow model registry"""
    try:
        model = mlflow.pytorch.load_model(f"models:/{model_name}/{version}")
        print(f"Successfully loaded model {model_name} version {version}")
        return model
    except Exception as e:
        print(f"Error loading model from registry: {e}")
        return None

def compare_experiments(experiment_name: str, metric: str = "val_accuracy") -> pd.DataFrame:
    """Compare different runs in an experiment"""
    client = mlflow.tracking.MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)
    
    if experiment is None:
        print(f"Experiment '{experiment_name}' not found")
        return pd.DataFrame()
    
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=[f"metrics.{metric} DESC"]
    )
    
    results = []
    for run in runs:
        run_data = {
            "run_id": run.info.run_id,
            "status": run.info.status,
            "start_time": run.info.start_time,
            **run.data.params,
            **run.data.metrics
        }
        results.append(run_data)
    
    df = pd.DataFrame(results)
    if not df.empty:
        print(f"Found {len(df)} runs in experiment '{experiment_name}'")
        print(f"Best {metric}: {df[metric].max():.4f}")
    
    return df

def plot_metrics_comparison(experiment_name: str, metrics: List[str] = None):
    """Plot comparison of metrics across runs"""
    if metrics is None:
        metrics = ["val_accuracy", "val_auc", "train_accuracy"]
    
    df = compare_experiments(experiment_name)
    if df.empty:
        return
    
    fig, axes = plt.subplots(1, len(metrics), figsize=(5*len(metrics), 5))
    if len(metrics) == 1:
        axes = [axes]
    
    for i, metric in enumerate(metrics):
        if metric in df.columns:
            df[metric].plot(kind='bar', ax=axes[i], title=f"{metric} by Run")
            axes[i].set_xlabel("Run Index")
            axes[i].set_ylabel(metric)
            axes[i].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(f"results/{experiment_name}_metrics_comparison.png")
    plt.show()

def list_experiments():
    """List all experiments"""
    client = mlflow.tracking.MlflowClient()
    experiments = client.list_experiments()
    
    print("Available experiments:")
    for exp in experiments:
        print(f"  - {exp.name} (ID: {exp.experiment_id})")

def list_runs(experiment_name: str):
    """List all runs in an experiment"""
    client = mlflow.tracking.MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)
    
    if experiment is None:
        print(f"Experiment '{experiment_name}' not found")
        return
    
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["start_time DESC"]
    )
    
    print(f"Runs in experiment '{experiment_name}':")
    for run in runs:
        print(f"  - Run ID: {run.info.run_id}")
        print(f"    Status: {run.info.status}")
        print(f"    Start Time: {run.info.start_time}")
        if "val_accuracy" in run.data.metrics:
            print(f"    Best Val Accuracy: {run.data.metrics['val_accuracy']:.4f}")
        print()

def setup_mlflow_from_config(config_path: str):
    """Setup MLflow from config file"""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    mlflow_config = config.get('mlflow', {})
    
    if 'tracking_uri' in mlflow_config:
        mlflow.set_tracking_uri(mlflow_config['tracking_uri'])
    
    experiment_name = mlflow_config.get('experiment_name', 'skin_cancer_classification')
    mlflow.set_experiment(experiment_name)
    
    return mlflow_config

def main():
    parser = argparse.ArgumentParser(description='MLflow utilities for skin cancer classification')
    parser.add_argument('--config', type=str, default='configs/config.yaml', help='Path to config file')
    parser.add_argument('--action', type=str, required=True, 
                       choices=['list_experiments', 'list_runs', 'compare', 'load_model', 'plot'],
                       help='Action to perform')
    parser.add_argument('--experiment', type=str, help='Experiment name')
    parser.add_argument('--run_id', type=str, help='Run ID for loading model')
    parser.add_argument('--model_name', type=str, default='best_model', help='Model name in run')
    
    args = parser.parse_args()
    
    # Setup MLflow
    setup_mlflow_from_config(args.config)
    
    if args.action == 'list_experiments':
        list_experiments()
    
    elif args.action == 'list_runs':
        if not args.experiment:
            print("Please provide --experiment name")
            return
        list_runs(args.experiment)
    
    elif args.action == 'compare':
        if not args.experiment:
            print("Please provide --experiment name")
            return
        df = compare_experiments(args.experiment)
        if not df.empty:
            print(df.to_string())
    
    elif args.action == 'load_model':
        if not args.run_id:
            print("Please provide --run_id")
            return
        model = load_model_from_run(args.run_id, args.model_name)
        if model:
            print("Model loaded successfully")
    
    elif args.action == 'plot':
        if not args.experiment:
            print("Please provide --experiment name")
            return
        plot_metrics_comparison(args.experiment)

if __name__ == "__main__":
    main() 