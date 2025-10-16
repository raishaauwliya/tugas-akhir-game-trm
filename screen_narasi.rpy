screen narasi_tengah(teks):
    # background kertas
    add "gui/image/bg b.png" xalign 0.5 yalign 0.5

    # teks di tengah kertas
    text teks:
        xalign 0.5
        yalign 0.5
        size 42
        color "#333333"             # abu gelap, biar lembut di mata
        outlines [(2, "#ffffff", 0, 0)]
        font "gui/fonts/Poppins-SemiBold.ttf"  # ganti font kamu kalau ada
        text_align 0.5
        slow_cps 40                 # efek teks berjalan (huruf per huruf)
