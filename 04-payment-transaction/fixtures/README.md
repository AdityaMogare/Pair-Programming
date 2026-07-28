# Fixtures for 04-payment-transaction

| File | Role |
|------|------|
| `seed_accounts.json` | Starting ledger balances (Alice has 10000 cents) |
| `expected_scenario.json` | Scripted charge / retry / decline / timeout steps |

Amounts in the scenario use dollar strings (`"19.99"`, `"1.15"`) that must become exact integer cents.
