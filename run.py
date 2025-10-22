#!/usr/bin/env python3
"""
University Blockchain System - Main Runner
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from blockchain.main import demo_system
from blockchain.cli import BlockchainCLI


def main():
    if len(sys.argv) > 1:
        # Run CLI mode
        cli = BlockchainCLI()
        cli.run()
    else:
        # Run demo mode
        demo_system()
        print("\n" + "="*50)
        print("Gunakan 'python run.py --help' untuk melihat command yang tersedia")


if __name__ == "__main__":
    main()