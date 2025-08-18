# Gerekli kütüphaneleri içe aktar
# gTTS'i yüklemek için terminalde 'pip install gTTS' komutunu çalıştırın.
from gtts import gTTS
import json
import os
import random
import time

# Kullanılacak aksanlar ve gTTS'in kullandığı TLD (Top-Level Domain) eşleşmeleri
ACCENTS = {
    'American': 'com',
    'British': 'co.uk',
    'Australian': 'com.au',
    'Canadian': 'ca',
    'Indian': 'co.in',
    'Irish': 'ie',
    'South_African': 'co.za',
}

# Giriş ve çıkış dosyalarının/klasörlerinin adları
JSON_FILE = 'engaqus.json'
OUTPUT_DIR = 'audios'

def generate_audio_files():
    """
    JSON dosyasını okur, içindeki tüm soruları ve takip sorularını
    rastgele aksanlarla seslendirir ve ID'leri ile .mp3 olarak kaydeder.
    """
    # Ses dosyalarının kaydedileceği klasörü oluştur (eğer yoksa)
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"'{OUTPUT_DIR}' klasörü oluşturuldu.")

    # JSON dosyasını yükle
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"HATA: '{JSON_FILE}' dosyası bulunamadı. Lütfen dosyanın doğru yerde olduğundan emin olun.")
        return
    except json.JSONDecodeError:
        print(f"HATA: '{JSON_FILE}' dosyası geçerli bir JSON formatında değil.")
        return

    print("Ses dosyası oluşturma işlemi başlıyor...")
    
    # JSON verisi içinde döngüye başla
    for level, categories in data.items():
        for category_name, content in categories.items():
            
            # Ana soruları işle
            if 'questions' in content:
                for question in content['questions']:
                    process_text_item(question['id'], question['question'])

            # Takip sorularını işle
            if 'follow_ups' in content:
                for followup in content['follow_ups']:
                    process_text_item(followup['fu_id'], followup['text'])
    
    print("\nTüm ses dosyaları başarıyla oluşturuldu!")

def process_text_item(item_id, text_to_speak):
    """
    Verilen metni ve ID'yi işler, ses dosyasını oluşturur.
    Eğer dosya zaten varsa, bu adımı atlar ve bir bildirim gösterir.
    """
    file_path = os.path.join(OUTPUT_DIR, f"{item_id}.mp3")

    # Eğer dosya zaten varsa, tekrar oluşturma ve kullanıcıyı bilgilendir
    if os.path.exists(file_path):
        print(f"Dosya zaten mevcut, atlanıyor: {item_id}.mp3")
        return

    try:
        # Rastgele bir aksan seç
        accent_name, tld = random.choice(list(ACCENTS.items()))

        # gTTS nesnesini oluştur
        tts = gTTS(text=text_to_speak, lang='en', tld=tld)

        # Dosyayı kaydet
        tts.save(file_path)

        print(f"Oluşturuldu: {item_id}.mp3 ({accent_name} aksanı ile)")

        # Google'ın sunucusuna çok sık istek göndermemek için kısa bir bekleme ekle
        time.sleep(0.5)

    except Exception as e:
        print(f"HATA: {item_id} işlenirken bir sorun oluştu: {e}")


# Script'i ana program olarak çalıştır
if __name__ == "__main__":
    generate_audio_files()
