def print_trip_summary(destination, country, days, budget, currency, travel_month):
    """Fungsi untuk mencetak ringkasan perjalanan dengan format yang rapi"""
    print("\n========================")
    print("KelanaAI")
    print("========================")
    print(f"Destination  : {destination}")
    print(f"Country      : {country}")
    print(f"Days         : {days}")
    # Format :g dipakai biar kalau budgetnya 1500.0, tampilnya tetap 1500 (angka bulat)
    print(f"Budget       : {budget:g} {currency}") 
    print(f"Currency     : {currency}")
    print(f"Travel Month : {travel_month}")
    print("========================\n")

def main():
    print("Masukkan detail rencana perjalanan Anda:")
    
    # a. Input Interaktif & Konversi Tipe Data
    destination = input("Masukkan Destination (contoh: Tokyo)   : ")
    country = input("Masukkan Country (contoh: Japan)       : ")
    days = int(input("Masukkan jumlah Days (contoh: 5)       : "))
    budget = float(input("Masukkan Budget (contoh: 1500)         : "))
    currency = input("Masukkan Currency (contoh: USD)        : ")
    travel_month = input("Masukkan Travel Month (contoh: December): ")

    # b. Panggil fungsi untuk mencetak hasil
    print_trip_summary(destination, country, days, budget, currency, travel_month)

# Memastikan script dijalankan secara langsung
if __name__ == "__main__":
    main()