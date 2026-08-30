from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

try:
    from .database import SessionLocal, Base, engine
    from .models.trip import Trip
    from .models.user import User
    from .schemas import TripRequest, TripUpdateRequest, RegisterRequest, LoginRequest, TokenResponse, UserResponse
    from .services.trip_service import calculate_daily_budget, get_trip_category
    from .services.auth_service import hash_password, verify_password, create_access_token, decode_token
except ImportError:
    from database import SessionLocal, Base, engine
    from models.trip import Trip
    from models.user import User
    from schemas import TripRequest, TripUpdateRequest, RegisterRequest, LoginRequest, TokenResponse, UserResponse
    from services.trip_service import calculate_daily_budget, get_trip_category
    from services.auth_service import hash_password, verify_password, create_access_token, decode_token

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get current user from JWT
def get_current_user(authorization: Optional[str] = Header(None)) -> User:
    """Extract and verify JWT token from Authorization header."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        # Expected format: "Bearer <token>"
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token does not contain user_id")
    
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user


# ============= AUTH ENDPOINTS =============

# --- PART 3: POST /auth/register ---
@app.post("/api/v1/auth/register", response_model=UserResponse)
def register(request: RegisterRequest):
    """Register a new user."""
    db = SessionLocal()
    
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user with hashed password
    user = User(
        name=request.name,
        email=request.email,
        password_hash=hash_password(request.password)
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    
    return user


# --- PART 4: POST /auth/login ---
@app.post("/api/v1/auth/login", response_model=TokenResponse)
def login(request: LoginRequest):
    """Login user and return JWT token."""
    db = SessionLocal()
    
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    db.close()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Verify password
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create JWT token
    access_token = create_access_token(data={"sub": user.id})
    
    return {"access_token": access_token, "token_type": "Bearer"}


# --- GET /auth/me ---
@app.get("/api/v1/auth/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user info."""
    return current_user


# ============= TRIP ENDPOINTS =============

# --- PART 7: POST (Save Trip) ---
@app.post("/api/v1/trips")
def create_trip(request: TripRequest, current_user: User = Depends(get_current_user)):
    """Create a new trip for the authenticated user."""
    # Logic perhitungan dari sesi sebelumnya
    daily_budget = calculate_daily_budget(request.budget, request.days)
    category = get_trip_category(request.budget)
    
    # Buat object model dengan user_id dari JWT
    trip = Trip(
        user_id=current_user.id,  # Backend sets this from JWT
        destination=request.destination,
        days=request.days,
        budget=request.budget,
        category=category,
        daily_budget=daily_budget
    )
    
    # Proses nyimpen ke DB
    db = SessionLocal()
    db.add(trip)
    db.commit()
    db.refresh(trip)
    db.close()
    
    return trip


# --- PART 8: GET (Retrieve Trips) ---

# 1. Ambil semua trip untuk user yang login
@app.get("/api/v1/trips")
def list_trips(current_user: User = Depends(get_current_user)):
    """Get all trips for the authenticated user."""
    db = SessionLocal()
    # Filter trips by user_id
    trips = db.query(Trip).filter(Trip.user_id == current_user.id).all()
    db.close()
    return trips


# 2. Ambil trip by ID (only if belongs to current user)
@app.get("/api/v1/trips/{trip_id}")
def get_trip(trip_id: int, current_user: User = Depends(get_current_user)):
    """Get a specific trip by ID (user can only access their own trips)."""
    db = SessionLocal()
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    db.close()
    
    if trip is None:
        raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")
    
    # Check ownership
    if trip.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to access this trip")
    
    return trip


# --- PART 7: PUT (Update Trip Budget) ---
@app.put("/api/v1/trips/{trip_id}")
def update_trip(trip_id: int, request: TripUpdateRequest, current_user: User = Depends(get_current_user)):
    """Update a trip's budget (user can only update their own trips)."""
    db = SessionLocal()
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if trip is None:
        db.close()
        raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")
    
    # Check ownership
    if trip.user_id != current_user.id:
        db.close()
        raise HTTPException(status_code=403, detail="You do not have permission to update this trip")

    trip.budget = request.budget
    trip.category = get_trip_category(trip.budget)
    trip.daily_budget = calculate_daily_budget(trip.budget, trip.days)

    db.commit()
    db.refresh(trip)
    db.close()
    return trip


# --- PART 7: DELETE (Delete Trip) ---
@app.delete("/api/v1/trips/{trip_id}")
def delete_trip(trip_id: int, current_user: User = Depends(get_current_user)):
    """Delete a trip (user can only delete their own trips)."""
    db = SessionLocal()
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if trip is None:
        db.close()
        raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")
    
    # Check ownership
    if trip.user_id != current_user.id:
        db.close()
        raise HTTPException(status_code=403, detail="You do not have permission to delete this trip")

    db.delete(trip)
    db.commit()
    db.close()

    return {"message": f"Trip with id {trip_id} deleted successfully"}