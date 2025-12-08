## FILE: game/audio_toggle.rpy (FIXED - Menggunakan _preferences.volumes)

screen quick_voice_toggle():
    layer "overlay"
    zorder 10

    # Cek apakah tidak di main menu
    if not main_menu:

        # --- PERBAIKAN DI SINI ---
        # Kita menggunakan _preferences.volumes (pakai underscore di depan).
        # Ini adalah dictionary asli Python, jadi .get() PASTI BERHASIL.
        $ current_vol = _preferences.volumes.get("voice", 1.0)
        $ is_voice_enabled = current_vol > 0.0

        fixed:
            xalign 0.98
            yalign 0.28

            frame:
                padding (10, 10)
                background Solid("#00000000")

                hbox:
                    textbutton ("🔊" if is_voice_enabled else "🔇"):
                        style "quick_button"

                        action If(is_voice_enabled,
                            Preference("voice volume", 0.0), # Matikan
                            Preference("voice volume", 1.0)  # Nyalakan
                        )
                        hovered Show("quick_voice_toggle")

# Daftarkan screen overlay
init python:
    if "quick_voice_toggle" not in config.overlay_screens:
        config.overlay_screens.append("quick_voice_toggle")