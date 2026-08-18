# backend/main.py
from fastapi import FastAPI

app = FastAPI(title="KelanaAI API")

# Endpoint 1: Rekomendasi Tempat
@app.get("/api/v1/recommendations")
def get_recommendations():
    # Mengembalikan daftar rekomendasi tempat wisata dalam bentuk List
    return ["Tokyo Tower", "Mount Fuji", "Shibuya"]

# Endpoint 2: Transportasi
@app.get("/api/v1/transportations")
def get_transportations():
    # Mengembalikan daftar pilihan moda transportasi dalam bentuk List
    return ["Bus", "Train", "Flight"]