from fastapi import FastAPI, HTTPException

try:
    from .database import SessionLocal
    from .models.trip import Trip
    from .schemas import TripRequest, TripUpdateRequest
    from .services.trip_service import calculate_daily_budget, get_trip_category
except ImportError:
    from database import SessionLocal
    from models.trip import Trip
    from schemas import TripRequest, TripUpdateRequest
    from services.trip_service import calculate_daily_budget, get_trip_category

app = FastAPI()

# --- PART 7: POST (Save Trip) ---
@app.post("/api/v1/trips")
def create_trip(request: TripRequest):
    # Logic perhitungan dari sesi sebelumnya
    daily_budget = calculate_daily_budget(request.budget, request.days)
    category = get_trip_category(request.budget)
    
    # 1. Buat object model (bukan dictionary biasa lagi)
    trip = Trip(
        destination=request.destination,
        days=request.days,
        budget=request.budget,
        category=category,
        daily_budget=daily_budget
    )
    
    # 2. Proses nyimpen ke DB
    db = SessionLocal()  # Buka koneksi
    db.add(trip)         # Siapin data
    db.commit()          # Simpan permanen
    db.refresh(trip)     # Reload biar dapet ID otomatis dari Postgres
    db.close()           # Tutup koneksi
    
    return trip

# --- PART 8: GET (Retrieve Trips) ---

# 1. Ambil semua trip
@app.get("/api/v1/trips")
def list_trips():
    db = SessionLocal()
    trips = db.query(Trip).all()  # Select * from trips
    db.close()
    return trips

# 2. Ambil trip by ID
@app.get("/api/v1/trips/{trip_id}")
def get_trip(trip_id: int):
    db = SessionLocal()
    # Query cari berdasarkan ID
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    db.close()
    
    if trip is None:
        raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")
    return trip

# --- PART 7: PUT (Update Trip Budget) ---
@app.put("/api/v1/trips/{trip_id}")
def update_trip(trip_id: int, request: TripUpdateRequest):
    db = SessionLocal()
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if trip is None:
        db.close()
        raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")

    trip.budget = request.budget
    trip.category = get_trip_category(trip.budget)
    trip.daily_budget = calculate_daily_budget(trip.budget, trip.days)

    db.commit()
    db.refresh(trip)
    db.close()
    return trip

# --- PART 7: DELETE (Delete Trip) ---
@app.delete("/api/v1/trips/{trip_id}")
def delete_trip(trip_id: int):
    db = SessionLocal()
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if trip is None:
        db.close()
        raise HTTPException(status_code=404, detail=f"Trip with id {trip_id} not found")

    db.delete(trip)
    db.commit()
    db.close()

    return {"message": f"Trip with id {trip_id} deleted successfully"}