import pygame as pg
from maxym import TextureButton

font = pg.font.Font(None, 36)
back_button_from_htp = TextureButton(630, 300, 230, 100, "assets\\textures\\ui\\back2.png")

def render_text_with_spacing(text, font, color, spacing):
    text_surface = pg.Surface((font.size(text)[0] + spacing * (len(text) - 1), font.size(text)[1]), pg.SRCALPHA)

    x_offset = 0

    for char in text:
        char_surface = font.render(char, True, color)
        text_surface.blit(char_surface, (x_offset, 0))
        x_offset += char_surface.get_width() + spacing

    return text_surface

def display_rules(window):
    window.fill((135, 95, 22))
    
    rules = [
        "Сложность игры можно настроить в настройках.",
        "Темные блоки не ломаются. Только белые!.",
        "Правила гри: Отбивайтесь от вражеских танков защищая свою базу!",
        "Вверх - W",
        "Вниз - S",
        "Направо - D",
        "Налево - A",
        "Стрелять - R"
    ]
    
    font_path = r"fonts\tankrusbyme.otf"
    font_size = 36
    font = pg.font.Font(font_path, font_size)
    
    text_color = (255, 255, 255)
    letter_spacing = 5

    y_offset = 50
    for rule in rules:
        text = render_text_with_spacing(rule, font, text_color, letter_spacing)
        window.blit(text, (50, y_offset))
        y_offset += text.get_height() + 20
    
    back_button_from_htp.draw(window)

    pg.display.flip()
    
    
    # вывод кнопки и текста на экран
    #button_rect = display_rules(window)
    # test coment 