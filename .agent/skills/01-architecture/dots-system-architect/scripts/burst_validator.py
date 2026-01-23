import argparse
import sys
import re

def validate_burst_compatibility(file_path):
    """
    Scans a C# file to ensure it adheres to basic Burst Compiler constraints.
    """
    with open(file_path, 'r') as f:
        content = f.read()

    errors = []

    # 1. Check for [BurstCompile]
    if "[BurstCompile]" not in content:
        errors.append("Missing '[BurstCompile]' attribute. Burst optimization is required.")

    # 2. Check for Managed Types (simplified check)
    # This is a heuristic. A real parser would need semantic analysis.
    # We check for common forbidden keywords in fields if it's a struct.
    if "string " in content and "FixedString" not in content:
        errors.append("Detected 'string' usage. Use 'FixedString32Bytes' (or similar) for Burst compatibility.")

    # 3. Check for ISystem struct keyword
    if ": ISystem" in content and "struct " not in content:
        errors.append("ISystem must be implemented as a 'struct', not a 'class'.")

    return errors

def main():
    parser = argparse.ArgumentParser(description="Validates C# code for Unity Burst compatibility.")
    parser.add_argument("--file", help="Path to the C# file to validate", required=True)
    args = parser.parse_args()

    print(f"Validating {args.file} for Burst Compatibility...")
    
    try:
        errors = validate_burst_compatibility(args.file)
        if errors:
            print("Validation FAILED:")
            for e in errors:
                print(f"- {e}")
            return 1
        else:
            print("Validation PASSED: Code looks Burst-compatible.")
            return 0
    except FileNotFoundError:
        print(f"Error: File {args.file} not found.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
