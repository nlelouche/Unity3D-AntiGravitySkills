# C# Coding Standards

## 1. Naming Conventions

| Item | Rule | Example |
|------|------|---------|
| **Classes** | PascalCase | `PlayerController` |
| **Methods** | PascalCase | `CalculateDamage` |
| **Public Fields** | PascalCase | `MaxHealth` |
| **Properties** | PascalCase | `CurrentHealth` |
| **Private Fields** | _camelCase | `_currentHealth` |
| **Parameters** | camelCase | `damageAmount` |
| **Local Vars** | camelCase | `tempIndex` |
| **Interfaces** | I + PascalCase | `IDamageable` |
| **Enums** | PascalCase | `GameState` |

## 2. Formatting (Allman Style)

Braces should always be on a new line.

```csharp
// Correct
if (isValid)
{
    DoSomething();
}

// Incorrect
if (isValid) {
    DoSomething();
}
```

## 3. Unity Specifics

### Serialization
Avoid `public` fields for Inspector exposure. Use `[SerializeField] private` to maintain encapsulation.

```csharp
// Correct
[SerializeField] private GameObject _prefab;

// Incorrect
public GameObject prefab;
```

### Components
Use `RequireComponent` dependency injection where possible.

```csharp
[RequireComponent(typeof(Rigidbody))]
public class PlayerMovement : MonoBehaviour { ... }
```

### Magic Strings/Numbers
Avoid magic values. Use constants or ScriptableObjects.

```csharp
// Correct
private const string PLAYER_TAG = "Player";

// Incorrect
if (tag == "Player") ...
```

## 4. Architecture

### Namespaces
All code must belong to a namespace relative to the feature.
`YourGame.Feature.SubFeature`

Example: `KingdomBuilder.City.Buildings`

### Regions
Use regions sparingly. Preferred for grouping Interface implementations.

```csharp
#region IDamageable
public void TakeDamage(int amount) { ... }
#endregion
```

### Optimization
- Cache `transform` or components in `Awake` if accessed frequently.
- Use `CompareTag("Tag")` instead of `tag == "Tag"`.
- Avoid LINQ in `Update()` loops.
