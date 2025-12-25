import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

class GoogleMapsMiner:
    def __init__(self, headless=False):
        self.options = webdriver.ChromeOptions()
        if headless:
            self.options.add_argument("--headless")
        
        # Maps İngilizce açılsın ki selectorler karışmasın
        self.options.add_argument("--lang=en-US")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("window-size=1280,800")
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    def run_maps_search(self, search_term, total_target=10):
        """
        Google Maps üzerinde arama yapar ve scroll ederek verileri toplar.
        """
        results = []
        try:
            url = "https://www.google.com/maps"
            self.driver.get(url)
            time.sleep(3) # Yükleme beklemesi

            # 1. Arama Kutusunu Bul ve Yaz
            try:
                # Google Maps arama kutusu ID'si genelde 'searchboxinput'tur
                search_box = self.driver.find_element(By.ID, "searchboxinput")
            except:
                # ID değişmişse Name ile dene
                search_box = self.driver.find_element(By.NAME, "q")
            
            print(f"📍 Haritada aranıyor: {search_term}")
            search_box.clear()
            search_box.send_keys(search_term)
            search_box.send_keys(Keys.ENTER)
            
            time.sleep(5) # Sonuçların listelenmesini bekle

            # 2. Scroll (Kaydırma) Mantığı
            # Sol paneldeki liste 'div[role="feed"]' içindedir.
            print("🔄 Liste yükleniyor ve kaydırılıyor...")
            
            extracted_companies = set() # Aynı firmayı tekrar eklememek için

            while len(results) < total_target:
                # Kartları bul (Sınıf isimleri çok değişkendir, genel yapı kullanacağız)
                # Genelde 'div.Nv2PK' her bir kartı temsil eder (Google 2024-2025 yapısı)
                cards = self.driver.find_elements(By.CSS_SELECTOR, "div.Nv2PK")
                
                # Scroll edilecek paneli bul (Listenin olduğu alan)
                # role='feed' olan div scroll edilebilir alandır
                try:
                    scrollable_div = self.driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
                    self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                except:
                    print("⚠️ Scroll alanı bulunamadı, sayfa yapısı farklı olabilir.")
                    break
                
                time.sleep(2) # Yeni elemanların yüklenmesi için bekle

                # Kartları İncele
                for card in cards:
                    if len(results) >= total_target:
                        break
                        
                    try:
                        # Şirket Adı (aria-label genelde şirket ismini tutar)
                        company_name = card.get_attribute("aria-label")
                        
                        # Eğer isim yoksa veya daha önce eklediysek geç
                        if not company_name or company_name in extracted_companies:
                            continue

                        # Web Sitesi Linkini Bulmaya Çalış
                        # Kartın içinde 'a' etiketlerini ararız
                        links = card.find_elements(By.TAG_NAME, "a")
                        website = None
                        
                        for link in links:
                            href = link.get_attribute("href")
                            # Maps linki olmayan, dışarı giden link web sitesidir
                            if href and "google.com/maps" not in href and "google.com/search" not in href:
                                website = href
                                break
                        
                        # Web sitesi yoksa bile Maps linkini alalım, belki sonra işe yarar
                        if not website and links:
                            website = links[0].get_attribute("href")

                        if company_name:
                            extracted_companies.add(company_name)
                            results.append({
                                "Şirket Adı": company_name,
                                "Web Sitesi": website if website else "Yok",
                                "Kaynak": "Google Maps"
                            })
                            print(f"✅ Bulundu: {company_name}")

                    except Exception as e:
                        continue # Hata veren kartı geç

                # Eğer scroll yaptık ama yeni kart gelmediyse (listenin sonu)
                if len(cards) == len(extracted_companies) and len(cards) > 0:
                    print("🏁 Listenin sonuna gelindi.")
                    break

        except Exception as e:
            print(f"❌ Hata: {e}")
            self.driver.save_screenshot("maps_error.png")
        
        finally:
            # self.driver.quit() # Debug için açık kalsın
            pass

        return pd.DataFrame(results)

if __name__ == "__main__":
    miner = GoogleMapsMiner(headless=False)
    # Test Araması
    df = miner.run_maps_search("Aluminium border in Texas", total_target=20)
    print("\n--- MAPS SONUÇLARI ---\n")
    print(df)