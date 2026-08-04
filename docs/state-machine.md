# State Machine

## Asset States

- IN STOCK
- ASSIGNED
- FAULTY
- IN MAINTENANCE
- SCRAPPED

## State Diagram

```
                  ┌──────────► SCRAPPED (final state)
                  │
IN STOCK ──► ASSIGNED ──► IN STOCK
    │            │
    │            └──► FAULTY ──► IN MAINTENANCE ──► IN STOCK
    │                                   │
    └──► IN MAINTENANCE ────────────────┘
```

## Allowed Transitions

| Current State  | Next State     | Allowed |
| -------------- | -------------- | ------- |
| IN STOCK       | ASSIGNED       | ✅      |
| IN STOCK       | IN MAINTENANCE | ✅      |
| ASSIGNED       | IN STOCK       | ✅      |
| ASSIGNED       | FAULTY         | ✅      |
| FAULTY         | IN MAINTENANCE | ✅      |
| IN MAINTENANCE | IN STOCK       | ✅      |
| IN MAINTENANCE | SCRAPPED       | ✅      |

## Business Rules

- An asset in ASSIGNED state must be returned before it can be scrapped.
- An asset in IN MAINTENANCE state cannot be assigned.
- SCRAPPED is the final state.
- Every state transition must follow the allowed transition rules.
