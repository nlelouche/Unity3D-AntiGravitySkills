---
name: gpu-instancing-expert
description: "Implements GPU instancing and indirect rendering to render thousands of identical meshes in a single draw call. Covers DrawMeshInstanced, DrawMeshInstancedIndirect, and MaterialPropertyBlock."
version: 2.0.0
tags: ["performance", "gpu", "instancing", "rendering", "optimization", "draw-calls"]
argument-hint: "technique='DrawMeshInstanced|Indirect' mesh='Tree' count='5000'"
tier: 2
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies: []
context_discovery:
  check_unity_version: true
  check_render_pipeline: true
  scan_manifest_for: []
performance_budget:
  gc_alloc_per_frame: "0 bytes (indirect uses compute buffers)"
  max_update_cost: "O(1) draw calls regardless of instance count"
tdd_first: true  # ⚠️ Updated by audit v2.0.1 - needs manual test implementation
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - write_to_file
---

# GPU Instancing Expert

## Overview
GPU Instancing collapses thousands of draw calls for identical meshes into **one** GPU draw call. Per-instance data (position, color, scale) is uploaded as a bulk buffer. Unity provides three escalating techniques: **instanced materials** (automatic), **DrawMeshInstanced** (managed code), and **DrawMeshInstancedIndirect** (full GPU control via ComputeShader).

## When to Use
- Use for forests, grass, crowds, projectiles, or any scene with >100 identical meshes.
- Use when Unity Profiler shows a high **SetPass** or **Draw Call** count.
- ❌ Do NOT use for animated Skinned Mesh Renderers (use GPU skinning or DOTS instead).
- ❌ Do NOT use if each object needs a unique mesh — instancing requires the same mesh.

## Technique Selection

| Technique | Max Instances | CPU Overhead | Use Case |
|-----------|:---:|:---|:---|
| Instanced Material (auto) | 511 | Low | Automatic, enable via Material Inspector |
| `DrawMeshInstanced` | 1023/call | Medium | Managed arrays, position-only variation |
| `DrawMeshInstancedIndirect` | Millions | Near-zero | Compute-driven, full GPU control |

## Architecture

```
CPU SIDE                          GPU SIDE
┌──────────────────────┐          ┌───────────────────────────┐
│ InstanceRenderer.cs  │─Buffer──▶│ Shader (instancing on)    │
│  ComputeBuffer       │          │  UNITY_INSTANCING_BUFFER  │
│  (Matrix4x4[])       │          │  _Color, _Position, etc.  │
│  MaterialPropertyBlk │          └───────────────────────────┘
└──────────────────────┘
    ↑ Updated once per frame max
```

## DrawMeshInstanced (≤1023 instances)

```csharp
using UnityEngine;

public class InstanceRenderer : MonoBehaviour
{
    [SerializeField] private Mesh     _mesh;
    [SerializeField] private Material _material; // GPU Instancing must be enabled in material
    [SerializeField] private int      _count = 500;

    private Matrix4x4[]          _matrices;
    private MaterialPropertyBlock _props;

    private void Awake()
    {
        _matrices = new Matrix4x4[_count];
        _props    = new MaterialPropertyBlock();
        var colors = new Vector4[_count];

        for (int i = 0; i < _count; i++)
        {
            var pos = new Vector3(Random.Range(-50f, 50f), 0f, Random.Range(-50f, 50f));
            _matrices[i] = Matrix4x4.TRS(pos, Quaternion.identity, Vector3.one);
            colors[i]    = new Vector4(Random.value, Random.value, Random.value, 1f);
        }
        _props.SetVectorArray("_BaseColor", colors);
    }

    private void Update()
    {
        // Single draw call for all instances — no per-object overhead
        Graphics.DrawMeshInstanced(_mesh, 0, _material, _matrices, _count, _props);
    }
}
```

## DrawMeshInstancedIndirect (millions of instances)

```csharp
using UnityEngine;

public class IndirectInstanceRenderer : MonoBehaviour
{
    [SerializeField] private Mesh     _mesh;
    [SerializeField] private Material _material;
    [SerializeField] private int      _count = 100000;

    private ComputeBuffer _argsBuffer;
    private ComputeBuffer _positionBuffer;

    private void Awake()
    {
        // Indirect args: index count, instance count, start index, base vertex, start instance
        var args = new uint[] { _mesh.GetIndexCount(0), (uint)_count, 0, 0, 0 };
        _argsBuffer = new ComputeBuffer(1, args.Length * sizeof(uint),
            ComputeBufferType.IndirectArguments);
        _argsBuffer.SetData(args);

        // Position buffer (populated by ComputeShader or CPU)
        _positionBuffer = new ComputeBuffer(_count, sizeof(float) * 3);
        var positions = new Vector3[_count];
        for (int i = 0; i < _count; i++)
            positions[i] = new Vector3(Random.Range(-200f, 200f), 0f, Random.Range(-200f, 200f));
        _positionBuffer.SetData(positions);
        _material.SetBuffer("_Positions", _positionBuffer);
    }

    private void Update()
    {
        Graphics.DrawMeshInstancedIndirect(_mesh, 0, _material,
            new Bounds(Vector3.zero, new Vector3(500f, 10f, 500f)), _argsBuffer);
    }

    private void OnDestroy()
    {
        _argsBuffer?.Release();
        _positionBuffer?.Release();
    }
}
```

## Shader Setup (URP)

```hlsl
// In HLSL shader — enable instancing:
#pragma instancing_options procedural:setup
#pragma multi_compile_instancing

StructuredBuffer<float3> _Positions; // for Indirect
uint unity_InstanceID;

void setup() {
    unity_ObjectToWorld = float4x4(
        1,0,0,_Positions[unity_InstanceID].x,
        0,1,0,_Positions[unity_InstanceID].y,
        0,0,1,_Positions[unity_InstanceID].z,
        0,0,0,1
    );
}
```

## Best Practices

- ✅ Enable "Enable GPU Instancing" on the Material in the Inspector.
- ✅ Use `MaterialPropertyBlock` to vary properties without creating new Material instances.
- ✅ Use `DrawMeshInstancedIndirect` when count > 1023 or driven by ComputeShader.
- ✅ Dispose `ComputeBuffer` in `OnDestroy()` — unmanaged GPU memory.
- ❌ **NEVER** call `DrawMeshInstanced` with > 1023 — it silently clips.
- ❌ **NEVER** create a new Material per instance — defeats the purpose.

## Performance Notes

| Scenario | Draw Calls | FPS Impact |
|----------|:---:|:---|
| 5000 trees, no instancing | 5000 | Severe |
| 5000 trees, DrawMeshInstanced | ~5 batches | Minimal |
| 100k grass, Indirect | 1 | Near zero |



---

## TDD Contract

> ⚠️ **Legacy Skill — Refactor Pending**
> Este skill NO tiene tests automatizados aún. El siguiente boilerplate es un punto de partida.

```csharp
// Escribe estos tests ANTES de implementar:

// Test 1: should [expected behavior] when [condition]
[Test]
public void GpuInstancingExpert_Should{ExpectedBehavior}_When{Condition}()
{{
    // Arrange
    // TODO: Setup test fixtures
    
    // Act
    // TODO: Execute system under test
    
    // Assert
    Assert.Fail("Not implemented — write test first");
}}

// Test 2: should handle [edge case]
[Test]
public void GpuInstancingExpert_ShouldHandle{EdgeCase}()
{{
    // Arrange
    // TODO: Setup edge case scenario
    
    // Act
    // TODO: Execute
    
    // Assert
    Assert.Fail("Not implemented");
}}

// Test 3: should throw when [invalid input]
[Test]
public void GpuInstancingExpert_ShouldThrow_When{InvalidInput}()
{{
    // Arrange
    var invalidInput = default;
    
    // Act & Assert
    Assert.Throws<Exception>(() => {{ /* execute */ }});
}}
```

### Pasos para completar el TDD:

1. **Descomenta** los tests above
2. **Implementa** la funcionalidad mínima para que compile
3. **Ejecuta** los tests — deben fallar (RED)
4. **Implementa** la funcionalidad real
5. **Verifica** que los tests pasen (GREEN)
6. **Refactorea** manteniendo los tests verdes

---

**Nota**: Este skill fue marcado como `tdd_first: false` durante la auditoría v2.0.1. La sección TDD fue agregada automáticamente pero requiere customización manual para reflejar el comportamiento real del skill.


## Related Skills

- `@lod-occlusion-culling` — Combine with instancing for maximum throughput
- `@shader-graph-expert` — Create instancing-compatible Shader Graph shaders
- `@job-system-burst` — Use Jobs to populate transform buffers
