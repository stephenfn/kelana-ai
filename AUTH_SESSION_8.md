# KelanaAI - Session 8: User Authentication with JWT

This document summarizes the authentication implementation for KelanaAI based on Session 8 of the ALKADEMI bootcamp.

## What Was Implemented

### Backend Changes

#### 1. **User Model** (`backend/models/user.py`)
- Created User table with fields: `id`, `name`, `email`, `password_hash`
- Email is unique to prevent duplicate accounts
- Passwords are stored as hashes (bcrypt) - never plain text

#### 2. **Updated Trip Model** (`backend/models/trip.py`)
- Added `user_id` foreign key to link trips to their owners
- Every trip must belong to a user

#### 3. **Authentication Service** (`backend/services/auth_service.py`)
- `hash_password()` - hashes passwords using bcrypt
- `verify_password()` - verifies password against stored hash
- `create_access_token()` - generates JWT tokens with 30-minute expiry
- `decode_token()` - verifies and decodes JWT tokens

#### 4. **Updated Schemas** (`backend/schemas.py`)
- `RegisterRequest` - name, email, password
- `LoginRequest` - email, password
- `TokenResponse` - access_token, token_type
- `UserResponse` - user info (id, name, email)

#### 5. **Protected API Endpoints** (`backend/main.py`)

**Auth Endpoints:**
- `POST /api/v1/auth/register` - Register new user
  - Request: `{ name, email, password }`
  - Response: User object
  - Returns 400 if email already exists

- `POST /api/v1/auth/login` - Login user
  - Request: `{ email, password }`
  - Response: `{ access_token, token_type: "Bearer" }`
  - Returns 401 if credentials invalid

- `GET /api/v1/auth/me` - Get current user info
  - Requires: Authorization header with Bearer token
  - Response: User object

**Protected Trip Endpoints:**
- `GET /api/v1/trips` - List only current user's trips
- `GET /api/v1/trips/{id}` - Get specific trip (403 if not owner)
- `POST /api/v1/trips` - Create trip with user_id from JWT
- `PUT /api/v1/trips/{id}` - Update trip (403 if not owner)
- `DELETE /api/v1/trips/{id}` - Delete trip (403 if not owner)

**Dependency:**
- `get_current_user()` - Extracts user from JWT in Authorization header
  - All protected endpoints use this dependency
  - Returns 401 if token missing/invalid

### Frontend Changes

#### 1. **Login Page** (`frontend/app/login/page.tsx`)
- Email + password form
- Posts to `/api/v1/auth/login`
- Stores JWT in localStorage
- Redirects to `/trips` on success

#### 2. **Register Page** (`frontend/app/register/page.tsx`)
- Name + email + password form
- Validates password match and minimum length
- Posts to `/api/v1/auth/register`
- Redirects to `/login` on success

#### 3. **Updated Trip Service** (`frontend/services/tripService.ts`)
- All API calls now include Authorization header
- Format: `Authorization: Bearer <token>`
- Handles 401 responses by clearing token and redirecting to login
- Updated functions:
  - `getTrips()`
  - `getTrip(id)`
  - `generateTrip(data)`
  - `updateTrip(id, data)` (new)
  - `deleteTrip(id)` (new)

#### 4. **Updated Pages**
- `app/page.tsx` - Checks for token on load, redirects to login if missing
- `app/trips/page.tsx` - Enhanced with:
  - Logout button
  - User greeting (Welcome back, Alice)
  - Loads user info from `/api/v1/auth/me`
  - Redirects to login if not authenticated

## Security Features

### Backend Security
✓ **Password Hashing**: bcrypt with automatic salting
✓ **JWT Authentication**: Signed tokens with expiry
✓ **Ownership Validation**: Backend checks user_id on all operations
✓ **Stateless Auth**: No server-side sessions needed
✓ **Backend-Set User ID**: Frontend cannot spoof user_id

### Frontend Security
✓ **Token Storage**: localStorage (XSS risk - consider HttpOnly cookies in production)
✓ **Authorization Headers**: All protected requests include Bearer token
✓ **Auto Redirect**: 401 responses redirect to login
✓ **Authentication Checks**: Pages redirect to login if no token

## API Usage Examples

### Register
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "email": "alice@email.com", "password": "password123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@email.com", "password": "password123"}'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer"
}
```

### Get Current User
```bash
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

### Create Trip (with auth)
```bash
curl -X POST http://localhost:8000/api/v1/trips \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  -d '{"destination": "Japan", "days": 5, "budget": 2000, "travel_style": "Family"}'
```

## Setup Instructions

### Backend
1. Install new dependencies:
```bash
pip install -r backend/requirement.txt
```

2. Update your PostgreSQL database (existing trips will need user_id):
   - The app will create tables automatically on first run
   - Existing trips may need to be deleted or migrated

3. Change `SECRET_KEY` in `backend/services/auth_service.py` for production

### Frontend
1. No new dependencies needed - uses built-in fetch API

2. Update `.env.local` if needed (default localhost:8000)

## Testing the Full Flow

1. **Register**: Visit http://localhost:3000/register
   - Create account for "Alice" with alice@email.com

2. **Login**: Visit http://localhost:3000/login
   - Login with Alice's credentials
   - Token stored in localStorage

3. **Create Trip**: On home page
   - Generate a trip (auto-saved with user_id)

4. **View Trips**: Click "Trip history"
   - Only Alice's trips appear

5. **Logout**: Click logout button
   - Token removed from localStorage
   - Redirected to login

6. **Register Second User**: Create "Bob" account
   - Login as Bob
   - Verify Bob can't see Alice's trips

## What's Next (Session 9)

- RAG with Amazon Bedrock Knowledge Bases
- Upload travel guides and company docs
- KelanaAI answers using YOUR trusted data
- No more hallucinations on factual questions

## Key Learnings

- **Authentication** = Who you are (verified via login)
- **Authorization** = What you can access (checked per request)
- **Backend owns access** = Never trust user input for ownership
- **JWT is stateless** = No server-side sessions needed
- **Logout is client-only** = Just remove the token
