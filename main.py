#!/usr/bin/env python3
"""
Employee Shift & Payroll Management System
A CLI-based system for managing employee attendance and payroll
"""

import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli.menu import CLIMenu


def main():
    """Main entry point for the application"""
    print("\n" + "=" * 50)
    print("   WELCOME TO PAYROLL MANAGEMENT SYSTEM")
    print("=" * 50)
    print("\nLoading system...")

    try:
        menu = CLIMenu()
        menu.display_main_menu()
    except KeyboardInterrupt:
        print("\n\n⚠️  System interrupted by user")
        print("Saving data before exit...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print("Please check data files and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()