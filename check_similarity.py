import pandas as pd
import sys

def compare_csv_files(file1, file2):
    try:
        # Read both CSV files into DataFrames
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)

        # Compare DataFrames
        if df1.equals(df2):
            print("The CSV files are exactly equal.")
        else:
            print("The CSV files are NOT equal.")
    except Exception as e:
        print(f"Error reading or comparing files: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_csv.py <file1.csv> <file2.csv>")
    else:
        compare_csv_files(sys.argv[1], sys.argv[2])