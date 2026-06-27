# Project options for 《风暴中的大顺朝：垂暮》

define config.name = "风暴中的大顺朝：垂暮"
define config.version = "0.1.0-prologue"
define build.name = "chuimuo_visual_novel"

define config.has_sound = True
define config.has_music = True
define config.has_voice = False

define config.main_menu_music = None
define config.default_fullscreen = False
define config.window_title = "风暴中的大顺朝：垂暮"

# Web-friendly behavior: avoid desktop-only assumptions and rely on Ren'Py web storage.
define config.save_directory = "chuimuo_visual_novel_saves"
define config.autosave_on_quit = True
define config.thumbnail_width = 384
define config.thumbnail_height = 216

# 待美术素材就位：bg_mainmenu.webp
define gui.main_menu_background = "images/background/bg_mainmenu.webp"
