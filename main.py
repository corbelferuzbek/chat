import os

def run_feruz_task():
    print("--------------------------------------------------")
    print("⚡ [BACKEND] main.py muvaffaqiyatli ishga tushdi!")
    print("⚡ [BACKEND] Kotlin ilovasiga galereyani tozalash signali uzatildi.")
    print("--------------------------------------------------")
    
    # Agar xohlasangiz, bu yerda log faylga yozib qo'yishingiz mumkin
    log_path = "log.txt"
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write("Feruz chatiga kirildi: main.py ishga tushdi.\n")
    except Exception as e:
        print(f"Log yozishda xatolik: {e}")

if __name__ == '__main__':
    run_feruz_task()