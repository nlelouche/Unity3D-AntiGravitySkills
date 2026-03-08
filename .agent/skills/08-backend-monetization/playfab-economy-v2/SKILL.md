---
name: playfab-economy-v2
description: "Full integration guide for PlayFab Economy v2: Catalogs, Inventory, Virtual Currencies, Stores, and Transactions. Replaces deprecated Economy v1 patterns."
version: 2.0.0
tags: ["backend", "playfab", "economy", "iap", "inventory", "virtual-currency", "monetization"]
argument-hint: "action='setup' OR action='purchase' item='sword_001' OR action='grant-currency' amount='100'"
tier: 2
requirements:
  unity_version: ">=6.0"
  render_pipeline: "Any"
  dependencies:
    - "com.playfab.unitysdk"
context_discovery:
  check_unity_version: true
  check_render_pipeline: false
  scan_manifest_for:
    - "com.playfab.unitysdk"
performance_budget:
  gc_alloc_per_frame: "N/A — async network calls only"
  max_update_cost: "N/A — event-driven"
tdd_first: true
disable-model-invocation: false
user-invocable: true
allowed-tools:
  - run_command
  - list_dir
  - write_to_file
---

# PlayFab Economy v2

## Overview
PlayFab Economy v2 is Microsoft's production-grade backend for game economies. It replaces the deprecated v1 `CatalogItems` / `PlayerInventory` API with a **unified, transactional** system using `Catalogs`, `InventoryItems`, and `StackableInventory`. This skill covers the full setup-to-purchase lifecycle for Unity.

> [!IMPORTANT]
> Economy v1 (`GetCatalogItems`, `PurchaseItem`, `GetUserInventory`) is **deprecated** as of 2024. All new projects must use Economy v2 APIs.

## When to Use
- Use for **virtual currency** systems (Gold, Gems, Energy).
- Use for **item catalogs** (weapons, skins, consumables).
- Use for **store fronts** (daily shop, IAP bundles).
- Use for **player inventory** management across sessions.
- ❌ Do NOT use for real-money IAP receipt validation alone — combine with `@monetization-iap`.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 PLAYFAB ECONOMY v2 FLOW                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  GAME CLIENT              PLAYFAB BACKEND                   │
│  ┌─────────────┐          ┌──────────────────────────────┐  │
│  │PlayFabEcon  │──Auth───▶│ Auth Service                 │  │
│  │Service.cs   │          │ (LoginWithCustomID/DeviceID) │  │
│  │             │──Search─▶│ Economy v2 Catalog           │  │
│  │             │          │  Items: sword_001, gem_pack  │  │
│  │             │──Buy────▶│ PurchaseInventoryItems       │  │
│  │             │          │  Transaction: deduct currency│  │
│  │             │◀─Inv────│ GetInventoryItems            │  │
│  └─────────────┘          └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Setup Checklist

```
☐ 1. Create PlayFab account at playfab.com
☐ 2. Create a Title → copy TitleId
☐ 3. Install PlayFab SDK: com.playfab.unitysdk (via Package Manager)
☐ 4. Set TitleId in PlayFabSettings asset (Resources/PlayFabSharedSettings)
☐ 5. In PlayFab Dashboard:
      Economy → Catalog v2 → Create Catalog
      Add Items (virtual currency items + purchaseable items)
      Add Virtual Currencies (e.g., "GO" = Gold)
☐ 6. Implement Authentication (step below)
☐ 7. Implement Economy service (step below)
```

## Core Implementation

```csharp
// --- IPlayFabEconomyService.cs ---
using System.Collections.Generic;
using System.Threading.Tasks;

public interface IPlayFabEconomyService
{
    Task LoginAsync();
    Task<List<CatalogItemData>> GetCatalogAsync(string filter = null);
    Task<List<InventoryItemData>> GetInventoryAsync();
    Task<bool> PurchaseItemAsync(string itemId, string currencyId, int price);
    Task<int> GetCurrencyBalanceAsync(string currencyId);
}

// --- PlayFabEconomyService.cs ---
using System.Collections.Generic;
using System.Threading.Tasks;
using PlayFab;
using PlayFab.EconomyModels;
using UnityEngine;

public class PlayFabEconomyService : IPlayFabEconomyService
{
    private string _entityId;
    private string _entityType;

    public async Task LoginAsync()
    {
        var tcs = new TaskCompletionSource<bool>();

        PlayFabClientAPI.LoginWithCustomID(
            new PlayFab.ClientModels.LoginWithCustomIDRequest
            {
                CustomId        = SystemInfo.deviceUniqueIdentifier,
                CreateAccount   = true,
                TitleId         = PlayFabSettings.TitleId
            },
            result =>
            {
                _entityId   = result.EntityToken.Entity.Id;
                _entityType = result.EntityToken.Entity.Type;
                tcs.SetResult(true);
            },
            error => { Debug.LogError(error.GenerateErrorReport()); tcs.SetResult(false); }
        );

        await tcs.Task;
    }

    public async Task<bool> PurchaseItemAsync(string itemId, string currencyId, int price)
    {
        var tcs = new TaskCompletionSource<bool>();

        PlayFabEconomyAPI.PurchaseInventoryItems(
            new PurchaseInventoryItemsRequest
            {
                Amount = 1,
                Item   = new InventoryItemReference { Id = itemId },
                PriceAmounts = new List<PurchasePriceAmount>
                {
                    new() { ItemId = currencyId, Amount = price }
                }
            },
            _ => tcs.SetResult(true),
            error =>
            {
                Debug.LogError($"Purchase failed: {error.GenerateErrorReport()}");
                tcs.SetResult(false);
            }
        );

        return await tcs.Task;
    }

    public async Task<List<InventoryItemData>> GetInventoryAsync()
    {
        var tcs = new TaskCompletionSource<List<InventoryItemData>>();

        PlayFabEconomyAPI.GetInventoryItems(
            new GetInventoryItemsRequest(),
            result =>
            {
                var items = result.Items.ConvertAll(i => new InventoryItemData
                {
                    ItemId   = i.Id,
                    Quantity = (int)(i.Amount ?? 1)
                });
                tcs.SetResult(items);
            },
            error => { Debug.LogError(error.GenerateErrorReport()); tcs.SetResult(new()); }
        );

        return await tcs.Task;
    }

    // --- GetCatalogAsync and GetCurrencyBalanceAsync follow same async pattern ---
}

// --- Data Transfer Objects ---
public class CatalogItemData
{
    public string Id;
    public string DisplayName;
    public int    Price;
    public string CurrencyId;
}

public class InventoryItemData
{
    public string ItemId;
    public int    Quantity;
}
```

## TDD Contract

```csharp
// Use a mock for unit testing — no network required
public class MockPlayFabEconomyService : IPlayFabEconomyService
{
    public int GoldBalance = 500;
    public List<InventoryItemData> Inventory = new();

    public Task LoginAsync() => Task.CompletedTask;
    public Task<int> GetCurrencyBalanceAsync(string id) => Task.FromResult(GoldBalance);

    public Task<bool> PurchaseItemAsync(string itemId, string currencyId, int price)
    {
        if (GoldBalance < price) return Task.FromResult(false);
        GoldBalance -= price;
        Inventory.Add(new InventoryItemData { ItemId = itemId, Quantity = 1 });
        return Task.FromResult(true);
    }
    // ... other stubs
}

[Test]
public async Task Purchase_WhenSufficientFunds_AddsItemToInventory()
{
    var svc = new MockPlayFabEconomyService { GoldBalance = 100 };
    var result = await svc.PurchaseItemAsync("sword_001", "GO", 50);
    Assert.IsTrue(result);
    Assert.AreEqual(1, svc.Inventory.Count);
}
```

## Best Practices

- ✅ Always **login before** any Economy API call — `_entityId` is required.
- ✅ Use `IPlayFabEconomyService` everywhere — swap mock for tests.
- ✅ Display **loading state** during async calls — network latency varies.
- ✅ Handle **insufficient funds** gracefully (not as an exception).
- ❌ **NEVER** trust client-side price validation — always use PlayFab Catalog prices.
- ❌ **NEVER** store sensitive Title Admin API keys in client builds.
- ❌ **NEVER** call Economy APIs before `LoginAsync()` completes.

## Related Skills

- `@monetization-iap` — Real-money purchase + receipt validation
- `@unity-gaming-services` — Alternative backend (UGS Economy)
- `@backend-integration` — Auth + cloud save foundation
- `@service-locator-pattern` — Register IPlayFabEconomyService at boot
