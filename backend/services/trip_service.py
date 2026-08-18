# backend/services/trip_service.py

def get_trip_category(budget: float) -> str:
    """Menentukan kategori perjalanan berdasarkan anggaran."""
    if budget < 1000:
        return "Backpacker"
    elif 1000 <= budget <= 3000:
        return "Standard"
    else:
        return "Luxury"


def get_travel_season(month: str) -> str:
    """Menentukan kategori season berdasarkan bulan keberangkatan."""
    clean_month = month.strip().capitalize()
    if clean_month == "December":
        return "Peak Season"
    elif clean_month == "June":
        return "Holiday Season"
    else:
        return "Regular Season"


def calculate_daily_budget(budget: float, days: int) -> float:
    """Menghitung pembagian anggaran harian."""
    if days > 0:
        return budget / days
    return 0.0


def get_recommendations(destination: str) -> list:
    """Mengembalikan daftar tempat tujuan dalam bentuk list."""
    return [
        f"Pusat Kota & Landmark {destination}",
        f"Wisata Kuliner Khas {destination}",
        f"Situs Budaya & Sejarah {destination}",
        f"Spot Foto & Area Santai {destination}",
    ]