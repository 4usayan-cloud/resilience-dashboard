#!/usr/bin/env python3
import pandas as pd

print("Inspecting INFORM Risk Excel file...\n")

# Read all sheets
excel_file = pd.ExcelFile('/Users/sayansen/Desktop/INFORM_Risk_Mid_2025_v071.xlsx')
print(f"Available sheets: {excel_file.sheet_names}\n")

# Read first sheet
for sheet_name in excel_file.sheet_names[:3]:  # Check first 3 sheets
    print(f"\n{'='*60}")
    print(f"Sheet: {sheet_name}")
    print(f"{'='*60}")
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    print(f"Shape: {df.shape} (rows, columns)")
    print(f"\nColumns:\n{df.columns.tolist()}")
    print(f"\nFirst few rows:")
    print(df.head(3))
    print(f"\nSample data types:\n{df.dtypes[:10]}")
