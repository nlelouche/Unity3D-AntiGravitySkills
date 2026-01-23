import argparse
import sys
import os
import shutil

def main():
    parser = argparse.ArgumentParser(description="Style Guide Enforcer")
    parser.add_argument("--action", choices=["install", "check"], default="install")
    parser.add_argument("--project_root", default=".", help="Unity Project Root")
    args = parser.parse_args()

    project_root = os.path.abspath(args.project_root)
    template_path = os.path.join(os.path.dirname(__file__), "..", "templates", "editorconfig.txt")
    target_path = os.path.join(project_root, ".editorconfig")

    if args.action == "install":
        print(f"Installing .editorconfig to {project_root}...")
        try:
            shutil.copy(template_path, target_path)
            print("Success: Style guide installed.")
        except Exception as e:
            print(f"Error installing style guide: {e}")
            return 1

    elif args.action == "check":
        if os.path.exists(target_path):
            print("Style Guide is present.")
        else:
            print("Warning: No .editorconfig found in project root.")
            print("Run with --action install to fix.")
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
