# Auth session expiry

**Level 2** · Login and session handling

## Scenario
Users stay logged in after logout on another device, or get bounced minutes after a successful refresh.

## Expected behavior
Access tokens expire as configured; refresh rotates correctly; logout clears session server-side and cookie flags are secure.

## Broken behavior
Expiry mismatch and logout not clearing sessions. Auth tests fail.

## Run
```bash
cd 07-auth-session-expiry
python3 test_auth.py
```

## Hints
- Compare token exp claims to server clock in fixtures
- Trace logout in logs/auth.log
- Check cookie Secure/HttpOnly/SameSite settings

## Planned bug themes
token expiry mismatch, refresh token bug, wrong cookie settings, auth bypass, session not cleared on logout

## Success criteria
The tests pass and the behavior matches the scenario.

## Stuck?
Open PR `solution/07-auth-session-expiry` → **Files changed** (when published). Do not merge that PR.

## Status
Scaffold only — buggy `app.py` and rich fixtures/logs still to be authored.
