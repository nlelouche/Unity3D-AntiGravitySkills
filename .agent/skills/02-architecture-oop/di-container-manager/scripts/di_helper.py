import argparse
import sys
import os
import re

def analyze_dependencies(project_root):
    """
    Scans scripts for 'IService' or 'Manager' naming conventions 
    and suggests registration in a LifetimeScope.
    """
    # This is a simplified static analysis. 
    # In a real agent workflow, we might use a deeper parser or the LSP.
    
    installers_needed = []
    
    # Walk through the scripts
    for root, dirs, files in os.walk(project_root):
        for file in files:
            if file.endswith(".cs"):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Heuristic: If it implements an interface and has "Service" or "Manager" in name
                if "interface I" in content:
                    continue # It's an interface definition
                
                # Check dependency injection attributes (Inject)
                if "[Inject]" in content:
                    # This class NEEDS dependencies. Ensure it's registered?
                    pass

                # Check if it looks like a Service implementation
                # class AudioService : IAudioService
                match = re.search(r'class\s+(\w+)\s*:\s*(I\w+)', content)
                if match:
                    class_name = match.group(1)
                    interface_name = match.group(2)
                    
                    if "Service" in class_name or "Manager" in class_name:
                        installers_needed.append({
                            "class": class_name,
                            "interface": interface_name,
                            "lifetime": "Singleton" # Default assumption
                        })

    return installers_needed

def generate_installer(services, output_path):
    """
    Generates a VContainer GameLifetimeScope.
    """
    lines = []
    lines.append("using VContainer;")
    lines.append("using VContainer.Unity;")
    lines.append("using UnityEngine;")
    lines.append("")
    lines.append("public class GameLifetimeScope : LifetimeScope")
    lines.append("{")
    lines.append("    protected override void Configure(IContainerBuilder builder)")
    lines.append("    {")
    
    for svc in services:
        lines.append(f"        // Registered {svc['class']}")
        lines.append(f"        builder.Register<{svc['class']}>(Lifetime.{svc['lifetime']}).As<{svc['interface']}>();")
    
    lines.append("    }")
    lines.append("}")
    
    with open(output_path, 'w') as f:
        f.write("\n".join(lines))

def main():
    parser = argparse.ArgumentParser(description="DI Container Helper")
    parser.add_argument("--action", choices=["analyze", "generate"], default="analyze")
    parser.add_argument("--output", default="Assets/Scripts/GameLifetimeScope.cs")
    args = parser.parse_args()

    if args.action == "analyze":
        # Just scan and print suggestions
        services = analyze_dependencies("Assets/Scripts")
        print(f"Found {len(services)} potential services to register:")
        for s in services:
            print(f" - {s['class']} (as {s['interface']})")
            
    elif args.action == "generate":
        # Generate the file
        services = analyze_dependencies("Assets/Scripts")
        generate_installer(services, args.output)
        print(f"Generated Installer at {args.output}")

if __name__ == "__main__":
    sys.exit(main())
