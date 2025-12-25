import streamlit as st
import pandas as pd
import time
from src.google_miner import GoogleSearchMiner # Bizim yazdığımız modülü çağırıyoruz

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="BuyerScout", page_icon="🎯", layout="wide")

st.title("🎯 BuyerScout: Lead Generation")
st.markdown("Hedef kitleni belirle, Google'dan topla, Apollo ile zenginleştir.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Arama Parametreleri")
    target_keyword = st.text_input("Ürün / Sektör", "wholesale aluminium suppliers usa")
    pages_to_scrape = st.slider("Taranacak Sayfa Sayısı", 1, 5, 1)
    
    st.info("Not: Sayfa sayısı arttıkça işlem süresi uzar.")

# --- ANA EKRAN ---
col1, col2 = st.columns([3, 1])

with col1:
    # "session_state" kullanarak veriyi hafızada tutuyoruz (sayfa yenilenince kaybolmasın diye)
    if 'leads_data' not in st.session_state:
        st.session_state.leads_data = None

    start_btn = st.button("🚀 Taramayı Başlat", type="primary")

    if start_btn:
        status_box = st.status("Bot çalışıyor...", expanded=True)
        
        try:
            status_box.write("🤖 Tarayıcı başlatılıyor...")
            # Miner Class'ımızı çağırıyoruz
            miner = GoogleSearchMiner(headless=False) 
            
            status_box.write(f"🔍 Google'da aranıyor: {target_keyword}")
            # Fonksiyonu çalıştır
            df = miner.run_search(target_keyword, max_pages=pages_to_scrape)
            
            status_box.write("✅ Tarama tamamlandı, veriler işleniyor...")
            st.session_state.leads_data = df # Sonucu hafızaya at
            
            status_box.update(label="İşlem Başarılı!", state="complete", expanded=False)
            
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")

    # SONUÇLARI GÖSTER
    if st.session_state.leads_data is not None and not st.session_state.leads_data.empty:
        df = st.session_state.leads_data
        st.success(f"Toplam {len(df)} potansiyel müşteri bulundu.")
        
        st.subheader("📋 Bulunan Firmalar")
        st.dataframe(df, use_container_width=True)
        
        # CSV İndirme Butonu
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Listeyi CSV Olarak İndir",
            data=csv,
            file_name=f'leads_{target_keyword.replace(" ", "_")}.csv',
            mime='text/csv',
        )
    elif st.session_state.leads_data is not None:
        st.warning("Maalesef hiç sonuç bulunamadı. Arama terimini değiştirmeyi dene.")

with col2:
    st.subheader("İstatistikler")
    if st.session_state.leads_data is not None:
        st.metric(label="Bulunan Lead", value=len(st.session_state.leads_data))
    else:
        st.write("Henüz veri yok.")