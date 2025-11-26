#!/usr/bin/env python3
"""
MyAntFarm.ai - Multi-Agent LLM Orchestration Framework
Main entry point for Docker container execution.

This wrapper allows the container to be used either:
1. Automatically: Runs full 348-trial evaluation on startup
2. Manually: Keeps container alive for interactive execution

Usage:
    Automatic: docker-compose up -d (runs trials on startup)
    Manual: docker exec -it evaluator python src/evaluator.py --trials 348
"""

import sys
import os
import argparse
import time

# Add src to path
sys.path.insert(0, '/app/src')

def main():
    parser = argparse.ArgumentParser(description='MyAntFarm.ai Evaluator')
    parser.add_argument('--mode', choices=['auto', 'manual'], default='manual',
                       help='auto: run trials on startup, manual: keep alive for commands')
    parser.add_argument('--trials', type=int, default=348,
                       help='Number of trials to run (auto mode only)')
    parser.add_argument('--seed', type=int, default=42,
                       help='Random seed for reproducibility')
    
    args = parser.parse_args()
    
    if args.mode == 'auto':
        # Run evaluation automatically
        print(f"Starting automatic evaluation: {args.trials} trials, seed={args.seed}")
        from evaluator import run_evaluation
        run_evaluation(trials=args.trials, seed=args.seed)
        print("Evaluation complete!")
    else:
        # Manual mode: keep container alive
        print("Container started in manual mode.")
        print("Run evaluations using:")
        print("  docker exec -it evaluator python src/evaluator.py --trials 348 --seed 42")
        print("\nKeeping container alive... (Ctrl+C in docker-compose logs to stop)")
        
        # Keep alive indefinitely
        while True:
            time.sleep(3600)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nShutdown requested... exiting")
        sys.exit(0)
