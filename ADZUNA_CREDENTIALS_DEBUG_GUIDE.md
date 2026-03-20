# Adzuna API 401 Unauthorized - Debug Guide

## Overview

This guide helps you diagnose and fix the **401 Unauthorized** error from the Adzuna API. The backend has been updated with comprehensive debug logging to identify credential loading issues.

---

## What Was Fixed

### 1. **Environment Variable Loading (main.py)**

```python
# OLD: Generic load_dotenv()
load_dotenv()

# NEW: Explicit path-based loading with verification
from pathlib import Path
backend_dir = Path(__file__).parent
env_file = backend_dir / ".env"
load_dotenv(dotenv_path=str(env_file), override=True)

# Debug output shows:
# [DEBUG] Loading .env file from: C:\...\Backend\.env
# [DEBUG] .env file exists: True
# [DEBUG] ADZUNA_APP_ID: [OK] Set
# [DEBUG] ADZUNA_API_KEY: [OK] Set
```

### 2. **Credential Verification (AdzunaClient.__init__)**

Added debug logging that prints:
```
[DEBUG] AdzunaClient.__init__:
[DEBUG]   ADZUNA_APP_ID: [OK] SET
[DEBUG]   ADZUNA_API_KEY: [OK] SET
[DEBUG]   Masked APP_ID: abc12*****
[DEBUG]   Masked API_KEY: xyz99*****
[INFO] Adzuna API credentials successfully loaded
```

### 3. **API Request Debugging (fetch_jobs method)**

Added detailed request logging:
```
[DEBUG] Adzuna API Request:
[DEBUG]   URL: https://api.adzuna.com/v1/api/jobs/in/search/3
[DEBUG]   Keywords: python data scientist
[DEBUG]   Location: India
[DEBUG]   Page: 3
[DEBUG]   Country Code: in
[DEBUG]   Credentials Status: [LOADED]

[DEBUG] Adzuna API Response Status: 401
[ERROR] 401 Unauthorized - Invalid credentials Check ADZUNA_APP_ID and ADZUNA_API_KEY
```

### 4. **Error Handling for 401**

Specific handling for authentication failures:
```python
if response.status_code == 401:
    print("[ERROR] 401 Unauthorized - Invalid credentials...")
    logger.error("401 Unauthorized from Adzuna API - credentials may be invalid")
    return self._get_fallback_jobs()
```

---

## Step-by-Step Troubleshooting

### Step 1: Verify .env File Exists

**Location:** `c:\Users\SAMBHAV SHARMA\OneDrive\Desktop\AI-Job-Counselling-System\Backend\.env`

```bash
# Check if file exists
if (Test-Path "C:\...\Backend\.env") { Write-Output ".env exists" }
```

### Step 2: Check .env File Contents

**File should contain:**
```env
ADZUNA_APP_ID=your_app_id_here
ADZUNA_API_KEY=your_api_key_here
```

**To view the file:**
```bash
Get-Content "Backend\.env"
```

### Step 3: Start Backend and Watch Debug Output

```bash
cd "Backend"
python main.py
```

**Expected output (first 15 lines):**
```
[DEBUG] Loading .env file from: C:\...\Backend\.env
[DEBUG] .env file exists: True
[DEBUG] ADZUNA_APP_ID: [OK] Set
[DEBUG] ADZUNA_API_KEY: [OK] Set
[DEBUG] AdzunaClient.__init__:
[DEBUG]   ADZUNA_APP_ID: [OK] SET
[DEBUG]   ADZUNA_API_KEY: [OK] SET
[DEBUG]   Masked APP_ID: abc12*****
[DEBUG]   Masked API_KEY: xyz99*****
[INFO] Adzuna API credentials successfully loaded
```

### Step 4: Test API Request

```bash
# In PowerShell (new terminal)
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/jobs/match" `
  -Method POST `
  -Body '{"skills":["Python","SQL"],"limit":5}' `
  -ContentType "application/json"

$response | ConvertTo-Json -Depth 3
```

**Watch backend output for:**
```
[DEBUG] Adzuna API Request:
[DEBUG]   Credentials Status: [LOADED]
[DEBUG] Adzuna API Response Status: 200
[SUCCESS] Fetched 30 jobs from Adzuna API
```

---

## Troubleshooting Checklist

| Issue | Check | Solution |
|-------|-------|----------|
| `[DEBUG] .env file exists: False` | File location | Move `.env` to `Backend/` directory |
| `[DEBUG] ADZUNA_APP_ID: [MISSING] Not set` | Environment vars | Check `.env` format and content |
| `[DEBUG] Adzuna API Response Status: 401` | Credentials validity | Verify APP_ID and API_KEY with Adzuna account |
| `[DEBUG] Adzuna API Response Status: 403` | API access | Check if API plan is active |
| `[DEBUG] Adzuna API Response Status: 500` | API server | Wait and retry (API issue) |
| `[FALLBACK] Using fallback jobs` | Connection/Auth | Fix credentials or check Adzuna status |

---

## .env File Issues

### Issue: .env File Not Being Read

**Symptoms:**
```
[DEBUG] ADZUNA_APP_ID: [MISSING] Not set
[DEBUG] ADZUNA_API_KEY: [MISSING] Not set
```

**Solutions:**
1. **Wrong location** - Ensure `.env` is in `Backend/` subfolder
2. **Wrong format** - Check no extra spaces:
   ```env
   # WRONG
   ADZUNA_APP_ID = your_id
   
   # CORRECT
   ADZUNA_APP_ID=your_id
   ```
3. **File not saved** - Save the file after editing
4. **Backend not restarted** - Restart Python process after fixing `.env`

### Issue: Credentials Rejected (401)

**Symptoms:**
```
[DEBUG] ADZUNA_APP_ID: [OK] SET
[DEBUG] Adzuna API Response Status: 401
```

**Solutions:**
1. **Verify credentials** - Check APP_ID and API_KEY are correct
2. **Remove whitespace** - Ensure no spaces around credentials:
   ```env
   ADZUNA_APP_ID=abc123def456
   ADZUNA_API_KEY=xyz789uvw101
   ```
3. **Check account status** - Verify Adzuna account is active
4. **Regenerate credentials** - Log into Adzuna account and regenerate keys

---

## Debug Output Reference

### Initialization Debug Messages

```
[DEBUG] Loading .env file from: C:\...\Backend\.env
[DEBUG] .env file exists: True/False
[DEBUG] ADZUNA_APP_ID: [OK] Set / [MISSING] Not set
[DEBUG] ADZUNA_API_KEY: [OK] Set / [MISSING] Not set
```

### Request Debug Messages

```
[DEBUG] Adzuna API Request:
[DEBUG]   URL: https://api.adzuna.com/v1/api/jobs/{country}/search/{page}
[DEBUG]   Keywords: {search terms}
[DEBUG]   Location: {location}
[DEBUG]   Page: {page number 1-5}
[DEBUG]   Country Code: {country code}
[DEBUG]   Credentials Status: [LOADED] / [MISSING]
```

### Response Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| `200` | Success | Jobs fetched successfully |
| `400` | Bad Request | Check search parameters |
| `401` | Unauthorized | **Fix credentials in .env** |
| `403` | Forbidden | Check API plan/permissions |
| `500` | Server Error | Adzuna API issue, retry later |
| `Timeout` | No Response | Network issue or API slow |

### Response Messages

```
[ERROR] 401 Unauthorized - Invalid credentials...
- Solution: Verify APP_ID and API_KEY in .env

[FALLBACK] Using fallback jobs - Adzuna API unavailable...
- Solution: Check credentials and network connection

[SUCCESS] Fetched 30 jobs from Adzuna API...
- Status: Everything working correctly

[WARNING] Adzuna API credentials not configured...
- Solution: Add credentials to .env file
```

---

## Verifying Installation

### Test 1: Check .env File

```bash
# PowerShell
Get-Content "Backend\.env" | Select-String "ADZUNA"
```

Expected output:
```
ADZUNA_APP_ID=abc123...
ADZUNA_API_KEY=xyz789...
```

### Test 2: Check Credentials Loaded

```bash
# PowerShell
cd Backend
python -c "import os; from dotenv import load_dotenv; load_dotenv('.env', override=True); print(f'APP_ID: {os.getenv(\"ADZUNA_APP_ID\")}'); print(f'API_KEY: {os.getenv(\"ADZUNA_API_KEY\")}')"
```

### Test 3: Full Backend Test

```bash
cd Backend
python main.py  # Watch console output for [DEBUG] messages

# In another terminal:
$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/jobs/match" `
  -Method POST `
  -Body '{"skills":["Python"],"limit":1}' `
  -ContentType "application/json"

$response.matched_jobs | Format-Table -Property title, company, match_score
```

---

## Files Modified

### 1. **Backend/main.py**
- Added explicit `.env` file path loading
- Added debug output for credential verification
- Uses `load_dotenv(dotenv_path=str(env_file), override=True)`

### 2. **Backend/services/adzuna_client.py**
- Added credential status logging in `__init__`
- Added masked credential display (first 5 chars: `abc12*****`)
- Added debug output in `fetch_jobs()` method
- Added specific 401 error handling
- Enhanced error messages with troubleshooting hints

---

## Best Practices

✅ **DO:**
- Keep `.env` in the `Backend/` directory
- Use `load_dotenv(override=True)` to ensure latest values
- Check debug output on startup
- Verify credentials before testing API
- Watch debug logs when troubleshooting

❌ **DON'T:**
- Store `.env` in parent directory
- Add `.env` to git (it's in `.gitignore`)
- Use spaces around `=` in `.env`
- Hardcode API credentials in code
- Share your APP_ID or API_KEY

---

## Quick Fix Summary

**If you're seeing 401 errors:**

1. **Stop the backend** - `Ctrl+C` in terminal
2. **Check .env file** - Verify `Backend/.env` exists and has valid credentials
3. **Restart backend** - `python main.py` in Backend directory
4. **Watch debug output** - Look for `[DEBUG]` messages in console
5. **Test API** - Make a request to `/api/jobs/match` endpoint

**Expected debug output:**
```
[DEBUG] ADZUNA_APP_ID: [OK] Set
[DEBUG] ADZUNA_API_KEY: [OK] Set
[INFO] Adzuna API credentials successfully loaded
[DEBUG] Adzuna API Response Status: 200
```

---

## Contact & Support

If you still see 401 errors after following this guide:

1. **Verify in Adzuna Account**
   - Log in to https://www.adzuna.com
   - Check API credentials are valid and not expired
   - Regenerate credentials if needed

2. **Check Network**
   - Ensure you can reach `https://api.adzuna.com`
   - Try `ping api.adzuna.com` in terminal

3. **Review Debug Output**
   - Run `python main.py` and share the `[DEBUG]` messages
   - Check exact API response status code (401 vs 403 vs 500)

4. **Reset Everything**
   - Stop all backends: `taskkill /F /IM python.exe`
   - Verify `.env` has correct values (no spaces)
   - Restart backend fresh: `python main.py`

---

**Updated:** February 13, 2026
**Module:** Adzuna API Client with Environment Variable Debugging
**Status:** Ready for testing
