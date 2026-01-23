import argparse
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="Best practices for UGUI optimization (Split Canvases, Raycast Target).")
    parser.add_argument("--example_arg", help="An example argument", required=False)
    args = parser.parse_args()

    # Logic goes here
    print(f"Running skill 'canvas-performance'...")
    print(f"Example arg received: {args.example_arg}")

    # TODO: Implement core logic
    
    # Return 0 for success
    return 0

if __name__ == "__main__":
    sys.exit(main())
