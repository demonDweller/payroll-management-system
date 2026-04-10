# Employee Shift & Payroll Management System

A professional, industry-level CLI-based employee management and payroll processing system built with pure Python, demonstrating advanced Object-Oriented Programming principles.

## 📋 Overview

This system solves real-world problems for small businesses (retail stores, restaurants, warehouses) requiring:
- Employee attendance and working hour tracking
- Payroll calculation with overtime rules
- Payroll report generation
- Data management without external databases or internet

**Key Achievement:** Built entirely with Python's standard library - no external frameworks, libraries, APIs, or databases.

## ✨ Features

### Core Features
- **Employee Management** - Add, update, delete, and list employees
- **Role-based Pay** - Different hourly rates for different roles (Manager, Cashier, Cleaner, Stocker)
- **Clock In/Out System** - Track work shifts with validation
- **Overtime Calculation** - 1.5x pay after 40 hours per week
- **Payroll Processing** - Weekly payroll with tax deductions (20%)
- **Attendance Reports** - View hours worked summary
- **Data Persistence** - All data saved to CSV/JSON files

### Advanced Features
- Prevents double clock-in/out
- Automatic shift duration calculation
- Active employee tracking
- Comprehensive error handling
- Modular, production-ready code structure

## 🛠 Technology Stack

**Pure Python 3.8+** using only standard libraries:
- `csv` - Employee data storage
- `json` - Shift data storage  
- `datetime` - Time calculations
- `os` - File system operations
- `abc` - Abstract base classes
- `sys` - System operations

**No external dependencies!** Runs on any machine with Python 3.8+.

## 🏗 System Architecture

### Class Hierarchy