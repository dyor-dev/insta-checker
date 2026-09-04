import itertools
import string
import time
import requests

def generate_usernames():
    # a-z va 0-9 belgilar
    chars = string.ascii_lowercase + string.digits
    # Barcha 3 belgili kombinatsiyalar (36^3 = 46656)
    all_combos = [''.join(c) for c in itertools.product(chars, repeat=3)]
    # Faqat raqamlardan iborat boganlani chiqarib tashash (1000 ta)
    valid_usernames = [u for u in all_combos if not u.isdigit()]
    return valid_usernames

def main():
    usernames = generate_usernames()
    total = len(usernames) # 45656 ta
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"Jami tekshiriladigan username'lar soni: {total}\n")

    # Fayllarni ochish
    with open("results.txt", "a", encoding="utf-8") as res_file, \
         open("possible.txt", "a", encoding="utf-8") as pos_file:

        for index, username in enumerate(usernames, 1):
            url = f"https://www.instagram.com/{username}/"
            status = "XATO"

            try:
                response = requests.get(url, headers=headers, timeout=10)

                if response.status_code == 200:
                    status = "MAVJUD"
                elif response.status_code == 404:
                    status = "TOPILMADI"
                    pos_file.write(f"{username}\n")
                    pos_file.flush()
                elif response.status_code == 429:
                    print(f"[{index}/{total}] {username} -> 429 RATE LIMIT! Tekshiruv to'xtatildi.")
                    res_file.write(f"{username} -> RATE_LIMIT_429\n")
                    res_file.flush()
                    break
                else:
                    status = "NOANIQ"

            except requests.exceptions.RequestException:
                status = "XATO"

            # Konsolga chiqarish
            print(f"[{index}/{total}] {username} -> {status}")

            # Natijani faylga yozish
            res_file.write(f"{username} -> {status}\n")
            res_file.flush()

            # soniya kutish
            time.sleep(0.5)

if __name__ == "__main__":
    main()
