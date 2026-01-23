#!/usr/bin/env python3
"""
Async Utilities Generator
Generates async helper components for Unity projects.

Usage:
  python async_gen.py --component loader --namespace Game.Async
  python async_gen.py --component monobehaviour --namespace Game.Core --name NetworkManager
"""

import argparse
from pathlib import Path


COMPONENT_TYPES = {
    'loader': 'AsyncLoader',
    'monobehaviour': 'AsyncMonoBehaviour',
    'operation': 'AsyncOperation',
}


def generate_async_monobehaviour(name: str, namespace: str, output_dir: Path):
    """Generate a custom AsyncMonoBehaviour subclass."""
    content = f'''using System.Threading;
using System.Threading.Tasks;
using UnityEngine;

namespace {namespace}
{{
    /// <summary>
    /// {name} with async lifecycle support.
    /// Uses DestroyCancellationToken for safe async operations.
    /// </summary>
    public class {name} : AsyncMonoBehaviour
    {{
        protected override void Awake()
        {{
            base.Awake();
            // Initialize your manager
        }}
        
        /// <summary>
        /// Example async initialization.
        /// </summary>
        public async Task InitializeAsync()
        {{
            RunAsync(async (token) =>
            {{
                // Your async logic here
                await Task.Delay(1000, token);
                Debug.Log("[{name}] Initialized");
            }});
        }}
        
        /// <summary>
        /// Example async operation with result.
        /// </summary>
        public async Task<bool> DoSomethingAsync()
        {{
            return await RunAsync(async (token) =>
            {{
                await Task.Delay(500, token);
                return true;
            }}, defaultValue: false);
        }}
    }}
}}
'''
    
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{name}.cs").write_text(content, encoding='utf-8')
    print(f"✓ Generated {name}.cs")


def main():
    parser = argparse.ArgumentParser(description='Generate async components')
    parser.add_argument('--component', '-c', choices=list(COMPONENT_TYPES.keys()),
                        help='Component type to generate')
    parser.add_argument('--name', '-n', default='CustomAsyncManager',
                        help='Class name (for monobehaviour)')
    parser.add_argument('--namespace', '-ns', default='Game.Async', help='Namespace')
    parser.add_argument('--output', '-o', default='Assets/Scripts/Async', help='Output dir')
    
    args = parser.parse_args()
    output_dir = Path(args.output)
    
    if args.component == 'monobehaviour':
        generate_async_monobehaviour(args.name, args.namespace, output_dir)
    else:
        print(f"Templates available at: templates/{COMPONENT_TYPES.get(args.component, 'AsyncOperation')}.cs.txt")
        print("Copy and customize as needed.")
    
    return 0


if __name__ == '__main__':
    exit(main())
