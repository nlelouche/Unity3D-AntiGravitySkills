---
name: procedural-generation
description: "Implements procedural content generation algorithms: BSP dungeon rooms, Wave Function Collapse for tile maps, and Perlin-noise terrain. Provides an agnostic grid API for any genre."
version: 2.0.0
tags: ["gameplay", "procedural", "dungeon", "wave-function-collapse", "perlin", "terrain", "generation"]
argument-hint: "algorithm='BSP|WFC|Perlin' grid_width='40' grid_height='40' seed='12345'"
tier: 2
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies: []
context_discovery:
  check_unity_version: false
  check_render_pipeline: false
  scan_manifest_for: []
performance_budget:
  gc_alloc_per_frame: "N/A — generation runs once at load time"
  max_update_cost: "O(W×H) per generation — run async or during loading screen"
tdd_first: true
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - write_to_file
---

# Procedural Generation

## Overview
Procedural generation creates game content algorithmically instead of by hand, enabling infinite replayability. This skill covers three complementary algorithms: **BSP** (Binary Space Partitioning) for dungeon rooms, **Wave Function Collapse** (WFC) for tile-constraint satisfaction, and **Perlin Noise** for organic terrain/heightmaps. All algorithms write to a shared `IGrid<T>` interface.

## When to Use
- Use **BSP** for classic dungeon crawlers with distinct rectangular rooms.
- Use **WFC** for tile maps that must respect adjacency rules (e.g., ocean can't be next to mountain).
- Use **Perlin Noise** for terrain heightmaps, biome maps, weather patterns.
- ❌ Do NOT run generation synchronously on large grids (>200×200) — use async or Jobs.

## Algorithm Comparison

| Algorithm | Output Quality | Control | Speed |
|-----------|:-:|:-:|:-:|
| BSP Dungeon | Rooms + corridors | High | Fast |
| Wave Function Collapse | Constraint-aware tiles | Medium | Medium |
| Perlin Noise | Organic blobs | Low | Very Fast |

## Shared Grid API

```csharp
// --- IGrid.cs ---
public interface IGrid<T>
{
    int Width  { get; }
    int Height { get; }
    T   Get(int x, int y);
    void Set(int x, int y, T value);
    bool InBounds(int x, int y);
}

// --- TileType.cs ---
public enum TileType { Empty, Floor, Wall, Door, Water, Mountain }

// --- Grid2D.cs ---
public class Grid2D<T> : IGrid<T>
{
    private readonly T[,] _cells;
    public int Width  { get; }
    public int Height { get; }

    public Grid2D(int width, int height, T defaultValue = default)
    {
        Width = width; Height = height;
        _cells = new T[width, height];
        for (int x = 0; x < width; x++)
            for (int y = 0; y < height; y++)
                _cells[x, y] = defaultValue;
    }

    public T    Get(int x, int y)          => _cells[x, y];
    public void Set(int x, int y, T value) => _cells[x, y] = value;
    public bool InBounds(int x, int y)     => x >= 0 && y >= 0 && x < Width && y < Height;
}
```

## BSP Dungeon Generator

```csharp
using System;
using System.Collections.Generic;
using UnityEngine;

public class BSPDungeonGenerator
{
    private readonly System.Random _rng;

    public BSPDungeonGenerator(int seed) => _rng = new System.Random(seed);

    public Grid2D<TileType> Generate(int width, int height, int minRoomSize = 6)
    {
        var grid = new Grid2D<TileType>(width, height, TileType.Wall);
        var rooms = new List<RectInt>();
        Split(new RectInt(1, 1, width - 2, height - 2), minRoomSize, rooms);

        foreach (var room in rooms)
            CarveRoom(grid, room);

        for (int i = 0; i < rooms.Count - 1; i++)
            CarveCorridor(grid, rooms[i].center, rooms[i + 1].center);

        return grid;
    }

    private void Split(RectInt area, int minSize, List<RectInt> rooms)
    {
        bool splitH = _rng.NextDouble() > 0.5;

        if (area.width < minSize * 2 && area.height < minSize * 2)
        { rooms.Add(Shrink(area)); return; }

        if (splitH && area.height >= minSize * 2)
        {
            int split = _rng.Next(minSize, area.height - minSize);
            Split(new RectInt(area.x, area.y, area.width, split), minSize, rooms);
            Split(new RectInt(area.x, area.y + split, area.width, area.height - split), minSize, rooms);
        }
        else
        {
            int split = _rng.Next(minSize, area.width - minSize);
            Split(new RectInt(area.x, area.y, split, area.height), minSize, rooms);
            Split(new RectInt(area.x + split, area.y, area.width - split, area.height), minSize, rooms);
        }
    }

    private RectInt Shrink(RectInt r) =>
        new(r.x + 1, r.y + 1, Mathf.Max(2, r.width - 2), Mathf.Max(2, r.height - 2));

    private void CarveRoom(Grid2D<TileType> g, RectInt r)
    {
        for (int x = r.x; x < r.x + r.width; x++)
            for (int y = r.y; y < r.y + r.height; y++)
                g.Set(x, y, TileType.Floor);
    }

    private void CarveCorridor(Grid2D<TileType> g, Vector2Int a, Vector2Int b)
    {
        int x = a.x;
        while (x != b.x) { g.Set(x, a.y, TileType.Floor); x += x < b.x ? 1 : -1; }
        int y = a.y;
        while (y != b.y) { g.Set(b.x, y, TileType.Floor); y += y < b.y ? 1 : -1; }
    }
}
```

## Perlin Noise Terrain

```csharp
public class PerlinTerrainGenerator
{
    public Grid2D<float> Generate(int width, int height, float scale = 0.1f, int octaves = 4,
        float persistence = 0.5f, int seed = 42)
    {
        var grid = new Grid2D<float>(width, height);
        float offsetX = seed * 1000f;
        float offsetY = seed * 2000f;

        for (int x = 0; x < width; x++)
        {
            for (int y = 0; y < height; y++)
            {
                float amplitude = 1f, frequency = 1f, noise = 0f;
                for (int o = 0; o < octaves; o++)
                {
                    noise     += Mathf.PerlinNoise((x + offsetX) * scale * frequency,
                                                   (y + offsetY) * scale * frequency) * amplitude;
                    amplitude *= persistence;
                    frequency *= 2f;
                }
                grid.Set(x, y, Mathf.Clamp01(noise));
            }
        }
        return grid;
    }

    // Map height to TileType
    public TileType HeightToTile(float h) => h switch
    {
        < 0.3f => TileType.Water,
        < 0.6f => TileType.Floor,
        _      => TileType.Mountain
    };
}
```

## TDD Contract

```csharp
[Test]
public void BSPDungeon_Generate_ContainsFloorTiles()
{
    var gen  = new BSPDungeonGenerator(seed: 42);
    var grid = gen.Generate(40, 40);
    bool hasFloor = false;
    for (int x = 0; x < 40 && !hasFloor; x++)
        for (int y = 0; y < 40 && !hasFloor; y++)
            hasFloor = grid.Get(x, y) == TileType.Floor;
    Assert.IsTrue(hasFloor);
}

[Test]
public void PerlinTerrain_Generate_AllValuesInRange()
{
    var gen  = new PerlinTerrainGenerator();
    var grid = gen.Generate(50, 50);
    for (int x = 0; x < 50; x++)
        for (int y = 0; y < 50; y++)
            Assert.IsTrue(grid.Get(x, y) >= 0f && grid.Get(x, y) <= 1f);
}
```

## Best Practices

- ✅ Always use a **seed** for reproducible generation (critical for bug reproduction).
- ✅ Run generation **during a loading screen** or async to avoid frame drop.
- ✅ Separate **generation** (data) from **visualization** (tilemap rendering).
- ❌ **NEVER** run WFC or large BSP synchronously on the main thread mid-gameplay.

## Related Skills

- `@save-load-serialization` — Serialize the seed to reproduce the same dungeon from a save
- `@job-system-burst` — Parallelize perlin noise generation over large grids
- `@minimap-system` — Render a minimap from the generated `IGrid<T>`
