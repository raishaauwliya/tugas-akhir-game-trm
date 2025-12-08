# FILE: game/script.rpy (Final - Rapi + STT + Karakter)

init python:
    import os, json, subprocess, string, math, re
    from collections import Counter

    # -----------------------------
    # 1) Fungsi Speech-to-Text (STT)
    # -----------------------------
    
    # --- STT Helper Functions ---
    def parse_stt_output(raw_out):
        renpy.log("Raw STT: {}".format(raw_out))

        try:
            data = json.loads(raw_out)
        except Exception as e:
            renpy.log("JSON error: {}".format(e))
            return None

        if not data.get("ok"):
            renpy.log("STT error: {}".format(data.get("error")))
            return None

        text = data.get("text") or ""
        return text.strip()
    
    def run_stt(lang_code="id-ID"):
        # Path ke stt_worker.py di root project
        script_path = os.path.join(config.basedir, "stt_worker.py")

        # >>> GANTI path ini jadi python.exe yang bener punyamu <<<
        python_exe = r"C:\Users\raish\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe"

        if not os.path.isfile(script_path):
            renpy.notify("stt_worker.py tidak ditemukan.")
            return None

        # --- Siapkan agar jendela CMD tidak muncul di Windows ---
        startupinfo = None
        creationflags = 0
        if renpy.windows:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            # hide console window
            creationflags = subprocess.CREATE_NO_WINDOW

        cmd = [python_exe, script_path, "--lang", lang_code]

        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                startupinfo=startupinfo,
                creationflags=creationflags,
            )
            # Batasi max 30 detik
            raw_out, raw_err = proc.communicate(timeout=30.0)
        except subprocess.TimeoutExpired:
            renpy.notify("STT timeout (terlalu lama).")
            return None
        except Exception as e:
            renpy.notify("STT gagal dijalankan: {}".format(e))
            return None

        raw_out = raw_out.strip()
        if not raw_out:
            renpy.notify("STT tidak mengembalikan output.")
            return None

        return parse_stt_output(raw_out)


    # -----------------------------
    # 2) Util: normalisasi & cosine similarity
    # -----------------------------
    def _normalize_text(text):
        if not text:
            return []

        # bikin huruf kecil semua
        text = text.lower()

        # buang karakter non-huruf/angka (tanda baca, dsb)
        text = re.sub(r"[^\w\s]", " ", text)

        # split per spasi & buang token kosong
        tokens = [w for w in text.split() if w]

        # hilangin duplikat berurutan (optional tapi bagus)
        dedup = []
        for w in tokens:
            if not dedup or dedup[-1] != w:
                dedup.append(w)

        return dedup


    def _cosine_similarity(words_a, words_b):
        ca = Counter(words_a)
        cb = Counter(words_b)
        all_words = set(ca) | set(cb)
        dot = sum(ca[w] * cb[w] for w in all_words)
        norm_a = math.sqrt(sum(v * v for v in ca.values()))
        norm_b = math.sqrt(sum(v * v for v in cb.values()))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        # Rumus Cosine Similarity:
        # dot product / (norm_a * norm_b)
        return dot / (norm_a * norm_b)
    
    def format_spoken(value):
        """Mengubah input dari STT menjadi string yang aman untuk renpy.notify."""
        if value is None:
            return "Tidak ada suara."
        if isinstance(value, str):
            text = value.strip()
            return text if text else "Tidak ada suara."
        if isinstance(value, (list, tuple)):
            if len(value) == 0:
                return "Tidak ada suara."
            return ", ".join(str(x) for x in value)
        return str(value)

    # -----------------------------
    # 3) Fungsi Utama Pemilih Menu Suara
    # -----------------------------
    def voice_menu_choice(
    option_texts,
    lang_code="id-ID",
    min_overlap=1,
    threshold=0.35,
    keyword_map=None
    ):
        # 1. Dapatkan input suara
        spoken = run_stt(lang_code=lang_code)
        if not spoken:
            return None
        renpy.log("STT recognized: '{}'".format(spoken))

        spoken_tokens = _normalize_text(spoken)
        renpy.notify("Kamu bilang: '{}'".format(spoken))

        # 2. Cek Kata Kunci (Keyword Mapping)
        if keyword_map:
            hits = []
            for idx, keywords in keyword_map.items():
                for kw in keywords:
                    if kw.lower() in spoken_tokens:
                        hits.append(idx)
                        break

            # Kalau hanya satu yang kena keyword → langsung pilih
            if len(hits) == 1:
                return hits[0]

            # Kalau tidak ada keyword yang ketemu → gagal (kembalikan None)
            if len(hits) == 0:
                renpy.notify("Tidak ada kata kunci pilihan yang terdeteksi.")
                return None

        # 3. Cosine similarity terhadap semua opsi
        best_idx = None
        best_score = None

        for idx, opt_text in enumerate(option_texts):
            opt_tokens = _normalize_text(opt_text)

            # minimal jumlah kata yang sama (overlap)
            overlap = len(set(spoken_tokens) & set(opt_tokens))
            if overlap < min_overlap:
                continue

            score = _cosine_similarity(spoken_tokens, opt_tokens)

            if (best_score is None) or (score > best_score):
                best_score = score
                best_idx = idx

        # 4. Filter dengan threshold confidence
        if best_idx is not None and best_score is not None:
            if best_score >= threshold:
                renpy.notify("Pilihanmu: {} (Score: {:.2f})".format(option_texts[best_idx], best_score))
                return best_idx
            else:
                renpy.notify("Suara kurang mirip dengan pilihan yang ada (Score: {:.2f})".format(best_score))
                return None

        # Tidak ada yang lolos min_overlap
        renpy.notify("Tidak ada kata yang cukup tumpang tindih dengan pilihan yang tersedia.")
        return None
    

# ====================================================================
# DEFINISI KARAKTER DAN POSISI
# ====================================================================

define niko = Character('Niko', color="#FFFFFF")
define rara = Character('Rara', color="#FFFFFF")
define adrian = Character('Adrian', color="#FFFFFF")
define siti = Character('Siti', color="#FFFFFF")
define pak_karto = Character('Pak Karto', color="#FFFFFF")
define bu_sari = Character('Bu Sari', color="#FFFFFF")
define pak_ardi = Character('Pak Ardi', color="#FFFFFF")
define warga1 = Character('Warga 1', color="#FFFFFF")
define warga2 = Character('Warga 2', color="#FFFFFF")
define warga3 = Character('Warga 3', color="#FFFFFF")

define left_position  = Position(xalign=0.05, yalign=0.8)
define right_position = Position(xalign=0.95, yalign=0.8)


# ====================================================================
# SCREEN: STT LISTENING MENU
# ====================================================================
# Screen ini dipanggil saat STT aktif.

screen stt_listening_menu(options):
    modal True              # Biar pemain nggak bisa klik apa-apa dulu
    zorder 100              # Di atas UI lain (paling depan)

    window:
        style "menu_window"   # Agar mirip tampilan menu biasa

        vbox:
            spacing 15
            xalign 0.5
            yalign 0.5

            text "Silakan ucapkan pilihanmu..." style "menu_prompt"

            text "Contoh: \"Belajar tentang longsor\" atau \"Belajar tentang banjir\"." size 22

            null height 15

            text "Pilihan yang tersedia:" size 24

            # Tampilkan daftar opsi seperti menu (tapi tidak bisa diklik)
            for o in options:
                text "• [o]" style "menu_choice_button_text"

            null height 20

            text "Mendengarkan..." italic True
    
    

# ====================================================================
# SCREEN & LABEL: PILIH BAHASA
# ====================================================================

label choose_language:

    # Di layar pilih bahasa, sistem Next dimatikan dulu
    $ next_lock = False

    # variabel penampung pilihan bahasa
    $ language_queued = None

    # panggil screen khusus pilih bahasa
    call screen choose_language_screen

    # terapkan bahasa sesuai pilihan
    if language_queued is None:
        $ renpy.change_language(None)        # Bahasa Indonesia (sumber)
    else:
        $ renpy.change_language(language_queued)

    # setelah lewat layar bahasa, hidupkan lagi sistem Next
    $ next_lock = True

    return


screen choose_language_screen():

    tag menu                # supaya menggantikan menu lain
    modal True              # player harus pilih dulu

    style_prefix "choice"   # pakai style tombol menu biasa (biru)

    vbox:
        xalign 0.5
        yalign 0.1
        spacing 10
        # === JUDUL (TIDAK BISA DIKLIK, TANPA BAR BIRU) ===
        text "Pilih Bahasa / Choose Language":
            size 40
            color "#FFFFFF"
            xalign 0.5

        # === PILIHAN BAHASA (TOMBOL BIRU) ===
        vbox:
            spacing 15
            xalign 0.5

            textbutton "Bahasa Indonesia":
                # Mengganti bahasa dan kembali (Return())
                action [ Function(renpy.change_language, None), Return() ]

            textbutton "English":
                # Mengganti bahasa dan kembali (Return())
                action [ Function(renpy.change_language, "english"), Return() ]

# ====================================================================
# ALUR CERITA UTAMA DIMULAI
# ====================================================================

label start:
    call choose_language
    
    # Atur volume BGM dan loop (BGM TIDAK dimatikan oleh tombol voice toggle)
    $ renpy.music.set_volume(0.4, delay=0, channel='music')
    play music "audio/sound.mp3" fadein 1.0 loop

    scene bg a

    "Suasana ruang klub terasa hangat dan penuh semangat."
    show adrian senyum at left_position
    play sound "audio/ID/Adrian 1.mp3"
    adrian "Halo teman-teman! Selamat datang di Klub Sahabat Alam. Di sini, kita akan belajar bagaimana cara menjaga alam dan juga cara menghadapi bencana alam supaya kita tetap aman."
    hide adrian
    with dissolve
    stop sound fadeout 1.0

    show siti senyum at right_position
    play sound "audio/ID/Siti 1.mp3"
    siti "Iya, betul banget, Adrian. Di Indonesia, kita punya banyak sekali keindahan alam, tapi juga ada bencana yang kadang terjadi, seperti longsor dan banjir. Jadi, penting banget kita tahu cara menghadapinya."
    hide siti
    with dissolve
    stop sound fadeout 1.0

    show pak karto senyum at left_position
    play sound "audio/ID/Pak Karto 1.mp3"
    pak_karto "Wah, saya senang melihat semangat dan antusias kalian! Nah, kalian mau mulai belajar dari yang mana dulu? Longsor atau banjir?"
    hide pak karto 
    with dissolve
    stop sound fadeout 1.0
    
    jump pilih_bencana

# ====================================================================
# PILIHAN BENCANA (LONGOSOR / BANJIR)
# ====================================================================

label pilih_bencana:    
    show pak karto senyum at left_position
    $ renpy.notify("Silakan ucapkan pilihanmu. Kamu bisa mengatakan:")
    $ renpy.pause(1.0)
    $ renpy.notify("Klik mouse untuk mulai mendengarkan.")
    pak_karto "Katakan topik apa yang ingin kamu pelajari:\n• Belajar tentang Longsor\n• Belajar tentang Banjir"
    jump stt_bencana
    
label stt_bencana:
    # --- VOICE MENU: Longsor vs Banjir ---
    $ pilihan_teks = [
        "Belajar tentang Longsor",
        "Belajar tentang Banjir",
    ]

    # Kata kunci khusus
    $ keyword_map = {
        0: ["longsor"],
        1: ["banjir"],
    }
    
    # Ulangi sampai ada pilihan yang valid
    while True:
        # Panggil fungsi STT
        $ idx = voice_menu_choice(
            pilihan_teks,
            lang_code="id-ID",
            min_overlap=1,
            threshold=0.35,
            keyword_map=keyword_map
        )

        if idx == 0:
            jump scene_longsor
        elif idx == 1:
            jump scene_banjir

        # Kalau gagal → kasih feedback lalu ulang
        show pak karto senyum at left_position
        pak_karto "Maaf, saya tidak menangkap pilihanmu. Mari kita coba lagi."

        jump pilih_bencana   # ulangi dari awal label

# ====================================================================
# ALUR CERITA: LONGSOR
# ====================================================================

label scene_longsor:

    scene bg b
    play sound "audio/ID/Narasi 1.mp3"
    show text Text(
        "Pada liburan sekolah yang cerah, Rara gadis kecil usia 11 tahun tiba di Desa Lereng Damai bersama keluarganya. Desa ini berada di kaki gunung yang megah, dikelilingi pepohonan hijau dan udara yang sejuk. Rara bersemangat memulai petualangan di tempat liburannya, tapi ia juga merasa sedikit cemas.",
        size=36,
        color="#179940",
        slow=True,          
        slow_cps=13,        
        xalign=0.5,         
        yalign=-0.1,         
        text_align=0.5,     
        justify=True,       
        xmaximum=900,       
        line_spacing=10,    
        layout="subtitle"
    )

    $ renpy.pause(20.0)
    hide text
    with dissolve

    scene bg c
    with dissolve


    show rara senang at right_position
    play sound "audio/ID/Rara 1.mp3"
    rara "Wow, desa ini indah sekali, Niko! Tapi kenapa bukitnya terlihat curam ya?"
    hide rara
    with dissolve
    stop sound fadeout 1.0


    show niko info at left_position
    play sound "audio/ID/Niko 1.mp3"
    niko "Iya Rara, bukit ini memang curam. Kita harus hati-hati saat hujan!"
    hide niko
    with dissolve
    stop sound fadeout 1.0

    show rara mikir at right_position
    play sound "audio/ID/Rara 2.mp3"
    rara "Emang kenapa jika hujan Niko? apa yang akan terjadi?"
    hide rara
    with dissolve
    stop sound fadeout 1.0

    show niko info2 at left_position
    play sound "audio/ID/Niko 2.mp3"
    niko "Kalau hujan deras, tanah bisa longsor! Ayo, aku ajak kamu ke sekolah untuk belajar lebih banyak tentang tanah longsor!"
    hide niko
    with dissolve
    stop sound fadeout 1.0
    
    scene bg d
    with dissolve

    # Bu Sari muncul bicara dulu
    show bu sari senyum at left_position
    play sound "audio/ID/Bu Sari 3.mp3"
    bu_sari "Anak-anak, hari ini kita akan belajar tentang tanah longsor. Siapa yang tahu apa itu bencana tanah longsor?"

    # Ganti ke Rara
    hide bu sari
    with dissolve
    stop sound fadeout 1.0

    show rara mikir at right_position
    play sound "audio/ID/Rara 3.mp3"
    rara "Tanah longsor itu ketika tanah bergerak turun dari bukit, kan, Bu?"

    # Kembalikan Bu Sari bicara lagi
    hide rara
    with dissolve
    stop sound fadeout 1.0

    show bu sari info at left_position
    play sound "audio/ID/Bu Sari 1.mp3"
    bu_sari "Iya, betul sekali! Tanah longsor adalah pergerakan massa tanah atau batuan di lereng bukit atau gunung. Ini bisa berbahaya, apalagi di tempat yang banyak rumah. Salah satu penyebabnya adalah curah hujan yang tinggi."

    # Ganti ke Niko
    hide bu sari
    with dissolve
    stop sound fadeout 1.0

    show niko mikir at right_position
    play sound "audio/ID/Niko 3.mp3"
    niko "Jadi, kalau hujan terus-menerus, itu bisa menyebabkan longsor ya, Bu?"

    # Kembalikan lagi ke Bu Sari
    hide niko
    with dissolve
    stop sound fadeout 1.0

    show bu sari info at left_position 
    play sound "audio/ID/Bu Sari 2.mp3"
    bu_sari "Tepat sekali, Niko! Selain hujan, lereng yang curam juga membuat longsor lebih mudah terjadi karena gaya pendorongnya lebih besar daripada gaya penahannya."

    scene bg e
    with dissolve
    stop sound fadeout 1.0

    show pak ardi senyum at left_position
    play sound "audio/ID/Pak Ardi 1.mp3"
    pak_ardi "Terima kasih adik-adik sudah datang di Program Menanam Pohon! Menanam pohon itu penting untuk mencegah longsor. Jika kita menjaga lingkungan kita artinya kita juga melindungi desa kita."

    hide pak ardi
    with dissolve
    stop sound fadeout 1.0

    show rara bingung at right_position
    play sound "audio/ID/Rara 4.mp3"
    rara "Kenapa pohon bisa membantu mencegah longsor, Pak?"

    hide rara
    with dissolve
    stop sound fadeout 1.0

    show pak ardi info at left_position
    play sound "audio/ID/Pak Ardi 2.mp3"
    pak_ardi "Pohon bisa mencegah longsor karena akar pohon mengikat tanah agar tidak mudah terbawa air. Saat hujan turun, akar bekerja seperti jaring yang menahan tanah. Tanpa pohon, tanah mudah longsor saat hujan deras."
    play sound "audio/ID/Pak Ardi 3.mp3"
    pak_ardi "Selain itu, pohon menyerap air hujan lewat daunnya. Ini mengurangi limpasan air yang bisa menyebabkan erosi. Semakin banyak pohon, semakin aman desa kita."

    hide pak ardi
    with dissolve
    stop sound fadeout 1.0

    show niko senang at right_position
    play sound "audio/ID/Niko 4.mp3"
    niko "Aku tidak sabar lihat pohon-pohon ini tumbuh besar! Desa kita akan jadi lebih hijau dan aman!"

    hide niko
    with dissolve
    stop sound fadeout 1.0

    scene bg f
    with dissolve

    show niko panik at left_position
    play sound "audio/ID/Niko 5.mp3"
    niko "Lihat, Rara! Ada retakan di tanah itu. Itu tanda bahaya!"

    hide niko
    with dissolve
    stop sound fadeout 1.0

    show rara mikir at left_position
    play sound "audio/ID/Rara 5.mp3"
    rara "Apa yang harus kita lakukan, Niko?"
    stop sound fadeout 1.0

    hide rara
    with dissolve
    
    jump pilih_longsor_1

label pilih_longsor_1:
    show niko info at left_position
    $ renpy.notify("Silakan ucapkan pilihanmu. Kamu bisa mengatakan:")
    $ renpy.pause(1.0)
    $ renpy.notify("Klik mouse untuk mulai mendengarkan.")
    niko "Katakan Tindakan apa yang ingin kamu ambil?\n• Ayo langsung laporkan ke Pak Ardi!\n• Tunggu dulu, ini cuma retakan kecil."

    jump stt_longsor_1
    
label stt_longsor_1:
    # --- VOICE MENU: Lapor vs Tunggu ---
    $ pilihan_teks = [
        "Ayo langsung laporkan ke Pak Ardi!",
        "Tunggu dulu, ini cuma retakan kecil.",
    ]

    # Kata kunci khusus
    $ keyword_map = {
        0: ["ayo", "langsung", "lapor", "laporkan", "pak", "ardi"],
        1: ["tunggu", "dulu", "ini", "cuma", "retakan", "kecil"],
    }
    
    while True:
        $ idx = voice_menu_choice(
            pilihan_teks,
            lang_code="id-ID",
            min_overlap=3,
            threshold=0.35,
            keyword_map=keyword_map
        )

        if idx == 0:
            jump scene_2_4_1
        elif idx == 1:
            jump scene_2_4_2

        # Kalau gagal → kasih feedback lalu ulang
        show niko info at left_position
        niko "Maaf, saya tidak menangkap pilihanmu. Mari kita coba lagi."

        jump pilih_longsor_1   # ulangi dari awal label

label scene_2_4_1:
    scene bg g
    with dissolve

    show pak ardi panik at left_position
    play sound "audio/ID/Pak Ardi 4.mp3"
    pak_ardi "Bagus, kalian cepat melapor! Kita akan pasang tanda peringatan di sini."

    hide pak ardi
    with dissolve
    stop sound fadeout 1.0

    show niko bahagia at left_position
    play sound "audio/ID/Niko 6.mp3"
    niko "Lihat, Rara! Laporan kita menyelamatkan warga!"

    hide niko
    with dissolve
    stop sound fadeout 1.0

    show rara senyum at left_position
    play sound "audio/ID/Rara 6.mp3"
    rara "Iya! Kita berhasil mencegah kecelakaan!"

    hide rara
    with dissolve
    stop sound fadeout 1.0
    jump scene_evacuation

label scene_2_4_2:
    scene bg h
    with dissolve

    show niko sedih at right_position
    play sound "audio/ID/Niko 7.mp3"
    niko "Lihat, Rara! Retakannya membesar setelah hujan tadi malam!"

    hide niko
    with dissolve

    show pak ardi marah at right_position
    play sound "audio/ID/Pak Ardi 5.mp3"
    pak_ardi "Kalian sudah tahu sejak kemarin? Kenapa tidak dilapor? Sekarang kita harus perbaikan darurat, itu terlalu membahayakan!"

    hide pak ardi
    with dissolve
    stop sound fadeout 1.0

    show rara kecewa at right_position
    play sound "audio/ID/Rara 7.mp3"
    rara "Maaf, Pak… kami tidak tahu ini akan memburuk secepat ini."

    hide rara
    with dissolve
    stop sound fadeout 1.0
    jump scene_evacuation

label scene_evacuation:

    # Background baru: papan jalur evakuasi / lapangan sekolah
    scene bg i
    with dissolve

    show bu sari ngajar at left_position
    play sound "audio/ID/Bu Sari 4.mp3"
    
    bu_sari "Anak-anak, jalur evakuasi adalah rute menuju tempat aman saat bencana. Titik kumpul kita ada di lapangan sekolah yang aman dari longsor. Penting untuk tahu jalur ini supaya bisa bergerak cepat dan aman."
    play sound "audio/ID/Bu Sari 5.mp3"
    bu_sari "Kalau terdengar alarm atau sirine, langkah pertama adalah tetap tenang. Ikuti rambu evakuasi yang ada."

    hide bu sari
    with dissolve
    stop sound fadeout 1.0

    show niko mikir at right_position
    play sound "audio/ID/Niko 8.mp3"
    niko "Kalau ada teman yang jatuh, bagaimana Bu?"

    hide niko
    with dissolve
    stop sound fadeout 1.0

    show bu sari info at left_position
    play sound "audio/ID/Bu Sari 6.mp3"
    bu_sari "Bantu temanmu dan pastikan semua mengikuti jalur evakuasi. Keselamatan bersama adalah yang utama!"

    hide bu sari
    with dissolve
    stop sound fadeout 1.0

    scene bg j
    with dissolve

    show niko mantau at left_position
    play sound "audio/ID/Niko 9.mp3"
    niko "Hujannya deras banget! Kita harus segera ke tempat aman!"

    hide niko
    with dissolve
    stop sound fadeout 1.0

    show rara mikir at right_position
    play sound "audio/ID/Rara 11.mp3"
    rara "Tapi bagaimana kalau ada longsor?"

    hide rara
    with dissolve
    stop sound fadeout 1.0

    show bu sari senyum at left_position
    play sound "audio/ID/Bu Sari 7.mp3"
    bu_sari "Tenang saja, kita sudah belajar cara evakuasi. Ayo ikuti jalur yang sudah kita pelajari! Segera ke titik kumpul!"

    hide bu sari
    with dissolve
    stop sound fadeout 1.0

    show rara takut at right_position
    play sound "audio/ID/Rara 8.mp3"
    rara "Aku takut… jalannya licin…"

    hide rara
    with dissolve
    stop sound fadeout 1.0

    jump pilih_scene_2_4_2

label pilih_scene_2_4_2:    
    show niko info at left_position
    $ renpy.notify("Silakan ucapkan pilihanmu. Kamu bisa mengatakan:")
    $ renpy.pause(1.0)
    $ renpy.notify("Klik mouse untuk mulai mendengarkan.")
    niko "Tindakan apa yang ingin kamu ambil?\n• Tetap tenang dan ikuti jalur evakuasi.\n• Panik dan lari sembarangan"

    jump stt_scene_2_4_2
    
label stt_scene_2_4_2:
    # --- VOICE MENU: Tenang vs Panik ---
    $ pilihan_teks = [
        "Tetap tenang dan ikuti jalur evakuasi",
        "Panik dan lari sembarangan",
    ]

    # Kata kunci khusus
    $ keyword_map = {
        0: ["tenang", "ikuti", "jalur", "evakuasi"],
        1: ["panik", "lari", "sembarang"],
    }
    
    while True:
        $ idx = voice_menu_choice(
            pilihan_teks,
            lang_code="id-ID",
            min_overlap=3,
            threshold=0.35,
            keyword_map=keyword_map
        )

        if idx == 0:
            jump scene_2_6_1
        elif idx == 1:
            jump scene_2_6_2

        # Kalau gagal → kasih feedback lalu ulang
        show niko info at left_position
        niko "Maaf, saya tidak menangkap pilihanmu. Mari kita coba lagi."

        jump pilih_scene_2_4_2   # ulangi dari awal label
        
label scene_2_6_1:

    scene bg k
    with dissolve

    show niko info2 at left_position
    play sound "audio/ID/Niko 10.mp3"
    niko "Pelankan langkah! Jangan sampai terjatuh!"

    hide niko
    with dissolve
    stop sound fadeout 1.0

    show rara senyum at right_position
    play sound "audio/ID/Rara 9.mp3"
    rara "Benar… lebih baik hati-hati daripada jatuh."

    hide rara
    with dissolve
    stop sound fadeout 1.0

    show bu sari senyum at left_position
    play sound "audio/ID/Bu Sari 8.mp3"
    bu_sari "Bagus! Kalian semua selamat karena tidak panik."

    hide bu sari
    with dissolve
    stop sound fadeout 1.0

    jump scene_refleksi_longsor

label scene_2_6_2:

    scene bg l
    with dissolve

    show rara sedih at right_position
    play sound "audio/ID/Rara 10.mp3"
    rara "Aduh! Kakiku terkilir!"

    hide rara
    with dissolve
    stop sound fadeout 1.0

    show niko mantau at left_position
    play sound "audio/ID/Niko 11.mp3"
    niko "Sudah kubilang jangan lari! Yuk aku bantu ke pos kesehatan!"

    hide niko
    with dissolve
    stop sound fadeout 1.0

    show bu sari marah at left_position
    play sound "audio/ID/Bu Sari 9.mp3"
    bu_sari "Ini risiko kalau tidak ikuti prosedur evakuasi."

    hide bu sari
    with dissolve
    stop sound fadeout 1.0

    jump scene_refleksi_longsor

label scene_refleksi_longsor:

    scene bg m
    with dissolve

    show pak ardi nyimak at left_position
    play sound "audio/ID/Pak Ardi 6.mp3"
    pak_ardi "Terima kasih kepada semua yang hadir. Kita harus belajar dari pengalaman ini dan meningkatkan kesadaran tentang bahaya tanah longsor."
    hide pak ardi
    with dissolve
    stop sound fadeout 1.0

    show niko info2 at right_position
    play sound "audio/ID/Niko 12.mp3"
    niko "Kita harus terus menjaga lingkungan agar tidak ada lagi longsor! Menanam pohon dan menjaga kebersihan saluran air itu penting."
    hide niko
    with dissolve
    stop sound fadeout 1.0

    show warga1 at left_position
    play sound "audio/ID/Warga 1.mp3"
    warga1 "Bagaimana kalau kita mengadakan pelatihan evakuasi setiap bulan? Agar semua orang tahu apa yang harus dilakukan saat terjadi bencana."
    hide warga1
    with dissolve
    stop sound fadeout 1.0

    show warga2 at right_position
    play sound "audio/ID/Warga 2.mp3"
    warga2 "Dan kita bisa membentuk kelompok relawan untuk membantu saat terjadi bencana!"
    hide warga2
    with dissolve
    stop sound fadeout 1.0

    show rara senang at right_position
    play sound "audio/ID/Rara 12.mp3"
    rara "Kita semua bisa menjadi pahlawan bagi desa ini! Dengan pengetahuan dan kerja sama, kita bisa melindungi diri dan tetangga kita."
    hide rara
    with dissolve
    stop sound fadeout 1.0

    show pak ardi senyum at left_position
    play sound "audio/ID/Pak Ardi 7.mp3"
    pak_ardi "Betul sekali, Rara! Kesadaran masyarakat sangat penting dalam mitigasi bencana. Kita perlu memahami tiga aspek utama: pengetahuan, sikap, dan perilaku."
    hide pak ardi
    with dissolve
    stop sound fadeout 1.0

    scene bg b
    play sound "audio/ID/Narasi 2.mp3"
    show text Text(
        "Setelah melalui berbagai pengalaman dan pembelajaran tentang tanah longsor, Rara, Niko dan warga sekitar di Desa Lereng Damai menyadari betapa pentingnya kesadaran akan bencana ini. Mereka belajar bahwa tanah longsor adalah pergerakan massa tanah yang dapat terjadi akibat curah hujan tinggi, gempa bumi, atau kondisi lereng yang tidak stabil. Melalui simulasi evakuasi dan kegiatan menanam pohon, mereka memahami bahwa tindakan pencegahan seperti menjaga lingkungan dan mengikuti prosedur evakuasi sangatlah penting untuk keselamatan diri dan orang lain.",
        size=36,
        color="#179940",
        slow=True,          
        slow_cps=13,        
        xalign=0.5,         
        yalign=-0.05,         
        text_align=0.5,     
        justify=True,       
        xmaximum=900,       
        line_spacing=10,    
        layout="subtitle"
    )

    $ renpy.pause(20.0)
    hide text
    with dissolve

    return

# ====================================================================
# ALUR CERITA: BANJIR
# ====================================================================

label scene_banjir:

    scene bg b
    play sound "audio/ID/Narasi 3.mp3"
    show text Text(
        "Pada suatu hari yang cerah di bulan November, Rara, seorang gadis kecil berusia 11 tahun, tiba di Desa Lereng Damai bersama keluarganya. Desa ini dikelilingi oleh sungai yang mengalir tenang dan sawah hijau yang luas. Rara sangat bersemangat memulai petualangan di tempat liburannya. Namun, ia mendengar dari warga bahwa desa ini sering terkena banjir saat musim hujan tiba.",
        size=36,
        color="#179940",
        slow=True,          
        slow_cps=13,        
        xalign=0.5,         
        yalign=-0.1,         
        text_align=0.5,     
        justify=True,       
        xmaximum=900,       
        line_spacing=10,    
        layout="subtitle"
    )

    $ renpy.pause(20.0)
    hide text
    with dissolve

    # Deskripsi: Jalan desa asri, sawah hijau, sungai lebar, anak-anak bermain, burung beterbangan
    scene bg n
    with dissolve

    show rara senang at right_position
    play sound "audio/ID/Rara 13.mp3"
    rara "Wow, desa ini indah sekali! Tapi kenapa sungainya terlihat begitu besar?"
    hide rara
    with dissolve
    stop sound fadeout 1.0

    show niko info at left_position
    play sound "audio/ID/Niko 13.mp3"
    niko "Sungai ini memang besar, Rara. Saat hujan deras, airnya sering meluap dan membanjiri desa."
    hide niko
    with dissolve
    stop sound fadeout 1.0

    show rara mikir at right_position
    play sound "audio/ID/Rara 14.mp3"
    rara "Banjir? Apa itu berbahaya?"
    hide rara
    with dissolve
    stop sound fadeout 1.0

    show niko info2 at left_position
    play sound "audio/ID/Niko 14.mp3"
    niko "Iya! Kalau tidak hati-hati, banjir bisa merusak rumah dan sawah kita. Ayo aku ajak kamu ke sekolah untuk belajar lebih banyak tentang banjir!"
    hide niko
    with dissolve
    stop sound fadeout 1.0

    jump scene_3_2

label scene_3_2:

    scene bg d
    with dissolve

    show bu sari ngajar at left_position
    play sound "audio/ID/Bu Sari 10.mp3"
    bu_sari "Anak-anak, hari ini kita akan belajar tentang banjir. Siapa yang tahu apa itu banjir?"
    hide bu sari
    with dissolve
    stop sound fadeout 1.0

    show niko mikir at right_position
    play sound "audio/ID/Niko 15.mp3"
    niko "Banjir itu saat air meluap dan menggenangi jalan atau rumah, kan Bu?"
    hide niko
    with dissolve
    stop sound fadeout 1.0

    show bu sari info at left_position
    play sound "audio/ID/Bu Sari 11.mp3"
    bu_sari "Betul sekali Niko! Banjir terjadi ketika air meluap dari sungai atau hujan turun sangat deras sehingga tanah tidak bisa menyerapnya."
    play sound "audio/ID/Bu Sari 12.mp3"
    bu_sari "Penyebab banjir ada beberapa: pertama, curah hujan yang tinggi; kedua, saluran air tersumbat sampah; ketiga, hutan di hulu sungai ditebang."
    hide bu sari
    with dissolve
    stop sound fadeout 1.0

    show rara mikir at right_position
    play sound "audio/ID/Rara 15.mp3"
    rara "Jadi kalau kita buang sampah sembarangan, itu bisa menyebabkan banjir ya, Bu?"
    hide rara
    with dissolve
    stop sound fadeout 1.0

    show bu sari senyum at left_position
    play sound "audio/ID/Bu Sari 13.mp3"
    bu_sari "Betul sekali! Sampah yang menyumbat saluran air membuat air tidak bisa mengalir lancar."
    hide bu sari
    with dissolve
    stop sound fadeout 1.0

    jump scene_3_3

# [3.3] Kebun Desa (Menanam Pohon)
label scene_3_3:

    # Deskripsi: lahan terbuka dekat sungai, warga & anak bawa bibit, ember/cangkul/pupuk
    scene bg o
    with dissolve

    show pak ardi senyum at left_position
    play sound "audio/ID/Pak Ardi 8.mp3"
    pak_ardi "Terima kasih sudah datang! Menanam pohon sangat penting untuk mencegah banjir. Pohon membantu menyerap air hujan dan mencegah erosi tanah."
    hide pak ardi
    with dissolve
    stop sound fadeout 1.0

    show rara senyum at right_position
    play sound "audio/ID/Rara 16.mp3"
    rara "Kenapa pohon bisa membantu mencegah banjir, Pak?"
    hide rara
    with dissolve
    stop sound fadeout 1.0

    show pak ardi info at left_position
    play sound "audio/ID/Pak Ardi 9.mp3"
    pak_ardi "Akar pohon menyerap air hujan sehingga tanah tidak cepat jenuh air. Pohon juga memperlambat aliran air ke sungai, jadi sungai tidak langsung meluap."
    hide pak ardi
    with dissolve
    stop sound fadeout 1.0

    show niko senang at right_position
    play sound "audio/ID/Niko 16.mp3"
    niko "Ayo kita tanam bersama! Semakin banyak pohon kita tanam, semakin aman desa kita dari banjir!"
    hide niko
    with dissolve
    stop sound fadeout 1.0

    jump scene_3_4


# [3.4] Tepi Sungai (Air Naik)
label scene_3_4:

    # Deskripsi: sungai keruh, air naik, awan gelap, suara air deras
    scene bg p
    with dissolve

    show niko panik at left_position
    play sound "audio/ID/Niko 17.mp3"
    niko "Lihat Rara! Air sungainya mulai naik dan warnanya keruh. Ini tanda bahaya!"
    hide niko
    with dissolve
    stop sound fadeout 1.0

    show rara bingung at right_position
    play sound "audio/ID/Rara 17.mp3"
    rara "Iya, Lalu apa yang harus kita lakukan Niko?"
    hide rara
    with dissolve
    stop sound fadeout 1.0
    jump pilih_scene_3_4

label pilih_scene_3_4:    
    show rara bingung at left_position
    $ renpy.notify("Silakan ucapkan pilihanmu. Kamu bisa mengatakan:")
    $ renpy.pause(1.0)
    $ renpy.notify("Klik mouse untuk mulai mendengarkan.")
    rara "Katakan Tindakan apa yang ingin kamu ambil?\n• Ayo langsung laporkan ke Pak Ardi!.\n• Tunggu dulu, sepertinya tidak akan sampai naik terlalu tinggi."

    jump stt_scene_3_4
    
label stt_scene_3_4:
    # --- VOICE MENU: Lapor vs Tunggu ---
    $ pilihan_teks = [
        "Ayo langsung laporkan ke Pak Ardi",
        "Tunggu dulu sepertinya tidak akan sampai naik terlalu tinggi",
    ]

    # Kata kunci khusus
    $ keyword_map = {
        0: ["lapor", "langsung", "pak ardi"],
        1: ["tunggu", "sepertinya", "tidak", "naik"],
    }
    
    while True:
        $ idx = voice_menu_choice(
            pilihan_teks,
            lang_code="id-ID",
            min_overlap=3,
            threshold=0.35,
            keyword_map=keyword_map
        )

        if idx == 0:
            jump scene_3_4_1
        elif idx == 1:
            jump scene_3_4_2

        # Kalau gagal → kasih feedback lalu ulang
        show rara bingung at left_position
        rara "Maaf, saya tidak menangkap pilihanmu. Mari kita coba lagi."

        jump pilih_scene_3_4   # ulangi dari awal label

# [3.4.1] Lapor Cepat
label scene_3_4_1:

    # Deskripsi: warga berkumpul, Pak Ardi memberi instruksi, anak-anak bantu info
    scene bg q
    with dissolve

    show pak ardi panik at left_position
    play sound "audio/ID/Pak Ardi 11.mp3"
    pak_ardi "Perhatian semua warga! Air sungai mulai naik. Segera siapkan barang-barang penting dan bersiap untuk evakuasi ke tempat aman!"
    hide pak ardi
    with dissolve
    stop sound fadeout 1.0

    show niko senang at left_position
    play sound "audio/ID/Niko 18.mp3"
    niko "Bagus sekali, Rara! Kita berhasil memberi tahu orang-orang tepat waktu!"
    hide niko
    with dissolve
    stop sound fadeout 1.0

    jump scene_3_5


# [3.4.2] Terlambat Melapor
label scene_3_4_2:

    # Deskripsi: air meluap ke jalan, warga panik
    scene bg r
    with dissolve

    show rara sedih at right_position
    play sound "audio/ID/Rara 18.mp3"
    rara "Oh tidak! Airnya sudah sampai ke jalan!"
    hide rara
    with dissolve
    stop sound fadeout 1.0

    show niko sedih at left_position
    play sound "audio/ID/Niko 19.mp3"
    niko "Kita seharusnya melapor lebih awal! Sekarang banyak orang yang kesulitan!"
    hide niko
    with dissolve
    stop sound fadeout 1.0

    jump scene_3_5


# [3.5] Lapangan Sekolah (Simulasi Evakuasi)
label scene_3_5:

    # Deskripsi: lapangan jauh dari sungai, peta jalur evakuasi, rambu hijau
    scene bg s
    with dissolve

    show bu sari ngajar at left_position
    play sound "audio/ID/Bu Sari 15.mp3"
    bu_sari "Anak-anak, hari ini kita akan simulasi evakuasi banjir. Jalur evakuasi penting untuk membawa kita ke tempat aman."
    play sound "audio/ID/Bu Sari 16.mp3"
    bu_sari "Kalau ada peringatan banjir, segera ambil barang-barang penting seperti dokumen, obat, dan makanan ringan."
    hide bu sari
    with dissolve
    stop sound fadeout 1.0

    show rara mikir at right_position
    play sound "audio/ID/Rara 19.mp3"
    rara "Kalau air sudah masuk ke rumah, Bu?"
    hide rara
    with dissolve
    stop sound fadeout 1.0

    show bu sari info at left_position
    play sound "audio/ID/Bu Sari 17.mp3"
    bu_sari "Segera keluar dan cari tempat lebih tinggi. Jangan tunggu air makin tinggi. Jangan bawa barang berat yang menghambat gerak."
    hide bu sari
    with dissolve
    stop sound fadeout 1.0

    show niko senang at right_position
    play sound "audio/ID/Niko 20.mp3"
    niko "Dan jangan lupa membantu keluarga atau teman yang kesulitan!"
    hide niko
    with dissolve
    stop sound fadeout 1.0

    show bu sari senyum at left_position
    play sound "audio/ID/Bu Sari 18.mp3"
    bu_sari "Tepat sekali! Kalau di sekolah, ikuti petunjuk guru atau petugas keamanan. Yang penting jangan panik, saling membantu, dan tetap tertib."
    hide bu sari
    with dissolve
    stop sound fadeout 1.0

    jump scene_3_6


# [3.6] Desa (Air Meluap)
label scene_3_6:

    # Deskripsi: air mulai masuk halaman rumah, warga evakuasi barang, suara hujan deras
    scene bg t
    with dissolve

    show pak ardi senyum at left_position
    play sound "audio/ID/Pak Ardi 15.mp3"
    pak_ardi "Warga Desa Lereng Damai! Air sungai meluap, banjir akan segera datang! Kita harus siap-siap evakuasi!"
    hide pak ardi
    with dissolve
    stop sound fadeout 1.0

    show rara bingung at right_position
    play sound "audio/ID/Rara 20.mp3"
    rara "Airnya sudah sampai ke halaman rumah! Apa yang harus kita lakukan?"
    hide rara
    with dissolve
    stop sound fadeout 1.0
    jump pilih_scene_3_6

label pilih_scene_3_6:    
    show niko info at left_position
    $ renpy.notify("Silakan ucapkan pilihanmu. Kamu bisa mengatakan:")
    $ renpy.pause(1.0)
    $ renpy.notify("Klik mouse untuk mulai mendengarkan.")
    niko "Katakan Tindakan apa yang ingin kamu ambil?\n• Segera ambil barang berharga dan keluar dari rumah!.\n• Tunggu sebentar dan lihat apakah airnya naik."

    jump stt_scene_3_6
    
label stt_scene_3_6:
    # --- VOICE MENU: Cepat vs Tunggu ---
    $ pilihan_teks = [
        "Segera ambil barang berharga dan keluar dari rumah",
        "Tunggu sebentar dan lihat apakah airnya naik",
    ]

    # Kata kunci khusus
    $ keyword_map = {
        0: ["ambil", "barang", "keluar"],
        1: ["tunggu", "air", "lihat", "naik"],
    }
    
    while True:
        $ idx = voice_menu_choice(
            pilihan_teks,
            lang_code="id-ID",
            min_overlap=3,
            threshold=0.35,
            keyword_map=keyword_map
        )

        if idx == 0:
            jump scene_3_6_1
        elif idx == 1:
            jump scene_3_6_2

        # Kalau gagal → kasih feedback lalu ulang
        show niko info at left_position
        niko "Maaf, saya tidak menangkap pilihanmu. Mari kita coba lagi."

        jump pilih_scene_3_6   # ulangi dari awal label


# [3.6.1] Bertindak Cepat
label scene_3_6_1:

    # Deskripsi: warga berjalan ke titik aman, anak bawa ransel
    scene bg u
    with dissolve

    show rara senyum at right_position
    play sound "audio/ID/Rara 21.mp3"
    rara "Aku senang kita langsung bergerak! Sekarang aku tahu apa yang harus dilakukan saat banjir."
    hide rara
    with dissolve
    stop sound fadeout 1.0

    show niko senang at left_position
    play sound "audio/ID/Niko 21.mp3"
    niko "Kita berhasil sampai di tempat aman sebelum air naik!"
    hide niko
    with dissolve
    stop sound fadeout 1.0

    show bu sari senyum at left_position
    play sound "audio/ID/Bu Sari 19.mp3"
    bu_sari "Bagus! Kalian selamat karena bertindak cepat dan tertib. Ini contoh yang benar saat darurat."
    hide bu sari
    with dissolve
    stop sound fadeout 1.0

    jump scene_3_7


# [3.6.2] Terlambat Evakuasi
label scene_3_6_2:

    # Deskripsi: air masuk rumah setinggi meja, barang mengambang
    scene bg u
    with dissolve

    show rara kecewa at right_position
    play sound "audio/ID/Rara 22.mp3"
    rara "Oh tidak! Airnya sudah sampai ke meja!"
    hide rara
    with dissolve
    stop sound fadeout 1.0

    show niko panik at left_position
    play sound "audio/ID/Niko 22.mp3"
    niko "Kita seharusnya tidak menunggu! Sekarang banyak barang rusak!"
    hide niko
    with dissolve
    stop sound fadeout 1.0

    show bu sari pasrah at left_position
    play sound "audio/ID/Bu Sari 20.mp3"
    bu_sari "Kita harus belajar dari ini. Jangan tunda tindakan saat banjir, keselamatan itu yang utama."
    hide bu sari
    with dissolve
    stop sound fadeout 1.0

    jump scene_3_7


# [3.7] Balai Desa (Refleksi)
label scene_3_7:

    # Deskripsi: warga duduk di balai desa, papan ide & spanduk "Jaga Lingkungan, Cegah Banjir"
    scene bg m
    with dissolve

    show pak ardi senyum at left_position
    play sound "audio/ID/Pak Ardi 12.mp3"
    pak_ardi "Kita harus belajar dari pengalaman ini. Banjir bukan hanya karena hujan, tapi juga karena kita kurang peduli lingkungan."
    hide pak ardi
    with dissolve
    stop sound fadeout 1.0

    show niko info2 at right_position
    play sound "audio/ID/Niko 23.mp3"
    niko "Kita harus menjaga saluran air tetap bersih. Ayo adakan kegiatan bersih-bersih tiap minggu!"
    hide niko
    with dissolve
    stop sound fadeout 1.0

    show warga1 at left_position
    play sound "audio/ID/Warga 3.mp3"
    warga1 "Bagaimana kalau kita bikin kelompok relawan kebersihan sungai?"
    hide warga1
    with dissolve
    stop sound fadeout 1.0

    show warga3 at right_position
    play sound "audio/ID/Warga 4.mp3"
    warga3 "Kita juga bisa mengadakan pelatihan rutin tentang bencana!"
    hide warga3
    with dissolve
    stop sound fadeout 1.0

    show pak ardi senyum at left_position
    play sound "audio/ID/Pak Ardi 13.mp3"
    pak_ardi "Bagus! Selain itu, mari tanam lebih banyak pohon di hulu sungai."
    hide pak ardi
    with dissolve
    stop sound fadeout 1.0

    show niko info at left_position
    play sound "audio/ID/Niko 24.mp3"
    niko "Ayo buat poster dan spanduk larangan buang sampah sembarangan!"
    hide niko
    with dissolve
    stop sound fadeout 1.0

    show warga2 at right_position
    play sound "audio/ID/Warga 5.mp3"
    warga2 "Setuju! Kita juga bisa buat sumur resapan untuk menyerap air hujan."
    hide warga2
    with dissolve
    stop sound fadeout 1.0

    show pak ardi senyum at left_position
    play sound "audio/ID/Pak Ardi 14.mp3"
    pak_ardi "Dengan kerja sama, desa kita akan lebih siap menghadapi banjir. Mari kita mulai sekarang!"
    hide pak ardi
    with dissolve
    stop sound fadeout 1.0

    # Narasi akhir
    scene bg b
    play sound "audio/ID/Narasi 4.mp3"
    show text Text(
        "Melalui pengalaman ini, Rara, Niko, dan warga Desa Lereng Damai belajar bahwa menjaga lingkungan adalah kunci mencegah banjir. Menanam pohon, membersihkan saluran air, dan mengenali tanda bahaya adalah langkah penting untuk melindungi diri dan masyarakat. Dengan kerja sama seluruh warga, desa mereka bisa lebih aman dari banjir di masa depan.",
        size=36,
        color="#179940",
        slow=True,          
        slow_cps=30,        
        xalign=0.5,         
        yalign=-0.1,         
        text_align=0.5,     
        justify=True,       
        xmaximum=900,       
        line_spacing=10,    
        layout="subtitle"
    )

    $ renpy.pause(20.0)
    hide text
    with dissolve

    return