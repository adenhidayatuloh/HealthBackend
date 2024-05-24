from fastapi import FastAPI, File, UploadFile
from fastai.vision.all import load_learner, PILImage
import io

app = FastAPI()

# Memuat model dari file model.pkl
learn = load_learner('model.pkl')

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):

    wound_details = {
        "Abrasions" : "Luka lecet terjadi ketika lapisan paling atas kulit (epidermis) tergores atau terkikis.Biasanya disebabkan oleh gesekan dengan benda kasar seperti aspal, lantai, atau benda tajam tumpul.Umumnya luka lecet bersifat dangkal, dengan pendarahan minimal dan sembuh dengan cepat.",
        "Bruises" : "Memar terjadi akibat pecahnya pembuluh darah di bawah permukaan kulit tanpa robekan pada kulit.Biasanya disebabkan oleh benturan benda tumpul.Awalnya berwarna merah kebiruan, kemudian berubah menjadi kuning kehijauan dan kuning sebelum akhirnya hilang.",
        "Burns":"Luka bakar terjadi akibat kerusakan jaringan kulit dan jaringan di bawahnya yang disebabkan oleh panas (api, benda panas), listrik, bahan kimia, atau sinar matahari (sunburn).Luka bakar dikategorikan berdasarkan tingkat keparahannya (derajat I, II, dan III).",
        "Cut":"Luka sayatan terjadi akibat robekan pada kulit yang disebabkan oleh benda tajam.Luka sayatan biasanya berdarah lebih banyak dibanding luka lecet.Kedalaman luka sayatan bervariasi tergantung jenis benda tajam yang menyebabkannya.",
        "Diabetic Wounds":"Luka Diabetes adalah luka terbuka pada kaki yang terjadi pada penderita diabetes.Disebabkan oleh kerusakan saraf dan aliran darah yang buruk pada penderita diabetes.Luka diabetes dapat menjadi serius jika tidak ditangani dengan baik dan bisa menyebabkan komplikasi seperti infeksi hingga amputasi.",
        "Laseration": "Luka robek terjadi akibat robekan yang dalam dan tidak rata pada jaringan kulit, otot, atau organ dalam akibat benda tajam.Luka robek biasanya membutuhkan perawatan medis untuk menutup luka dan mencegah infeksi.",
        "Normal":"Tidak ada luka",
        "Pressure Wounds": "Luka yang terjadi akibat tekanan berkepanjangan pada kulit.Biasanya terjadi pada orang yang harus duduk atau berbaring dalam waktu lama, terutama pada lansia atau penderita yang lumpuh.Mencegah tekanan dan menjaga aliran darah penting untuk mencegah luka ini.",
        "Surgical Wounds": "Luka operasi adalah robekan yang disengaja pada kulit dan jaringan di bawahnya yang dibuat oleh dokter untuk prosedur pembedahan.Luka operasi biasanya sembuh dengan perawatan yang tepat dan meninggalkan bekas luka.",
        "Venous Wounds": "Luka pembuluh vena merupakan luka terbuka yang terjadi pada kaki akibat aliran darah vena yang tidak lancar.Biasanya terjadi pada orang yang menderita gangguan pada sistem vena, seperti insufisiensi vena kronis."
    }

    wound_solutions = {
        "Abrasions": [
            "Selalu cuci tangan dengan sabun dan air mengalir sebelum dan sesudah menangani luka.",
            "Gunakan sarung tangan steril jika memungkinkan.",
            "Bersihkan luka dengan air mengalir dan sabun.",
            "Oleskan salep antibiotik.",
            "Tutup luka dengan perban steril.",
            "Ganti perban secara teratur, jaga luka tetap bersih dan kering.",
            "Konsultasikan dengan dokter jika luka parah, dalam, atau menunjukkan tanda-tanda infeksi (memerah, bengkak, panas, bernanah, berbau).",
        ],
        "Bruises": [
            "Selalu cuci tangan dengan sabun dan air mengalir sebelum dan sesudah menangani luka.",
            "Gunakan sarung tangan steril jika memungkinkan.",
            "Kompres dingin area memar selama 20 menit, beberapa kali sehari untuk mengurangi bengkak.",
            "Tinggikan area memar untuk mengurangi aliran darah ke area tersebut.",
            "Hindari aktivitas yang dapat memperparah memar.",
            "Gunakan obat pereda nyeri seperti paracetamol atau ibuprofen jika diperlukan.",
            "Konsultasikan dengan dokter jika luka parah, dalam, atau menunjukkan tanda-tanda infeksi (memerah, bengkak, panas, bernanah, berbau).",
        ],
        "Burns": [
            "Selalu cuci tangan dengan sabun dan air mengalir sebelum dan sesudah menangani luka.",
            "Gunakan sarung tangan steril jika memungkinkan.",
            "Segera dinginkan luka bakar dengan air dingin selama 20 menit (jangan gunakan es).",
            "Lepaskan pakaian dan perhiasan di sekitar luka bakar.",
            "Tutup luka bakar dengan perban steril yang longgar.",
            "Jangan mengoleskan apapun pada luka bakar, termasuk salep atau minyak.",
            "Segera ke dokter untuk luka bakar yang parah atau luas.",
            "Konsultasikan dengan dokter jika luka bakar menunjukkan tanda-tanda infeksi (memerah, bengkak, panas, bernanah, berbau).",
        ],
        "Cut": [
            "Selalu cuci tangan dengan sabun dan air mengalir sebelum dan sesudah menangani luka.",
            "Gunakan sarung tangan steril jika memungkinkan.",
            "Hentikan pendarahan dengan menekan area luka dengan kain bersih selama 5-10 menit.",
            "Bersihkan luka dengan air mengalir dan sabun.",
            "Oleskan salep antibiotik.",
            "Tutup luka dengan perban steril.",
            "Ganti perban secara teratur, jaga luka tetap bersih dan kering.",
            "Jika luka dalam atau berdarah terus, segera ke dokter untuk dijahit.",
            "Konsultasikan dengan dokter jika luka menunjukkan tanda-tanda infeksi (memerah, bengkak, panas, bernanah, berbau).",
        ],
        "Diabetic Wounds": [
            "Selalu cuci tangan dengan sabun dan air mengalir sebelum dan sesudah menangani luka.",
            "Gunakan sarung tangan steril jika memungkinkan.",
            "Bersihkan luka dengan air mengalir dan sabun.",
            "Oleskan salep antibiotik.",
            "Tutup luka dengan perban steril.",
            "Ganti perban secara teratur, jaga luka tetap bersih dan kering.",
            "Kontrol gula darah dengan baik.",
            "Hindari tekanan pada area luka.",
            "Rutin periksa kaki ke dokter untuk memantau kondisi luka.",
            "Konsultasikan dengan dokter jika luka menunjukkan tanda-tanda infeksi (memerah, bengkak, panas, bernanah, berbau).",
        ],
        "Laseration": [
            "Selalu cuci tangan dengan sabun dan air mengalir sebelum dan sesudah menangani luka.",
            "Gunakan sarung tangan steril jika memungkinkan.",
            "Hentikan pendarahan dengan menekan area luka dengan kain bersih selama 5-10 menit.",
            "Bersihkan luka dengan air mengalir dan sabun.",
            "Oleskan salep antibiotik.",
            "Tutup luka dengan perban steril.",
            "Ganti perban secara teratur, jaga luka tetap bersih dan kering.",
            "Jika luka dalam atau berdarah terus, segera ke dokter untuk dijahit.",
            "Konsultasikan dengan dokter jika luka menunjukkan tanda-tanda infeksi (memerah, bengkak, panas, bernanah, berbau).",
        ],
        "Pressure Wounds": [
            "Selalu cuci tangan dengan sabun dan air mengalir sebelum dan sesudah menangani luka.",
            "Gunakan sarung tangan steril jika memungkinkan.",
            "Hindari tekanan pada area luka.",
                    "Ganti posisi secara teratur untuk menghindari tekanan pada satu area.",
            "Jaga kebersihan kulit.",
            "Gunakan kasur khusus untuk mencegah ulkus dekubitus.",
            "Konsultasikan dengan dokter untuk perawatan luka yang tepat.",
            "Konsultasikan dengan dokter jika luka menunjukkan tanda-tanda infeksi (memerah, bengkak, panas, bernanah, berbau).",
        ],
        "Surgical Wounds": [
            "Selalu cuci tangan dengan sabun dan air mengalir sebelum dan sesudah menangani luka.",
            "Gunakan sarung tangan steril jika memungkinkan.",
            "Ikuti instruksi dokter tentang cara merawat luka operasi.",
            "Jaga luka tetap bersih dan kering.",
            "Ganti perban sesuai anjuran dokter.",
            "Minum obat pereda nyeri jika diperlukan.",
            "Konsultasikan dengan dokter jika ada tanda-tanda infeksi (memerah, bengkak, panas, bernanah, berbau).",
        ],
        "Venous Wounds": [
            "Selalu cuci tangan dengan sabun dan air mengalir sebelum dan sesudah menangani luka.",
            "Gunakan sarung tangan steril jika memungkinkan.",
            "Tinggikan kaki saat istirahat untuk meningkatkan aliran darah vena.",
            "Gunakan stoking kompresi untuk membantu aliran darah vena.",
            "Konsultasikan dengan dokter untuk perawatan luka yang tepat.",
            "Hindari berdiri atau duduk dalam waktu lama.",
            "Rutin berolahraga untuk meningkatkan aliran darah.",
            "Konsultasikan dengan dokter jika luka menunjukkan tanda-tanda infeksi (memerah, bengkak, panas, bernanah, berbau).",
        ],
    }       
    img_bytes = await file.read()
    img = PILImage.create(io.BytesIO(img_bytes))
    
    # Melakukan prediksi
    pred_class, pred_idx, outputs = learn.predict(img)
    pred_class = str(pred_class)
   
    
    return {"predicted_class": pred_class,"wound_detail" : wound_details[pred_class], "solution" :wound_solutions[pred_class]}

# Untuk menjalankan server, gunakan perintah berikut di terminal:
# uvicorn main:app --reload

 #uvicorn main:app --host 0.0.0.0 --port 8000

 