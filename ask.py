import json
import os
import random
from gtts import gTTS

# --- Ayarlar ---
JSON_FILE_PATH = 'engaqus.json'
AUDIO_FOLDER_PATH = 'audios'

# Kullanılacak aksanlar ve gTTS için karşılık gelen 'tld' (top-level domain) değerleri
ACCENTS = {
    'American': 'com',
    'British': 'co.uk',
    'Australian': 'com.au',
    'Canadian': 'ca',
    'Indian': 'co.in',
    'Irish': 'ie',
    'South_African': 'co.za',
}

def create_audio_files():
    """
    JSON dosyasını okur ve her soru için, eğer zaten mevcut değilse,
    rastgele bir aksanla ses dosyası oluşturur.
    """
    print("Seslendirme script'i başlatıldı...")

    # 1. Ses dosyalarının kaydedileceği klasörün varlığını kontrol et, yoksa oluştur.
    if not os.path.exists(AUDIO_FOLDER_PATH):
        print(f"'{AUDIO_FOLDER_PATH}' klasörü bulunamadı, oluşturuluyor...")
        os.makedirs(AUDIO_FOLDER_PATH)
    else:
        print(f"'{AUDIO_FOLDER_PATH}' klasörü zaten mevcut.")

    # 2. JSON dosyasını oku ve verileri yükle.
    try:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            questions = json.load(f)
        print(f"'{JSON_FILE_PATH}' dosyasından {len(questions)} adet soru başarıyla yüklendi.")
    except FileNotFoundError:
        print(f"HATA: '{JSON_FILE_PATH}' dosyası bulunamadı. Lütfen dosyanın doğru yerde olduğundan emin olun.")
        return
    except json.JSONDecodeError:
        print(f"HATA: '{JSON_FILE_PATH}' dosyası geçerli bir JSON formatında değil.")
        return

    # 3. Her bir soruyu döngüye al ve ses dosyasını oluştur.
    created_count = 0
    skipped_count = 0
    for item in questions:
        try:
            question_id = item['id']
            question_text = item['question']
            
            # Ses dosyasının adını ID'ye göre belirle (örn: 1.mp3, 2.mp3)
            audio_file_path = os.path.join(AUDIO_FOLDER_PATH, f"{question_id}.mp3")

            # Eğer bu ID'ye sahip ses dosyası zaten varsa, bu adımı atla.
            if os.path.exists(audio_file_path):
                # print(f"'{question_id}.mp3' zaten mevcut, atlanıyor.")
                skipped_count += 1
                continue

            # Eğer dosya yoksa, oluşturma işlemine başla.
            print(f"'{question_id}.mp3' oluşturuluyor...")
            
            # Rastgele bir aksan seç
            accent_name, tld = random.choice(list(ACCENTS.items()))
            
            # gTTS kullanarak metni sese çevir
            tts = gTTS(text=question_text, lang='en', tld=tld, slow=False)
            
            # Ses dosyasını kaydet
            tts.save(audio_file_path)
            
            print(f"-> '{question_id}.mp3' ({accent_name} aksanıyla) başarıyla oluşturuldu.")
            created_count += 1

        except KeyError:
            print(f"UYARI: JSON içindeki bir öğede 'id' veya 'question' anahtarı eksik. Bu öğe atlanıyor: {item}")
        except Exception as e:
            print(f"HATA: '{question_id}' ID'li soru işlenirken bir hata oluştu: {e}")

    print("\n--- İşlem Tamamlandı ---")
    print(f"Yeni oluşturulan dosya sayısı: {created_count}")
    print(f"Mevcut olduğu için atlanan dosya sayısı: {skipped_count}")
    print(f"Ses dosyalarınızı '{AUDIO_FOLDER_PATH}' klasöründe bulabilirsiniz.")


if __name__ == "__main__":
    create_audio_files()
