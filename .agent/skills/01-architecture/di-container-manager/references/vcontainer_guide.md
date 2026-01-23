# VContainer & OOP Best Practices

## Why Dependency Injection (DI)?
- **Decoupling**: Classes don't need to know *how* to create their dependencies.
- **Testing**: We can easily swap real services for Mock services in tests.
- **No Singletons**: Avoid `public static instance`. It makes spaghetti code.

## Quick Start
1.  **Define Interface**: `public interface IAudioService { void PlaySfx(); }`
2.  **Implement**: `public class AudioService : IAudioService { ... }`
3.  **Register (LifetimeScope)**: 
    ```csharp
    builder.Register<AudioService>(Lifetime.Singleton).As<IAudioService>();
    ```
4.  **Inject**:
    ```csharp
    public class HeroController : MonoBehaviour
    {
        private IAudioService _audio;

        [Inject]
        public void Construct(IAudioService audio) 
        {
            _audio = audio;
        }
    }
    ```

## Lifetimes
- **Singleton**: One instance for the whole game. (e.g., Audio, Network).
- **Scoped**: One instance per Scene/Scope. (e.g., LevelManager).
- **Transient**: New instance every time it's asked for. (e.g., UI Popups).

## Rules
- **Pure C# Prefered**: Try to make your Services plain classes, not MonoBehaviours.
- **EntryPoints**: Use `IStartable` / `ITickable` interfaces instead of `Start()` / `Update()` inside services.
