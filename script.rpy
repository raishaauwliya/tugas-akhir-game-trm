define niko = Character('Niko', color="#da7c11")
define rara = Character('Rara', color="#bc1473")
define adrian = Character('Adrian', color="#054a19")
define siti = Character('Siti', color="#7777e2")
define pak_karto = Character('Pak Karto', color="#4F492B")
define bu_sari = Character('Bu Sari', color="#8c0e0e")
define pak_ardi = Character('Pak Ardi', color="#e0a80e")
define warga1 = Character('Warga 1', color="#000000")
define warga2 = Character('Warga 2', color="#000000")
define warga3 = Character('Warga 3', color="#0A0A0A")

define left_position  = Position(xalign=0.05, yalign=0.8)
define right_position = Position(xalign=0.95, yalign=0.8)

label choose_language:
    menu:
        "Pilih Bahasa / Choose Language":
            pass
        "Bahasa Indonesia":
            $ renpy.change_language(None)      # bahasa sumber (ID)
        "English":
            $ renpy.change_language("english")  # aktifkan terjemahan EN
    return

label start:
    call choose_language
    play audio "audio/sound.mp3" fadein 1.0

    scene bg a

    "Suasana ruang klub terasa hangat dan penuh semangat."
    show adrian senyum at left_position
    adrian "Halo teman-teman! Selamat datang di Klub Sahabat Alam. Di sini, kita kan belajar bagaimana cara menjaga alam dan juga cara menghadapi bencana alam supaya kita tetap aman."
    
    hide adrian
    with dissolve

    show siti senyum at right_position
    siti "Iya, betul banget, Adrian. Di Indonesia, kita punya banyak sekali keindahan alam, tapi juga ada bencana yang kadang terjadi, seperti longsor dan banjir. Jadi, penting banget kita tahu cara menghadapinya."

    hide siti
    with dissolve

    show pak karto senyum at left_position
    pak_karto "Wah, saya senang melihat semangat dan antusias kalian! Nah, kalian mau mulai belajar dari yang mana dulu? Longsor atau banjir?"

    menu:
        "Belajar tentang Longsor":
            jump scene_longsor

        "Belajar tentang Banjir":
            jump scene_banjir

label scene_longsor:

    scene bg b

    show text Text(
        "Pada liburan sekolah yang cerah, Rara gadis kecil usia 11 tahun tiba di Desa Lereng Damai bersama keluarganya. "
        "Desa ini berada di kaki gunung yang megah, dikelilingi pepohonan hijau dan udara yang sejuk. "
        "Rara bersemangat memulai petualangan di tempat liburannya, tapi ia juga merasa sedikit cemas.",
        size=36,
        color="#179940",
        slow=True,          # aktifkan animasi teks berjalan
        slow_cps=30,        # kecepatan huruf (character per second)
        xalign=0.5,         # posisikan di tengah horizontal
        yalign=-0.1,         # posisikan di tengah vertical
        text_align=0.5,     # rata tengah isi teks
        justify=True,       # paragraf rata kiri-kanan
        xmaximum=900,       # lebar maksimal teks
        line_spacing=10,    # jarak antar baris
        layout="subtitle"
    )

    $ renpy.pause(20.0)
    hide text
    with dissolve

    scene bg c
    with dissolve


    show rara senang at right_position
    rara "Wow, desa ini indah sekali, Niko! Tapi kenapa bukitnya terlihat curam ya?"
    hide rara
    with dissolve

    show niko info at left_position
    niko "Iya Rara, bukit ini memang curam. Kita harus hati-hati saat hujan!"
    hide niko
    with dissolve

    show rara mikir at right_position
    rara "Emang kenapa jika hujan Niko? apa yang akan terjadi?"
    hide rara
    with dissolve

    show niko info2 at left_position
    niko "Kalau hujan deras, tanah bisa longsor! Ayo, aku ajak kamu ke sekolah untuk belajar lebih banyak tentang tanah longsor!"
    hide niko
    with dissolve
    
    scene bg d
    with dissolve

    # Bu Sari muncul bicara dulu
    show bu sari senyum at left_position
    bu_sari "Anak-anak, hari ini kita akan belajar tentang tanah longsor. Siapa yang tahu apa itu bencana tanah longsor?"

    # Ganti ke Rara
    hide bu sari
    with dissolve

    show rara mikir at right_position
    rara "Tanah longsor itu ketika tanah bergerak turun dari bukit, kan, Bu?"

    # Kembalikan Bu Sari bicara lagi
    hide rara
    with dissolve

    show bu sari info at left_position
    bu_sari "Iya, betul sekali! Tanah longsor adalah pergerakan massa tanah atau batuan di lereng bukit atau gunung. Ini bisa berbahaya, apalagi di tempat yang banyak rumah. Salah satu penyebabnya adalah curah hujan yang tinggi."

    # Ganti ke Niko
    hide bu sari
    with dissolve

    show niko mikir at right_position
    niko "Jadi, kalau hujan terus-menerus, itu bisa menyebabkan longsor ya, Bu?"

    # Kembalikan lagi ke Bu Sari
    hide niko
    with dissolve

    show bu sari info at left_position 
    bu_sari "Tepat sekali, Niko! Selain hujan, lereng yang curam juga membuat longsor lebih mudah terjadi karena gaya pendorongnya lebih besar daripada gaya penahannya."

    scene bg e
    with dissolve

    show pak ardi senyum at left_position
    pak_ardi "Terima kasih adik-adik sudah datang di Program Menanam Pohon! Menanam pohon itu penting untuk mencegah longsor. Jika kita menjaga lingkungan kita artinya kita juga melindungi desa kita."

    hide pak ardi
    with dissolve

    show rara bingung at right_position
    rara "Kenapa pohon bisa membantu mencegah longsor, Pak?"

    hide rara
    with dissolve

    show pak ardi info at left_position
    pak_ardi "Pohon bisa mencegah longsor karena akar pohon mengikat tanah agar tidak mudah terbawa air. Saat hujan turun, akar bekerja seperti jaring yang menahan tanah. Tanpa pohon, tanah mudah longsor saat hujan deras."

    pak_ardi "Selain itu, pohon menyerap air hujan lewat daunnya. Ini mengurangi limpasan air yang bisa menyebabkan erosi. Semakin banyak pohon, semakin aman desa kita."

    hide pak ardi
    with dissolve

    show niko senang at right_position
    niko "Aku tidak sabar lihat pohon-pohon ini tumbuh besar! Desa kita akan jadi lebih hijau dan aman!"

    hide niko
    with dissolve

    scene bg f
    with dissolve

    show niko panik at left_position
    niko "Lihat, Rara! Ada retakan di tanah itu. Itu tanda bahaya!"

    hide niko
    with dissolve

    show rara mikir at right_position
    rara "Apa yang harus kita lakukan, Niko?"

    hide rara
    with dissolve

    # === Pilihan Pemain ===
    menu:
        "Ayo langsung laporkan ke Pak Ardi!":
            jump scene_2_4_1

        "Tunggu dulu, ini cuma retakan kecil.":
            jump scene_2_4_2

label scene_2_4_1:
    scene bg g
    with dissolve

    show pak ardi panik at left_position
    pak_ardi "Bagus, kalian cepat melapor! Kita akan pasang tanda peringatan di sini."

    hide pak ardi
    with dissolve

    show niko bahagia at right_position
    niko "Lihat, Rara! Laporan kita menyelamatkan warga!"

    hide niko
    with dissolve

    show rara senyum at right_position
    rara "Iya! Kita berhasil mencegah kecelakaan!"

    hide rara
    with dissolve
    jump scene_evacuation

label scene_2_4_2:
    scene bg h
    with dissolve

    show niko sedih at left_position
    niko "Lihat, Rara! Retakannya membesar setelah hujan tadi malam!"

    hide niko
    with dissolve

    show pak ardi marah at left_position
    pak_ardi "Kalian sudah tahu sejak kemarin? Kenapa tidak dilapor? Sekarang kita harus perbaikan darurat, itu terlalu membahayakan!"

    hide pak ardi
    with dissolve

    show rara kecewa at right_position
    rara "Maaf, Pak… kami tidak tahu ini akan memburuk secepat ini."

    hide rara
    with dissolve
    jump scene_evacuation

    label scene_evacuation:

    # Background baru: papan jalur evakuasi / lapangan sekolah
    scene bg i
    with dissolve

    show bu sari ngajar at left_position
    bu_sari "Anak-anak, jalur evakuasi adalah rute menuju tempat aman saat bencana. Titik kumpul kita ada di lapangan sekolah yang aman dari longsor. Penting untuk tahu jalur ini supaya bisa bergerak cepat dan aman."

    bu_sari "Kalau terdengar alarm atau sirine, langkah pertama adalah tetap tenang. Ikuti rambu evakuasi yang ada."

    hide bu sari
    with dissolve

    show niko mikir at right_position
    niko "Kalau ada teman yang jatuh, bagaimana Bu?"

    hide niko
    with dissolve

    show bu sari info at left_position
    bu_sari "Bantu temanmu dan pastikan semua mengikuti jalur evakuasi. Keselamatan bersama adalah yang utama!"

    hide bu sari
    with dissolve

    scene bg j
    with dissolve

    show niko mantau at left_position
    niko "Hujannya deras banget! Kita harus segera ke tempat aman!"

    hide niko
    with dissolve

    show rara mikir at right_position
    rara "Tapi bagaimana kalau ada longsor?"

    hide rara
    with dissolve

    show bu sari senyum at left_position
    bu_sari "Tenang saja, kita sudah belajar cara evakuasi. Ayo ikuti jalur yang sudah kita pelajari! Segera ke titik kumpul!"

    hide bu sari
    with dissolve

    show rara takut at right_position
    rara "Aku takut… jalannya licin…"

    hide rara
    with dissolve

    # === Pilihan Pemain ===
    menu:
        "Tetap tenang dan ikuti jalur evakuasi.":
            jump scene_2_6_1

        "Panik dan lari sembarangan.":
            jump scene_2_6_2

label scene_2_6_1:

    scene bg k
    with dissolve

    show niko info2 at left_position
    niko "Pelankan langkah! Jangan sampai terpeleset!"

    hide niko
    with dissolve

    show rara senyum at right_position
    rara "Benar… lebih baik hati-hati daripada jatuh."

    hide rara
    with dissolve

    show bu sari senyum at left_position
    bu_sari "Bagus! Kalian semua selamat karena tidak panik."

    hide bu sari
    with dissolve

    jump scene_refleksi_longsor

label scene_2_6_2:

    scene bg l
    with dissolve

    show rara sedih at right_position
    rara "Aduh! Kaki… kakiku terkilir!"

    hide rara
    with dissolve

    show niko mantau at left_position
    niko "Sudah kubilang jangan lari! Aku bantu ke pos kesehatan!"

    hide niko
    with dissolve

    show bu sari marah at left_position
    bu_sari "Ini risiko kalau tidak ikuti prosedur evakuasi."

    hide bu sari
    with dissolve

    jump scene_refleksi_longsor

label scene_refleksi_longsor:

    scene bg m
    with dissolve

    show pak ardi nyimak at left_position
    pak_ardi "Terima kasih kepada semua yang hadir. Kita harus belajar dari pengalaman ini dan meningkatkan kesadaran tentang bahaya tanah longsor."
    hide pak ardi
    with dissolve

    show niko senang at right_position
    niko "Kita harus terus menjaga lingkungan agar tidak ada lagi longsor! Menanam pohon dan menjaga kebersihan saluran air itu penting."
    hide niko
    with dissolve

    show warga1 at left_position
    warga1 "Bagaimana kalau kita mengadakan pelatihan evakuasi setiap bulan? Agar semua orang tahu apa yang harus dilakukan saat terjadi bencana."
    hide warga1
    with dissolve

    show warga2 at right_position
    warga2 "Dan kita bisa membentuk kelompok relawan untuk membantu saat terjadi bencana!"
    hide warga2
    with dissolve

    show rara senang at right_position
    rara "Kita semua bisa menjadi pahlawan bagi desa ini! Dengan pengetahuan dan kerja sama, kita bisa melindungi diri dan tetangga kita."
    hide rara
    with dissolve

    show pak ardi senyum at left_position
    pak_ardi "Betul sekali, Rara! Kesadaran masyarakat sangat penting dalam mitigasi bencana. Kita perlu memahami tiga aspek utama: pengetahuan, sikap, dan perilaku."
    hide pak ardi
    with dissolve

    scene bg b
    show text Text(
        "Setelah melalui berbagai pengalaman dan pembelajaran tentang tanah longsor, Rara, Niko dan warga sekitar di Desa Lereng Damai menyadari betapa pentingnya kesadaran akan bencana ini. Mereka belajar bahwa tanah longsor adalah pergerakan massa tanah yang dapat terjadi akibat curah hujan tinggi, gempa bumi, atau kondisi lereng yang tidak stabil. Melalui simulasi evakuasi dan kegiatan menanam pohon, mereka memahami bahwa tindakan pencegahan seperti menjaga lingkungan dan mengikuti prosedur evakuasi sangatlah penting untuk keselamatan diri dan orang lain.",
        size=36,
        color="#179940",
        slow=True,          # aktifkan animasi teks berjalan
        slow_cps=30,        # kecepatan huruf (character per second)
        xalign=0.5,         # posisikan di tengah horizontal
        yalign=-0.05,         # posisikan di tengah vertical
        text_align=0.5,     # rata tengah isi teks
        justify=True,       # paragraf rata kiri-kanan
        xmaximum=900,       # lebar maksimal teks
        line_spacing=10,    # jarak antar baris
        layout="subtitle"
    )

    $ renpy.pause(20.0)
    hide text
    with dissolve

    return

label scene_banjir:

    scene bg b

    show text Text(
        "Pada suatu hari yang cerah di bulan November, Rara, seorang gadis kecil berusia 11 tahun, tiba di Desa Lereng Damai bersama keluarganya. Desa ini dikelilingi oleh sungai yang mengalir tenang dan sawah hijau yang luas. Rara sangat bersemangat memulai petualangan di tempat liburannya. Namun, ia mendengar dari warga bahwa desa ini sering terkena banjir saat musim hujan tiba.",
        size=36,
        color="#179940",
        slow=True,          # aktifkan animasi teks berjalan
        slow_cps=30,        # kecepatan huruf (character per second)
        xalign=0.5,         # posisikan di tengah horizontal
        yalign=-0.1,         # posisikan di tengah vertical
        text_align=0.5,     # rata tengah isi teks
        justify=True,       # paragraf rata kiri-kanan
        xmaximum=900,       # lebar maksimal teks
        line_spacing=10,    # jarak antar baris
        layout="subtitle"
    )

    $ renpy.pause(20.0)
    hide text
    with dissolve

    # Deskripsi: Jalan desa asri, sawah hijau, sungai lebar, anak-anak bermain, burung beterbangan
    scene bg n
    with dissolve

    show rara senang at right_position
    rara "Wow, desa ini indah sekali! Tapi kenapa sungainya terlihat begitu besar?"
    hide rara
    with dissolve

    show niko info at left_position
    niko "Sungai ini memang besar, Rara. Saat hujan deras, airnya sering meluap dan membanjiri desa."
    hide niko
    with dissolve

    show rara mikir at right_position
    rara "Banjir? Apa itu berbahaya?"
    hide rara
    with dissolve

    show niko info2 at left_position
    niko "Iya! Kalau tidak hati-hati, banjir bisa merusak rumah dan sawah kita. Ayo aku ajak kamu ke sekolah untuk belajar lebih banyak tentang banjir!"
    hide niko
    with dissolve

    jump scene_3_2

label scene_3_2:

    scene bg d
    with dissolve

    show bu sari ngajar at left_position
    bu_sari "Anak-anak, hari ini kita akan belajar tentang banjir. Siapa yang tahu apa itu banjir?"
    hide bu sari
    with dissolve

    show niko mikir at right_position
    niko "Itu saat air meluap dan menggenangi jalan atau rumah, kan Bu?"
    hide niko
    with dissolve

    show bu sari info at left_position
    bu_sari "Betul sekali Niko! Banjir terjadi ketika air meluap dari sungai atau hujan turun sangat deras sehingga tanah tidak bisa menyerapnya."
    bu_sari "Penyebab banjir ada beberapa: pertama, curah hujan yang tinggi; kedua, saluran air tersumbat sampah; ketiga, hutan di hulu sungai ditebang."
    hide bu sari
    with dissolve

    show rara mikir at right_position
    rara "Jadi kalau kita buang sampah sembarangan, itu bisa menyebabkan banjir ya, Bu?"
    hide rara
    with dissolve

    show bu sari senyum at left_position
    bu_sari "Betul sekali! Sampah yang menyumbat saluran air membuat air tidak bisa mengalir lancar."
    hide bu sari
    with dissolve

    jump scene_3_3

# [3.3] Kebun Desa (Menanam Pohon)
label scene_3_3:

    # Deskripsi: lahan terbuka dekat sungai, warga & anak bawa bibit, ember/cangkul/pupuk
    scene bg o
    with dissolve

    show pak ardi senyum at left_position
    pak_ardi "Terima kasih sudah datang! Menanam pohon sangat penting untuk mencegah banjir. Pohon membantu menyerap air hujan dan mencegah erosi tanah."
    hide pak ardi
    with dissolve

    show rara senyum at right_position
    rara "Kenapa pohon bisa membantu mencegah banjir, Pak?"
    hide rara
    with dissolve

    show pak ardi info at left_position
    pak_ardi "Akar pohon menyerap air hujan sehingga tanah tidak cepat jenuh air. Pohon juga memperlambat aliran air ke sungai, jadi sungai tidak langsung meluap."
    hide pak ardi
    with dissolve

    show niko senang at right_position
    niko "Ayo kita tanam bersama! Semakin banyak pohon kita tanam, semakin aman desa kita dari banjir!"
    hide niko
    with dissolve

    jump scene_3_4


# [3.4] Tepi Sungai (Air Naik)
label scene_3_4:

    # Deskripsi: sungai keruh, air naik, awan gelap, suara air deras
    scene bg p
    with dissolve

    show niko panik at left_position
    niko "Lihat Rara! Air sungainya mulai naik dan warnanya keruh. Ini tanda bahaya!"
    hide niko
    with dissolve

    show rara bingung at right_position
    rara "Iya, Lalu apa yang harus kita lakukan Niko?"
    hide rara
    with dissolve

    menu:
        "Ayo langsung laporkan ke Pak Ardi!":
            jump scene_3_4_1

        "Tunggu dulu, sepertinya tidak akan sampai naik terlalu tinggi.":
            jump scene_3_4_2


# [3.4.1] Lapor Cepat
label scene_3_4_1:

    # Deskripsi: warga berkumpul, Pak Ardi memberi instruksi, anak-anak bantu info
    scene bg q
    with dissolve

    show pak ardi panik at left_position
    pak_ardi "Perhatian semua warga! Air sungai mulai naik. Segera siapkan barang-barang penting dan bersiap untuk evakuasi ke tempat aman!"
    hide pak ardi
    with dissolve

    show niko senang at right_position
    niko "Bagus sekali, Rara! Kita berhasil memberi tahu orang-orang tepat waktu!"
    hide niko
    with dissolve

    jump scene_3_5


# [3.4.2] Terlambat Melapor
label scene_3_4_2:

    # Deskripsi: air meluap ke jalan, warga panik
    scene bg r
    with dissolve

    show rara sedih at right_position
    rara "Oh tidak! Airnya sudah sampai ke jalan!"
    hide rara
    with dissolve

    show niko sedih at left_position
    niko "Kita seharusnya melapor lebih awal! Sekarang banyak orang yang kesulitan!"
    hide niko
    with dissolve

    jump scene_3_5


# [3.5] Lapangan Sekolah (Simulasi Evakuasi)
label scene_3_5:

    # Deskripsi: lapangan jauh dari sungai, peta jalur evakuasi, rambu hijau
    scene bg s
    with dissolve

    show bu sari ngajar at left_position
    bu_sari "Anak-anak, hari ini kita akan simulasi evakuasi banjir. Jalur evakuasi penting untuk membawa kita ke tempat aman."
    bu_sari "Kalau ada peringatan banjir, segera ambil barang-barang penting seperti dokumen, obat, dan makanan ringan."
    hide bu sari
    with dissolve

    show rara mikir at right_position
    rara "Kalau air sudah masuk ke rumah, Bu?"
    hide rara
    with dissolve

    show bu sari info at left_position
    bu_sari "Segera keluar dan cari tempat lebih tinggi. Jangan tunggu air makin tinggi. Jangan bawa barang berat yang menghambat gerak."
    hide bu sari
    with dissolve

    show niko senang at right_position
    niko "Dan jangan lupa membantu keluarga atau teman yang kesulitan!"
    hide niko
    with dissolve

    show bu sari senyum at left_position
    bu_sari "Tepat sekali! Kalau di sekolah, ikuti petunjuk guru atau petugas keamanan. Yang penting jangan panik, saling membantu, dan tetap tertib."
    hide bu sari
    with dissolve

    jump scene_3_6


# [3.6] Desa (Air Meluap)
label scene_3_6:

    # Deskripsi: air mulai masuk halaman rumah, warga evakuasi barang, suara hujan deras
    scene bg t
    with dissolve

    show pak ardi senyum at left_position
    pak_ardi "Warga Desa Lereng Damai! Air sungai meluap, banjir akan segera datang! Kita harus siap-siap evakuasi!"
    hide pak ardi
    with dissolve

    show rara bingung at right_position
    rara "Airnya sudah sampai ke halaman rumah! Apa yang harus kita lakukan?"
    hide rara
    with dissolve

    menu:
        "Segera ambil barang berharga dan keluar dari rumah!":
            jump scene_3_6_1

        "Tunggu sebentar dan lihat apakah airnya naik.":
            jump scene_3_6_2


# [3.6.1] Bertindak Cepat
label scene_3_6_1:

    # Deskripsi: warga berjalan ke titik aman, anak bawa ransel
    scene bg u
    with dissolve

    show rara senyum at right_position
    rara "Aku senang kita langsung bergerak! Sekarang aku tahu apa yang harus dilakukan saat banjir."
    hide rara
    with dissolve

    show niko senang at left_position
    niko "Kita berhasil sampai di tempat aman sebelum air naik!"
    hide niko
    with dissolve

    show bu sari senyum at left_position
    bu_sari "Bagus! Kalian selamat karena bertindak cepat dan tertib. Ini contoh yang benar saat darurat."
    hide bu sari
    with dissolve

    jump scene_3_7


# [3.6.2] Terlambat Evakuasi
label scene_3_6_2:

    # Deskripsi: air masuk rumah setinggi meja, barang mengambang
    scene bg u
    with dissolve

    show rara kecewa at right_position
    rara "Oh tidak! Airnya sudah sampai ke meja!"
    hide rara
    with dissolve

    show niko panik at left_position
    niko "Kita seharusnya tidak menunggu! Sekarang banyak barang rusak!"
    hide niko
    with dissolve

    show bu sari pasrah at left_position
    bu_sari "Kita harus belajar dari ini. Jangan tunda tindakan saat banjir, keselamatan itu yang utama."
    hide bu sari
    with dissolve

    jump scene_3_7


# [3.7] Balai Desa (Refleksi)
label scene_3_7:

    # Deskripsi: warga duduk di balai desa, papan ide & spanduk "Jaga Lingkungan, Cegah Banjir"
    scene bg m
    with dissolve

    show pak ardi senyum at left_position
    pak_ardi "Kita harus belajar dari pengalaman ini. Banjir bukan hanya karena hujan, tapi juga karena kita kurang peduli lingkungan."
    hide pak ardi
    with dissolve

    show niko senang at right_position
    niko "Kita harus menjaga saluran air tetap bersih. Ayo adakan kegiatan bersih-bersih tiap minggu!"
    hide niko
    with dissolve

    show warga1 at left_position
    warga1 "Bagaimana kalau kita bikin kelompok relawan kebersihan sungai?"
    hide warga1
    with dissolve

    show warga2 at right_position
    warga2 "Kita juga bisa mengadakan pelatihan rutin tentang bencana!"
    hide warga2
    with dissolve

    show pak ardi senyum at left_position
    pak_ardi "Bagus! Selain itu, mari tanam lebih banyak pohon di hulu sungai."
    hide pak ardi
    with dissolve

    show bu sari senyum at right_position
    bu_sari "Kita juga perlu mengajari anak-anak pentingnya menjaga lingkungan."
    hide bu sari
    with dissolve

    show niko info at left_position
    niko "Ayo buat poster dan spanduk larangan buang sampah sembarangan!"
    hide niko
    with dissolve

    show warga3 at right_position
    warga3 "Setuju! Kita juga bisa buat sumur resapan untuk menyerap air hujan."
    hide warga3
    with dissolve

    show pak ardi senyum at left_position
    pak_ardi "Dengan kerja sama, desa kita akan lebih siap menghadapi banjir. Mari kita mulai sekarang!"
    hide pak ardi
    with dissolve

    # Narasi akhir
    scene bg b
    show text Text(
         "Melalui pengalaman ini, Rara, Niko, dan warga Desa Lereng Damai belajar bahwa menjaga lingkungan adalah kunci mencegah banjir. Menanam pohon, membersihkan saluran air, dan mengenali tanda bahaya adalah langkah penting untuk melindungi diri dan masyarakat. Dengan kerja sama seluruh warga, desa mereka bisa lebih aman dari banjir di masa depan.",
        size=36,
        color="#179940",
        slow=True,          # aktifkan animasi teks berjalan
        slow_cps=30,        # kecepatan huruf (character per second)
        xalign=0.5,         # posisikan di tengah horizontal
        yalign=-0.1,         # posisikan di tengah vertical
        text_align=0.5,     # rata tengah isi teks
        justify=True,       # paragraf rata kiri-kanan
        xmaximum=900,       # lebar maksimal teks
        line_spacing=10,    # jarak antar baris
        layout="subtitle"
    )

    $ renpy.pause(20.0)
    hide text
    with dissolve

    # Selesai → kembali ke Klub/awal
