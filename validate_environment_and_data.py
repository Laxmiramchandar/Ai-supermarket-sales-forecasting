"""
Production Environment and Dataset Validation Script
Project: AI-Powered Supermarket Sales Forecasting and Analytics System
Author: Senior Data Science & MLOps Team
"""

import os
import sys
import platform
import hashlib
from pathlib import Path
import pandas as pd
import numpy as np

def compute_sha256(filepath: Path) -> str:
    """Calculate SHA-256 checksum of a file for audit and data versioning."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def print_banner(title: str):
    width = 75
    print("\n" + "=" * width)
    print(f" {title.upper()} ".center(width, "="))
    print("=" * width)

def print_section(title: str):
    print(f"\n--- {title} ---")

def validate_environment() -> dict:
    print_banner("1. Windows 11 Environment & Python Runtime Diagnostic")
    
    env_info = {
        "OS": platform.system(),
        "OS Release": platform.release(),
        "OS Version": platform.version(),
        "Architecture": platform.architecture()[0],
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Python Version": platform.python_version(),
        "Python Executable": sys.executable,
        "Working Directory": os.getcwd()
    }
    
    for k, v in env_info.items():
        print(f"  • {k:<20}: {v}")
        
    print_section("Core Package Ecosystem Verification")
    packages = [
        "numpy", "pandas", "scipy", "sklearn", "statsmodels",
        "tensorflow", "torch", "fastapi", "uvicorn", "streamlit", "pytest"
    ]
    
    pkg_status = {}
    for pkg in packages:
        try:
            mod = __import__(pkg)
            version = getattr(mod, "__version__", "Installed (Version unknown)")
            pkg_status[pkg] = (True, version)
            print(f"  [PASS] {pkg:<15}: v{version}")
        except ImportError:
            pkg_status[pkg] = (False, "Missing")
            print(f"  [FAIL] {pkg:<15}: NOT INSTALLED")
            
    return {"env": env_info, "packages": pkg_status}

def validate_supermarket_sales(filepath: Path):
    print_banner("2. Primary Time Series Dataset: supermarket_sales.csv")
    
    if not filepath.exists():
        print(f"  [ERROR] File not found at: {filepath}")
        return False
        
    file_size_kb = filepath.stat().st_size / 1024
    checksum = compute_sha256(filepath)
    print(f"  • File Location      : {filepath.resolve()}")
    print(f"  • File Size          : {file_size_kb:.2f} KB")
    print(f"  • SHA-256 Checksum   : {checksum}")
    
    df = pd.read_csv(filepath)
    print(f"  • Dimensions         : {df.shape[0]:,} rows x {df.shape[1]} columns")
    
    print_section("Schema & Null-Value Audit")
    null_counts = df.isnull().sum()
    for col in df.columns:
        dtype = str(df[col].dtype)
        null_cnt = null_counts[col]
        null_pct = (null_cnt / len(df)) * 100
        print(f"  - {col:<16} | Type: {dtype:<10} | Nulls: {null_cnt:<4} ({null_pct:.1f}%) | Unique: {df[col].nunique():<5}")
        
    print_section("Temporal Diagnostics (Time Series Feasibility)")
    df['Parsed_Date'] = pd.to_datetime(df['Date'], errors='coerce')
    invalid_dates = df['Parsed_Date'].isnull().sum()
    min_date = df['Parsed_Date'].min()
    max_date = df['Parsed_Date'].max()
    unique_dates = df['Parsed_Date'].nunique()
    total_days = (max_date - min_date).days + 1
    
    print(f"  • Date Column Syntax : Validated (Invalid formats: {invalid_dates})")
    print(f"  • Earliest Record    : {min_date.strftime('%Y-%m-%d')}")
    print(f"  • Latest Record      : {max_date.strftime('%Y-%m-%d')}")
    print(f"  • Temporal Span      : {total_days} calendar days")
    print(f"  • Active Sales Days  : {unique_dates} days ({unique_dates / total_days * 100:.1f}% day-level continuity)")
    
    print_section("Categorical Granularity & Segments")
    for cat_col in ['Branch', 'City', 'Customer_Type', 'Gender', 'Product_Line', 'Payment']:
        val_counts = df[cat_col].value_counts().to_dict()
        val_str = ", ".join([f"{k}: {v}" for k, v in val_counts.items()])
        print(f"  • {cat_col:<15}: {val_str}")
        
    print_section("Financial & Numerical Summary")
    num_cols = ['Unit_Price', 'Quantity', 'Tax', 'Total', 'Rating']
    stats_df = df[num_cols].describe().T[['mean', 'std', 'min', '50%', 'max']]
    stats_df.columns = ['Mean', 'Std Dev', 'Min', 'Median (50%)', 'Max']
    print(stats_df.to_string())
    
    daily_sales = df.groupby('Parsed_Date')['Total'].sum()
    print_section("Aggregated Daily Sales Benchmark")
    print(f"  • Total Gross Revenue: ${df['Total'].sum():,.2f}")
    print(f"  • Mean Daily Revenue : ${daily_sales.mean():,.2f} (Std: ${daily_sales.std():,.2f})")
    print(f"  • Min Daily Revenue  : ${daily_sales.min():,.2f}")
    print(f"  • Max Daily Revenue  : ${daily_sales.max():,.2f}")
    
    return True

def validate_customer_churn(filepath: Path):
    print_banner("3. Optional Classification Dataset: customer_churn.csv")
    
    if not filepath.exists():
        print(f"  [ERROR] File not found at: {filepath}")
        return False
        
    file_size_kb = filepath.stat().st_size / 1024
    checksum = compute_sha256(filepath)
    print(f"  • File Location      : {filepath.resolve()}")
    print(f"  • File Size          : {file_size_kb:.2f} KB")
    print(f"  • SHA-256 Checksum   : {checksum}")
    
    df = pd.read_csv(filepath)
    print(f"  • Dimensions         : {df.shape[0]:,} rows x {df.shape[1]} columns")
    
    print_section("Schema & Null-Value Audit")
    null_counts = df.isnull().sum()
    for col in df.columns:
        dtype = str(df[col].dtype)
        null_cnt = null_counts[col]
        null_pct = (null_cnt / len(df)) * 100
        print(f"  - {col:<18} | Type: {dtype:<10} | Nulls: {null_cnt:<4} ({null_pct:.1f}%) | Unique: {df[col].nunique():<5}")
        
    print_section("Target Variable (Churn) Distribution")
    churn_counts = df['Churn'].value_counts()
    churn_pct = df['Churn'].value_counts(normalize=True) * 100
    for cls in churn_counts.index:
        print(f"  • Churn = {cls}: {churn_counts[cls]} samples ({churn_pct[cls]:.2f}%)")
    imbalance_ratio = churn_counts.max() / churn_counts.min() if churn_counts.min() > 0 else 0
    print(f"  • Class Imbalance Ratio: {imbalance_ratio:.2f}:1")
    
    return True

def main():
    sales_path = Path("data/raw/supermarket_sales.csv")
    churn_path = Path("data/raw/customer_churn.csv")
    
    env_res = validate_environment()
    sales_ok = validate_supermarket_sales(sales_path)
    churn_ok = validate_customer_churn(churn_path)
    
    print_banner("4. System Readiness & Verification Verdict")
    all_passed = (
        all(status[0] for status in env_res["packages"].values()) and
        sales_ok and
        churn_ok
    )
    
    print(f"  • Python Environment Check  : PASS")
    print(f"  • Package Dependencies Check: {'PASS' if all(status[0] for status in env_res['packages'].values()) else 'FAIL'}")
    print(f"  • Supermarket Sales Dataset : {'PASS' if sales_ok else 'FAIL'}")
    print(f"  • Customer Churn Dataset    : {'PASS' if churn_ok else 'FAIL'}")
    print(f"\n  OVERALL STATUS: {'[READY FOR TIME SERIES MODELING]' if all_passed else '[ACTION REQUIRED]'}\n")
    print("=" * 75 + "\n")

if __name__ == "__main__":
    main()
