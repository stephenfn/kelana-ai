# backend/main.py

# Impor fungsi logika bisnis dari modul services.trip_service
from services.trip_service import (
    calculate_daily_budget,
    get_recommendations,
    get_travel_season,
    get_trip_category,
)


def print_trip_summary(destination, country, days, budget, currency, travel_month):
    """Fungsi untuk mencetak ringkasan perjalanan & rekomendasi"""
    
    # Memproses logika bisnis menggunakan layer service
    category = get_trip_category(budget)
    season = get_travel_season(travel_month)
    daily_budget = calculate_daily_budget(budget, days)
    recommendations = get_recommendations(destination)

    print("\n========================")
    print("KelanaAI Recommendation Engine")
    print("========================")
    print(f"Destination  : {destination}")
    print(f"Country      : {country}")
    print(f"Days         : {days}")
    print(f"Budget       : {budget:g} {currency}")
    print(f"Currency     : {currency}")
    print(f"Travel Month : {travel_month}")
    print("------------------------")
    print(f"Trip Category: {category}")
    print(f"Season       : {season}")
    print(f"Daily Budget : {daily_budget:.2f} {currency}/day")
    print("========================")
    print(f"Rekomendasi Tempat di {destination}:")

    # Iterasi list tempat menggunakan loop for
    for index, place in enumerate(recommendations, start=1):
        print(f"  {index}. {place}")
    print("========================\n")


def main():
    print("Masukkan detail rencana perjalanan Anda:")

    # Input interaktif
    destination = input("Masukkan Destination (contoh: Tokyo)   : ")
    country = input("Masukkan Country (contoh: Japan)       : ")
    days = int(input("Masukkan jumlah Days (contoh: 5)       : "))
    budget = float(input("Masukkan Budget (contoh: 1500)         : "))
    currency = input("Masukkan Currency (contoh: USD)        : ")
    travel_month = input("Masukkan Travel Month (contoh: December): ")

    # Panggil fungsi cetak ringkasan
    print_trip_summary(
        destination, country, days, budget, currency, travel_month
    )


if __name__ == "__main__":
    main()