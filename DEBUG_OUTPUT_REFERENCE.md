# Debug Output Reference Guide

## Expected Debug Output When Backend Starts

### SUCCESS SCENARIO: Credentials Properly Loaded

```
[DEBUG] Loading .env file from: C:\Users\SAMBHAV SHARMA\OneDrive\Desktop\AI-Job-Counselling-System\Backend\.env
[DEBUG] .env file exists: True
[DEBUG] ADZUNA_APP_ID: [OK] Set
[DEBUG] ADZUNA_API_KEY: [OK] Set
[DEBUG] AdzunaClient.__init__:
[DEBUG]   ADZUNA_APP_ID: [OK] SET
[DEBUG]   ADZUNA_API_KEY: [OK] SET
[DEBUG]   Masked APP_ID: abc12*****  (first 5 chars + asterisks)
[DEBUG]   Masked API_KEY: xyz78*****  (first 5 chars + asterisks)
[INFO] Adzuna API credentials successfully loaded

INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**What this means:** ✅ Everything is working correctly. Your credentials are loaded and ready.

---

### FAILURE SCENARIO 1: Missing .env File

```
[DEBUG] Loading .env file from: C:\Users\SAMBHAV SHARMA\OneDrive\Desktop\AI-Job-Counselling-System\Backend\.env
[DEBUG] .env file exists: False
[DEBUG] ADZUNA_APP_ID: [MISSING] Not set
[DEBUG] ADZUNA_API_KEY: [MISSING] Not set
[DEBUG] AdzunaClient.__init__:
[DEBUG]   ADZUNA_APP_ID: [MISSING] NOT SET
[DEBUG]   ADZUNA_API_KEY: [MISSING] NOT SET
[WARNING] Adzuna API credentials not configured - will use fallback jobs
```

**What this means:** ❌ The `.env` file doesn't exist or is not in the right location.
**Fix:** Create `Backend/.env` file with your credentials.

---

### FAILURE SCENARIO 2: .env File Exists But Empty Credentials

```
[DEBUG] Loading .env file from: C:\University\AI-Job-Counselling-System\Backend\.env
[DEBUG] .env file exists: True
[DEBUG] ADZUNA_APP_ID: [MISSING] Not set
[DEBUG] ADZUNA_API_KEY: [MISSING] Not set
[DEBUG] AdzunaClient.__init__:
[DEBUG]   ADZUNA_APP_ID: [MISSING] NOT SET
[DEBUG]   ADZUNA_API_KEY: [MISSING] NOT SET
[WARNING] Adzuna API credentials not configured - will use fallback jobs
```

**What this means:** ❌ The `.env` file exists but doesn't have the credentials filled in.
**Fix:** Add credentials to `.env`:
```env
ADZUNA_APP_ID=your_actual_app_id
ADZUNA_API_KEY=your_actual_api_key
```

---

### FAILURE SCENARIO 3: Invalid Credentials (401 Error)

**During startup (credentials appear to be set):**
```
[DEBUG] Loading .env file from: C:\Users\SAMBHAV SHARMA\OneDrive\Desktop\AI-Job-Counselling-System\Backend\.env
[DEBUG] .env file exists: True
[DEBUG] ADZUNA_APP_ID: [OK] Set
[DEBUG] ADZUNA_API_KEY: [OK] Set
[DEBUG] AdzunaClient.__init__:
[DEBUG]   ADZUNA_APP_ID: [OK] SET
[DEBUG]   ADZUNA_API_KEY: [OK] SET
[DEBUG]   Masked APP_ID: wrong1*****
[DEBUG]   Masked API_KEY: creds2*****
[INFO] Adzuna API credentials successfully loaded
```

**When making a job search request:**
```
[DEBUG] Adzuna API Request:
[DEBUG]   URL: https://api.adzuna.com/v1/api/jobs/in/search/3
[DEBUG]   Keywords: python developer
[DEBUG]   Location: India
[DEBUG]   Page: 3
[DEBUG]   Country Code: in
[DEBUG]   Credentials Status: [LOADED]

[DEBUG] Adzuna API Response Status: 401
[ERROR] 401 Unauthorized - Invalid credentials. Check ADZUNA_APP_ID and ADZUNA_API_KEY
[FALLBACK] Using fallback jobs - Adzuna API unavailable or credentials invalid
```

**What this means:** ❌ The `.env` file is being read, but the credentials are invalid or expired.
**Fix:** 
1. Log in to your Adzuna account
2. Verify APP_ID and API_KEY are correct
3. Check if credentials have expired
4. Regenerate credentials if needed
5. Update `.env` file with new credentials

---

## Debug Output During API Calls

### Successful Job Fetch

```
[DEBUG] Adzuna API Request:
[DEBUG]   URL: https://api.adzuna.com/v1/api/jobs/in/search/2
[DEBUG]   Keywords: python sql database
[DEBUG]   Location: India
[DEBUG]   Page: 2
[DEBUG]   Country Code: in
[DEBUG]   Credentials Status: [LOADED]

[DEBUG] Adzuna API Response Status: 200
[SUCCESS] Fetched 30 jobs from Adzuna API, returning top 10
```

**Meaning:** ✅ API.call successful, 30 jobs retrieved, returning 10 top results.

---

### Connection Timeout

```
[DEBUG] Adzuna API Request:
[DEBUG]   URL: https://api.adzuna.com/v1/api/jobs/in/search/1
[DEBUG]   Keywords: python
...

[ERROR] Timeout - Adzuna API did not respond within 15s
[FALLBACK] Using fallback jobs - Adzuna API unavailable or credentials invalid
```

**Meaning:** ❌ API didn't respond within 15 seconds.
**Causes:** Slow network, API down, firewall blocking, etc.

---

### Connection Error

```
[ERROR] Connection error with Adzuna API: <error details>
[FALLBACK] Using fallback jobs - Adzuna API unavailable or credentials invalid
```

**Meaning:** ❌ Can't connect to Adzuna API server.
**Causes:** Network issue, DNS issue, API server down.

---

## Debug Message Reference

### Initialization Messages (Startup)

| Message | Meaning | Action |
|---------|---------|--------|
| `[DEBUG] Loading .env file from: ...` | Shows which .env path is being used | Verify path is correct |
| `[DEBUG] .env file exists: True` | .env file found | Good |
| `[DEBUG] .env file exists: False` | .env file not found | Create it |
| `[DEBUG] ADZUNA_APP_ID: [OK] Set` | APP_ID loaded | Good |
| `[DEBUG] ADZUNA_APP_ID: [MISSING] Not set` | APP_ID missing | Add to .env |
| `[DEBUG] ADZUNA_API_KEY: [OK] Set` | API_KEY loaded | Good |
| `[DEBUG] ADZUNA_API_KEY: [MISSING] Not set` | API_KEY missing | Add to .env |
| `[DEBUG] Masked APP_ID: abc123*****` | Shows first 5 chars | Verify it's your credential |
| `[INFO] Adzuna API credentials successfully loaded` | All ready | Proceed |
| `[WARNING] Adzuna API credentials not configured` | Missing credentials | Add to .env |

### Request Messages (When making API calls)

| Message | Meaning | Action |
|---------|---------|--------|
| `[DEBUG] Adzuna API Request:` | About to make API call | Watch for status code |
| `[DEBUG]   URL: ...` | API endpoint being called | Verify it looks correct |
| `[DEBUG]   Keywords: ...` | Search terms being used | Verify they're relevant |
| `[DEBUG]   Location: ...` | Job location filter | Verify it's correct |
| `[DEBUG]   Page: ...` | Which page being fetched (1-5) | Random selection |
| `[DEBUG] Credentials Status: [LOADED]` | Credentials ready for request | Good |
| `[DEBUG] Credentials Status: [MISSING]` | Credentials not available | Error will follow |

### Response Messages

| Message | Meaning | Action |
|---------|---------|--------|
| `[DEBUG] Adzuna API Response Status: 200` | Success | Jobs being processed |
| `[DEBUG] Adzuna API Response Status: 401` | Unauthorized | Check credentials |
| `[ERROR] 401 Unauthorized - Invalid credentials` | Auth failed | Fix credentials in .env |
| `[SUCCESS] Fetched 30 jobs from Adzuna API` | Request succeeded | Jobs returned |
| `[FALLBACK] Using fallback jobs` | Using sample data | Fix issue and retry |

---

## Common Scenarios & Solutions

### Scenario 1: First Run - Credentials Not Set

**You see:**
```
[DEBUG] .env file exists: False
[DEBUG] ADZUNA_APP_ID: [MISSING] Not set
```

**What to do:**
1. Create file: `Backend/.env`
2. Add lines:
   ```env
   ADZUNA_APP_ID=your_app_id_from_adzuna
   ADZUNA_API_KEY=your_api_key_from_adzuna
   ```
3. Save the file
4. Restart backend: `python main.py`

---

### Scenario 2: Credentials Set But 401 Error

**You see:**
```
[DEBUG] ADZUNA_APP_ID: [OK] Set
[DEBUG] Masked APP_ID: abc12*****
[DEBUG] Adzuna API Response Status: 401
```

**What to do:**
1. Log in to Adzuna.com
2. Check if APP_ID starts with "abc12"
3. If not, update `.env` with correct values
4. If yes, try regenerating credentials
5. Update `.env` and restart backend

---

### Scenario 3: Credentials Valid But Getting Fallback

**You see:**
```
[INFO] Adzuna API credentials successfully loaded
[FALLBACK] Using fallback jobs
```

**Possible causes:**
- Network connectivity issue
- Adzuna API server down
- Firewall blocking api.adzuna.com
- Timeout (API too slow)

**What to do:**
1. Check your internet connection
2. Try visiting https://api.adzuna.com in browser
3. Wait a few minutes and retry
4. Contact Adzuna support if it continues

---

### Scenario 4: Immediate Fallback Without Details

**You see:**
```
[WARNING] Adzuna API credentials not configured
[FALLBACK] Using fallback jobs
```

**What to do:**
1. Verify `.env` file exists in `Backend/` folder
2. Verify it contains ADZUNA_APP_ID and ADZUNA_API_KEY
3. No extra spaces: `ADZUNA_APP_ID=abc123` (not `ADZUNA_APP_ID = abc123`)
4. No quotes: `ADZUNA_APP_ID=abc123` (not `ADZUNA_APP_ID="abc123"`)
5. Save file and restart backend

---

## Tips for Reading Debug Output

### 1. Look for Your Credentials Validation
Check if these appear in order:
```
[DEBUG] .env file exists: True
[DEBUG] ADZUNA_APP_ID: [OK] Set
[DEBUG] ADZUNA_API_KEY: [OK] Set
[INFO] Adzuna API credentials successfully loaded
```

If you see `[MISSING]` instead of `[OK]`, credentials aren't loading.

### 2. Check API Response Status Codes
- `200` = Success ✅
- `401` = Unauthorized (bad credentials) ❌
- `403` = Forbidden (account issue) ❌
- `500` = Server error ❌
- `Timeout` = No response ❌

### 3. Look for [ERROR] or [FALLBACK]
These indicate something went wrong. Read the message for details.

### 4. Verify Masked Credentials
Compare first 5 characters with your actual APP_ID:
```
[DEBUG] Masked APP_ID: abc12*****
```
Your real APP_ID should start with "abc12".

---

## Quick Diagnostic Steps

When something isn't working:

1. **Stop backend**
   ```bash
   Ctrl+C
   ```

2. **Check .env file**
   ```bash
   Get-Content Backend\.env
   ```
   Should show:
   ```
   ADZUNA_APP_ID=your_id
   ADZUNA_API_KEY=your_key
   ```

3. **Start backend fresh**
   ```bash
   cd Backend
   python main.py
   ```

4. **Read first 20 lines of output**
   Look for any `[MISSING]` or `[ERROR]` messages

5. **Test API**
   ```bash
   # In new terminal:
   $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/jobs/match" `
     -Method POST `
     -Body '{"skills":["Python"],"limit":1}' `
     -ContentType "application/json"
   ```

6. **Watch backend output**
   Look for API request/response debug lines

---

## Sample Complete Success Output

```
[DEBUG] Loading .env file from: C:\...\Backend\.env
[DEBUG] .env file exists: True
[DEBUG] ADZUNA_APP_ID: [OK] Set
[DEBUG] ADZUNA_API_KEY: [OK] Set
[DEBUG] AdzunaClient.__init__:
[DEBUG]   ADZUNA_APP_ID: [OK] SET
[DEBUG]   ADZUNA_API_KEY: [OK] SET
[DEBUG]   Masked APP_ID: abc12def456ghi78*
[DEBUG]   Masked API_KEY: xyz98vut654srq32*
[INFO] Adzuna API credentials successfully loaded

INFO:     Started server process [5432]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000

# Later, when making API call:
[DEBUG] Adzuna API Request:
[DEBUG]   URL: https://api.adzuna.com/v1/api/jobs/in/search/3
[DEBUG]   Keywords: python
[DEBUG]   Location: India
[DEBUG]   Page: 3
[DEBUG]   Country Code: in
[DEBUG]   Credentials Status: [LOADED]

[DEBUG] Adzuna API Response Status: 200
[SUCCESS] Fetched 30 jobs from Adzuna API, returning top 10

GET /api/jobs/match HTTP/1.1" 200 OK
```

**Interpretation:** ✅ Everything working perfectly!

---

**Last Updated:** February 13, 2026
**Module:** Adzuna API Client
**Debug Version:** Comprehensive with 401 Handling
