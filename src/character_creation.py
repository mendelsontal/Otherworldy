# src/character_creation.py
import pygame
import os
from .player import Player
from .character_preview import CharacterPreview
from .intro import play_intro

def run_character_creation(screen, font, screen_width, screen_height):
    """
    Step-by-step character creation:
     1) Enter name (text)
     2) Choose gender (← / →, Enter to confirm)
     3) Choose hair (← / →) with live preview
     4) Confirm (Enter) -> returns Player instance
     Press Esc during steps to cancel and return None.
    """
    clock = pygame.time.Clock()

    # state
    name = ""
    gender_options = ["Male", "Female"]
    gender_index = 0
    hair_folders = _get_hair_folders()
    hair_index = 0

    preview = CharacterPreview(font, screen_width, screen_height)
    state = "name"   # "name" -> "gender" -> "hair" -> finish

    while True:
        screen.fill((10, 10, 10))

        # draw UI per state
        if state == "name":
            _draw_centered(screen, font, "Enter character name:", y=100)
            name_surf = font.render(name, True, (255, 220, 80))
            screen.blit(name_surf, (50, 180))

        elif state == "gender":
            _draw_centered(screen, font, "Select gender:", y=100)
            for i, g in enumerate(gender_options):
                color = (255,255,0) if i == gender_index else (200,200,200)
                gsurf = font.render(g, True, color)
                screen.blit(gsurf, (screen_width//2 - gsurf.get_width()//2, 200 + i*60))

        elif state == "hair":
            _draw_centered(screen, font, "Select hair style:", y=40)
            # draw live preview of full character
            current_hair = hair_folders[hair_index] if hair_folders else None
            preview.draw_preview(screen, gender=gender_options[gender_index], hair=current_hair)
            # draw hair folder name small
            if current_hair:
                hair_text = font.render(current_hair, True, (200,200,200))
                screen.blit(hair_text, (50, screen_height - 80))

        pygame.display.flip()

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                # universal cancel
                if event.key == pygame.K_ESCAPE:
                    if state == "name":
                        return None
                    elif state == "gender":
                        state = "name"
                    elif state == "hair":
                        state = "gender"
                    continue

                if state == "name":
                    if event.key == pygame.K_RETURN:
                        state = "gender"
                    elif event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        if event.unicode and event.unicode.isprintable():
                            name += event.unicode

                elif state == "gender":
                    if event.key == pygame.K_UP:
                        gender_index = (gender_index - 1) % len(gender_options)
                    elif event.key == pygame.K_DOWN:
                        gender_index = (gender_index + 1) % len(gender_options)
                    elif event.key == pygame.K_RETURN:
                        state = "hair"

                elif state == "hair":
                    if hair_folders:
                        if event.key == pygame.K_LEFT:
                            hair_index = (hair_index - 1) % len(hair_folders)
                        elif event.key == pygame.K_RIGHT:
                            hair_index = (hair_index + 1) % len(hair_folders)
                        elif event.key == pygame.K_RETURN:
                            return Player(
                                name=name or "Hero",
                                gender=gender_options[gender_index],
                                hair_style=hair_folders[hair_index],
                                clothing_style="Default"
                            )
                            intro = IntroScene(screen)
                            intro.play()
                            return player
                    else:
                        if event.key == pygame.K_RE1TURN:
                            return Player(
                                name=name or "Hero",
                                gender=gender_options[gender_index],
                                hair_style=None,
                                clothing_style="Default"
                            )
                            intro = IntroScene(screen)
                            intro.play()
                            return player

        clock.tick(60)


def _get_hair_folders():
    hair_root = os.path.join("assets", "images", "Characters", "Hair")
    if not os.path.exists(hair_root):
        return []
    return sorted([d for d in os.listdir(hair_root) if os.path.isdir(os.path.join(hair_root, d))])

def _draw_centered(screen, font, text, y=20):
    surf = font.render(text, True, (200,200,200))
    screen.blit(surf, (screen.get_width()//2 - surf.get_width()//2, y))
