import pygame
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from config import screen_width, screen_height,explode_side_size,enenmy_health_bar_height,enenmy_health_bar_width
from src.engine.game import Game
from src.engine.menu import Menu, GameModeMenu, MapCharacterMenu,MultiplayerMapCharacterMenu
from src.engine.multiplayer_game import Game_2
from src.engine.menu import Menu

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("BrawlForge")


try:
    icon = pygame.image.load("src/assets/images/icon.jpg")
    pygame.display.set_icon(icon)
except FileNotFoundError:
    print("Warning: Icon image not found. Continuing without icon.")

try:
    background = pygame.image.load("src/assets/images/BrawlhalaBackground.jpg")
    background = pygame.transform.scale(background, (screen_width, screen_height))
    platform_image_path = "src/assets/images/"
    platform_images = {
        'left': pygame.image.load(os.path.join(platform_image_path, "platform_left.png")).convert_alpha(),
        'middle': pygame.image.load(os.path.join(platform_image_path, "platform_middle.png")).convert_alpha(),
        'right': pygame.image.load(os.path.join(platform_image_path, "platform_right.png")).convert_alpha(),
        'solid': pygame.image.load(os.path.join(platform_image_path, "platform_solid.png")).convert_alpha(),
    }   

except (FileNotFoundError, pygame.error) as e:
    print(f"Error: Could not load asset: {e}")
    pygame.quit()
    exit() 

while True:
    menu = Menu(screen, background)
    menu_action = menu.run()
    if menu_action == "start":
        mode_menu = GameModeMenu(screen, background)
        mode = mode_menu.run()
        if mode == "single":
            single_player_menu = MapCharacterMenu(screen, background, hero_profile_picture) # تغییر اینجا
            result = single_player_menu.run() 
            
            if result[0] == "exit": 
                continue

            selected_char, selected_map, _ = result
            game=Game(screen,platform_images,background)
        elif mode == "multi": 
            multi_player_menu = MultiplayerMapCharacterMenu(screen, background, hero_profile_picture) # تغییر اینجا
            result = multi_player_menu.run()

            if result[0] == "exit": 
                continue

            selected_char_list, selected_map, _ = result 
            player1_char_name = selected_char_list[0]
            player2_char_name = selected_char_list[1]

            player1_start_pos = levels_module.get_start_position(selected_map, player_index=1)
            player2_start_pos = levels_module.get_start_position(selected_map, player_index=2) 

            hero1 = None
            hero2 = None
            if player1_char_name == "Roboman":
                hero1 = Roboman(player1_start_pos['x'], player1_start_pos['y'],
                                roboman_health_bar_frame, roboman_health_bar, hero_profile_picture,
                                screen_width, screen_height, sounds=game_sounds)
            elif player1_char_name == "NinjaGirl":
                hero1 = NinjaGirl(player1_start_pos['x'], player1_start_pos['y'],
                                  screen_width, screen_height, [], ninja_health_bar_frame, ninja_health_bar)
            elif player1_char_name == "Ninja":
                hero1 = Ninja(player1_start_pos['x'], player1_start_pos['y'],
                              screen_width, screen_height, [], ninja_health_bar_frame, ninja_health_bar)
            elif player1_char_name == "Archer":
                hero1 = Archer(player1_start_pos['x'], player1_start_pos['y'],
                               screen_width, screen_height, [], archer_health_bar_frame, archer_health_bar)

            if player2_char_name == "Roboman":
                hero2 = Roboman(player2_start_pos['x'], player2_start_pos['y'],
                                roboman_health_bar_frame, roboman_health_bar, hero_profile_picture,
                                screen_width, screen_height, sounds=game_sounds)
            elif player2_char_name == "NinjaGirl":
                hero2 = NinjaGirl(player2_start_pos['x'], player2_start_pos['y'],
                                  screen_width, screen_height, [], ninja_health_bar_frame, ninja_health_bar)
            elif player2_char_name == "Ninja":
                hero2 = Ninja(player2_start_pos['x'], player2_start_pos['y'],
                              screen_width, screen_height, [], ninja_health_bar_frame, ninja_health_bar)
            elif player2_char_name == "Archer":
                hero2 = Archer(player2_start_pos['x'], player2_start_pos['y'],
                               screen_width, screen_height, [], archer_health_bar_frame, archer_health_bar)
            game = Game_2(
                screen,
                platform_images,
                background, explode_picture,
                game_sounds,
                ninja_health_bar_frame, ninja_health_bar,
                roboman_health_bar_frame, roboman_health_bar,
                hero_profile_picture, 
                selected_map , hero1=hero1,hero2=hero2
            )

        elif mode == "exit":
            pygame.quit()
            sys.exit() 
        else:
            continue 

    elif menu_action == "settings":
        print("Settings menu not implemented yet!")
    elif menu_action == "exit":
        pygame.quit()
        sys.exit() 

    if 'game' in locals() and game: 
        game_result = game.run() 
        if game_result == "menu":
            continue
        elif game_result == "exit":
            pygame.quit()
            sys.exit() 
    
    
    