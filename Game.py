import pygame, sys, random

collision = 0
# TODO Task 1 Make the paddle bigger
player_width = 200
shrink_amount = 20

def ball_movement(dificult):
    """
    Handles the movement of the ball and collision detection with the player and screen boundaries.
    """
    global ball_speed_x, ball_speed_y, score, easy_high_score, medium_high_score,hard_high_score, endless_high_score, start,collision,flash_timer, game_state, shrink_amount
    global morewidth_powerup_active,morewidth_powerup_rect,less_speed_powerup_active,less_speed_powerup_rect

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    max_speed = 30
    ball_speed_x = max(-max_speed, min(ball_speed_x, max_speed)) #caps the speed
    ball_speed_y = max(-max_speed, min(ball_speed_y, max_speed)) #caps the speed

    # Start the ball movement when the game begins
    # TODO Task 5 Create a Merge Conflict
    speed = 7
    if start:
        ball_speed_x = speed * random.choice((1, -1))  # Randomize initial horizontal direction
        ball_speed_y = speed * random.choice((1, -1))  # Randomize initial vertical direction
        start = False


    # Ball collision with the player paddle
    if ball.colliderect(player):

        if abs(ball.bottom - player.top) < 10:  # Check if ball hits the top of the paddle

            # TODO Task 2: Fix score to increase by 1
            score += 1  # Increase player score

            if dificult == "easy":
                if score > easy_high_score:
                    easy_high_score = score
            elif dificult == "medium":
                if score > medium_high_score:
                    medium_high_score = score
            elif dificult == "hard":
                if score > hard_high_score:
                    hard_high_score = score
            else:
                if score > endless_high_score:
                    endless_high_score = score

            ball_speed_y *= -1  # Reverse ball's vertical direction

            # TODO Task 6: Add sound effects HERE
            pygame.mixer.init()
            sound_effect = pygame.mixer.Sound("music/tenisound.mp3.mp3")
            sound_effect.play()

            collision += 1

# when the ball collides, the speed increases
    if dificult == "medium" or dificult == "hard":
        if collision > 9:
            collision = 0
            if abs(ball_speed_x) < max_speed and abs(ball_speed_y) < max_speed: #checks the absolute speed (positive) to see if we are pass the speed limit
                ball_speed_x *= 1.2
                ball_speed_y *= 1.2
                speed_up = pygame.mixer.Sound("music/speed_up.wav")
                speed_up.play()
                flash_timer = 30 # for the displaying of the text
                if dificult == "hard" and player.width > 50:
                    shrink_amount = 20
                    player.width -= shrink_amount # changing the width
                    player.x += shrink_amount // 2 # shrink on both sides
            else:
                collision = 0  # reset collision even if max speed reached

    if dificult == "endless":
        if collision > 9:
            collision = 0
            ball_speed_x *= 1.2
            ball_speed_y *= 1.2
            speed_up = pygame.mixer.Sound("music/speed_up.wav")
            speed_up.play()
            flash_timer = 30  # for the displaying of the text
            shrink_amount = 20
            player.width -= shrink_amount  # changing the width
            player.x += shrink_amount // 2  # shrink on both sides


        #MORE WIDTH
        if ball.colliderect(player) and (score <= 20):  #intial phase
            posible_power_up = random.randint(1, 500)
            if posible_power_up == 1 and not morewidth_powerup_active:
                while True:
                    rand_x = random.randint(40, screen_width - 40)
                    rand_y = player.centery  # same vertical position as paddle
                    new_rect = morewidth_powerup_img.get_rect(center=(rand_x, rand_y))
                    if (
                            not new_rect.colliderect(player) and
                            (not less_speed_powerup_active or not new_rect.colliderect(less_speed_powerup_rect))
                    ):  # make sure it’s not inside paddle and not inside of the other powerup
                        morewidth_powerup_rect = new_rect
                        morewidth_powerup_active = True
                        break
        elif ball.colliderect(player) and (20<score<40):  #Second Phase (more common but not everytime)
            posible_power_up = random.randint(1, 50)
            if posible_power_up == 1 and not morewidth_powerup_active:
                while True:
                    rand_x = random.randint(40, screen_width - 40)
                    rand_y = player.centery  # same vertical position as paddle
                    new_rect = morewidth_powerup_img.get_rect(center=(rand_x, rand_y))
                    if (
                            not new_rect.colliderect(player) and
                            (not less_speed_powerup_active or not new_rect.colliderect(less_speed_powerup_rect))
                    ): # make sure it’s not inside paddle and not inside of the other powerup
                        morewidth_powerup_rect = new_rect
                        morewidth_powerup_active = True
                        break
        elif ball.colliderect(player) and (40 < score <= 60): #third Phase (almost every other time)
            posible_power_up = random.randint(1, 20)
            if posible_power_up == 1 and not morewidth_powerup_active:
                while True:
                    rand_x = random.randint(40, screen_width - 40)
                    rand_y = player.centery  # same vertical position as paddle
                    new_rect = morewidth_powerup_img.get_rect(center=(rand_x, rand_y))
                    if (
                            not new_rect.colliderect(player) and
                            (not less_speed_powerup_active or not new_rect.colliderect(less_speed_powerup_rect))
                    ):  # make sure it’s not inside paddle
                        morewidth_powerup_rect = new_rect
                        morewidth_powerup_active = True
                        break
        elif ball.colliderect(player) and (score > 60): #FINAL PHASE (everytime so u dont die :) )
            posible_power_up = random.randint(1, 5)
            if posible_power_up == 1 and not morewidth_powerup_active:
                while True:
                    rand_x = random.randint(40, screen_width - 40)
                    rand_y = player.centery  # same vertical position as paddle
                    new_rect = morewidth_powerup_img.get_rect(center=(rand_x, rand_y))
                    if (
                            not new_rect.colliderect(player) and
                            (not less_speed_powerup_active or not new_rect.colliderect(less_speed_powerup_rect))
                    ):# make sure it’s not inside paddle and not inside of the other powerup
                        morewidth_powerup_rect = new_rect
                        less_speed_powerup_active = True
                        break


        # LESS SPEED POWERUP
        if ball.colliderect(player) and (score < 30): #intial phase (the ball is getting to fast to handle at this rate)
            posible_power_up2 = random.randint(1, 500)
            if posible_power_up2 == 1 and not less_speed_powerup_active:
                while True:
                    rand_x = random.randint(40, screen_width - 40)
                    y=player.centery
                    new_rect = less_speed_powerup_img.get_rect(center=(rand_x, y))
                    if (
                            not new_rect.colliderect(player) and
                            (not morewidth_powerup_active or not new_rect.colliderect(morewidth_powerup_rect))
                    ):# make sure it’s not inside paddle and not inside of the other powerup
                        less_speed_powerup_rect = new_rect
                        less_speed_powerup_active = True
                        break
        elif ball.colliderect(player) and (30<=score<=80): #third phase (more bc the ball is getting fast)
            posible_power_up2 = random.randint(1, 10)
            if posible_power_up2 == 1 and not less_speed_powerup_active:
                while True:
                    rand_x = random.randint(40, screen_width - 40)
                    y=player.centery
                    new_rect = less_speed_powerup_img.get_rect(center=(rand_x, y))
                    if (
                            not new_rect.colliderect(player) and
                            (not morewidth_powerup_active or not new_rect.colliderect(morewidth_powerup_rect))
                    ):# make sure it’s not inside paddle and not inside of the other powerup
                        less_speed_powerup_rect = new_rect
                        less_speed_powerup_active = True
                        break

        elif ball.colliderect(player) and (score>80): #FINAL PHASE (everytime so u dont die :) )
            posible_power_up2 = random.randint(1, 5)
            if posible_power_up2 == 1 and not less_speed_powerup_active:
                while True:
                    rand_x = random.randint(40, screen_width - 40)
                    y=player.centery
                    new_rect = less_speed_powerup_img.get_rect(center=(rand_x, y))
                    if (
                            not new_rect.colliderect(player) and
                            (not morewidth_powerup_active or not new_rect.colliderect(morewidth_powerup_rect))
                    ):# make sure it’s not inside paddle and not inside of the other powerup
                        less_speed_powerup_rect = new_rect
                        less_speed_powerup_active = True
                        break


    # Ball collision with top boundary
    if ball.top <= 0:
        ball_speed_y *= -1  # Reverse ball's vertical direction

    # Ball collision with left and right boundaries
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    # Ball goes below the bottom boundary (missed by player)
    if ball.bottom > screen_height:
        collision = 0
        restart()  # Reset the game
        game_state = "gameover"

def player_movement():
    """
    Handles the movement of the player paddle, keeping it within the screen boundaries.
    """
    player.x += player_speed  # Move the player paddle horizontally

    # Prevent the paddle from moving out of the screen boundaries
    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

def restart():
    """
    Resets the ball and player scores to the initial state.
    """
    global ball_speed_x, ball_speed_y, score,moving, game_state, last_score, player_width, morewidth_powerup_active
    ball.center = (screen_width // 2, screen_height // 2)  # Reset ball position to center
    ball_speed_y, ball_speed_x = 0, 0  # Stop ball movement
    last_score = score
    score = 0  # Reset player score
    player.width = 200
    morewidth_powerup_active = False

def draw_text(text, font, text_col, y):
    img = font.render(text, True, text_col)
    text_rect = img.get_rect()
    text_rect.centerx = screen.get_width() // 2  # Center horizontally
    text_rect.y = y  # Keep vertical position
    screen.blit(img, text_rect)


# General setup
pygame.mixer.pre_init(44100, -16, 1, 1024)
pygame.init()
clock = pygame.time.Clock()
pygame.mixer.music.load("music/main_game_bg_music.mp3")


# Main Window setup
screen_width = 500  # Screen width (can be adjusted)
screen_height = 500  # Screen height (can be adjusted)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')  # Set window title
img=pygame.image.load("skill-issue.png").convert_alpha() # Load the gameover pic and converts alpha to change the size
resized_image = pygame.transform.scale(img, (150, 150))
morewidth_powerup_img = pygame.image.load("morewidth.png").convert_alpha()
morewidth_powerup_img = pygame.transform.scale(morewidth_powerup_img, (40, 40))
morewidth_powerup_active = False
morewidth_powerup_rect = None

less_speed_powerup_img = pygame.image.load("less_speed.png").convert_alpha()
less_speed_powerup_img = pygame.transform.scale(less_speed_powerup_img, (40, 40))
less_speed_powerup_active = False
less_speed_powerup_rect = None
sound_played = 0
gameover_played = False


# Colors
bg_color = pygame.Color('grey12')
TEXT_COL = (255, 255, 255)
flash_timer = 0

# Game Rectangles (ball and player paddle)
ball = pygame.Rect(screen_width // 2 - 15, screen_height // 2 - 15, 30, 30)  # Ball (centered)

player_height = 15
player = pygame.Rect(screen_width//2 - 45, screen_height - 20, player_width, player_height)  # Player paddle

# Game Variables
ball_speed_x = 0
ball_speed_y = 0
player_speed = 0

# Score Text setup
score = 0
easy_high_score = 0
medium_high_score = 0
hard_high_score = 0
endless_high_score = 0
high_score_active=0
last_score = score
basic_font = pygame.font.Font('PressStart2P-Regular.ttf', 24)# Bigger Font
score_font = pygame.font.Font('PressStart2P-Regular.ttf', 18)# Medium Font
smaler_font=pygame.font.Font('PressStart2P-Regular.ttf', 12)# Small Font

menu_played=False # allow menu sound again
game_state="menu" # Indicates if it suposse to be in menu, play or gameover
menu_state="main"
play_state="easy"
start = False  # Indicates if the game has started

# Main game loop
while True:
    # Event handling
    # TODO Task 4: Add your name
    name = "Daniel F. Muñoz & Issac E. Beaudry"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit the game
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed -= 6  # Move paddle left
            if event.key == pygame.K_RIGHT:
                player_speed += 6  # Move paddle right
            if event.key == pygame.K_SPACE:
                if (game_state == "menu" and menu_state == "main")  or game_state == "gameover":
                    moving=1
                    game_state = "play"
                    pygame.mixer.music.load("music/main_game_bg_music.mp3")
                    pygame.mixer.music.play(-1)
                    gameover_played = False  # allow gameover sound again
                    menu_played = False # allow menu sound again
                    start = True  # Start the ball movement
                elif game_state == "play":
                    restart() # Restart
                    game_state = "gameover"
            if event.key == pygame.K_ESCAPE:
                game_state="menu"
                menu_state = "main"
                restart()
            if event.key == pygame.K_1:
                if game_state=="menu":
                    change_sound = pygame.mixer.Sound("music/change_dificulty.wav")
                    change_sound.play()
                    play_state="easy"
            if event.key == pygame.K_2:
                if game_state=="menu":
                    change_sound = pygame.mixer.Sound("music/change_dificulty.wav")
                    change_sound.play()
                    play_state="medium"
            if event.key == pygame.K_3:
                if game_state=="menu":
                    change_sound = pygame.mixer.Sound("music/change_dificulty.wav")
                    change_sound.play()
                    play_state="hard"
            if event.key == pygame.K_4:
                if game_state=="menu":
                    change_sound = pygame.mixer.Sound("music/change_dificulty.wav")
                    change_sound.play()
                    play_state="endless"
            if event.key == pygame.K_5:
                menu_state="codes"
                print("1")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_speed += 6  # Stop moving left
            if event.key == pygame.K_RIGHT:
                player_speed -= 6  # Stop moving right


    if game_state=="menu":
        if not menu_played:
            pygame.mixer.init()
            pygame.mixer.music.load("music/menu_bg_music.mp3")
            pygame.mixer.music.play(-1)
            menu_played = True
        if menu_state=="main":
            start = False
            screen.fill(bg_color)
            draw_text("PONG", basic_font, TEXT_COL, 80)
            draw_text("Press SPACE to start", basic_font, TEXT_COL, 150)
            draw_text(f"Difficulty: {play_state}" , score_font, TEXT_COL, 180)
            if play_state == "easy":
                draw_text(f"High Score: {easy_high_score}", score_font, TEXT_COL, 200)
            elif play_state == "medium":
                draw_text(f"High Score: {medium_high_score}", score_font, TEXT_COL, 200)
            elif play_state == "hard":
                draw_text(f"High Score: {hard_high_score}", score_font, TEXT_COL, 200)
            else:
                draw_text(f"High Score: {endless_high_score}", score_font, TEXT_COL, 200)
            draw_text("Press 1 to  play Easy", score_font, TEXT_COL, 240)
            draw_text("Press 2 to play Medium", score_font, TEXT_COL, 270)
            draw_text("Press 3 to play Hard", score_font, TEXT_COL, 300)
            draw_text("Press 4 to play Endless", score_font, TEXT_COL, 330)
            draw_text("Music from Five Nights at Freddy 6", smaler_font, TEXT_COL, 400)
            pygame.display.flip()
        elif menu_state=="codes":
            screen.fill(bg_color)
            draw_text("CODES", basic_font, TEXT_COL, 100)
            pygame.display.flip()

        continue
    elif game_state=="gameover":
        screen.fill(bg_color)
        draw_text("GAMEOVER", basic_font, TEXT_COL, 100)
        draw_text(f" Your score: {last_score}", basic_font, TEXT_COL, 150)
        draw_text("Press SPACE to Restart", score_font, TEXT_COL, 200)
        draw_text("Press ESC to go back to the menu", smaler_font, TEXT_COL, 220)
        screen.blit(resized_image, (170, 300))
        if high_score_active == 1:
            pygame.mixer.init()
            high_score_achived = pygame.mixer.Sound("music/high_score.wav")
            high_score_achived.play()
            high_score_active = 0
        if not gameover_played:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("music/gameover_bg_music.mp3")
            pygame.mixer.music.play(-1)
            gameover_played = True
        pygame.display.flip()
        continue

    else:
        # Visuals
        # TODO Task 3: Change color of the ball
        orange = pygame.Color('orange')
        light_grey = pygame.Color('grey83')
        red = pygame.Color('red')
        screen.fill(bg_color)  # Clear screen with background color
        pygame.draw.rect(screen, light_grey, player)  # Draw player paddle
        pygame.draw.ellipse(screen, orange, ball)  # Draw ball

        pygame.draw.ellipse(screen, orange, ball)  # Draw ball
        if play_state == "easy":
            player_text = score_font.render(f'Score:{score} | High Score:{endless_high_score}', False, light_grey)
        elif play_state == "medium":
            player_text = score_font.render(f'Score:{score} | High Score:{medium_high_score}', False, light_grey)
        elif play_state == "hard":
            player_text = score_font.render(f'Score:{score} | High Score:{hard_high_score}', False, light_grey)
        elif play_state == "endless":
            player_text = score_font.render(f'Score:{score} | High Score:{endless_high_score}', False, light_grey)
        # Render player score and high score
        text_rect = player_text.get_rect()
        text_rect.centerx = screen.get_width() // 2
        text_rect.y = 10
        screen.blit(player_text, text_rect)  # Display score on screen

        if play_state == "medium":

            # Game Logic
            ball_movement("medium")
            player_movement()

            if score == 0:  #When starting the game, info to restart and go back to the menu
                draw_text("Press SPACE to Restart (GameOver)",smaler_font, TEXT_COL, 40)
                draw_text("Press ESC to go back to menu", smaler_font, TEXT_COL, 60)
                draw_text("MEDIUM", score_font, TEXT_COL, 200)

            if flash_timer > 0: # Display for that the speed changed
                draw_text("SPEED UP!", basic_font, TEXT_COL, 200)
                flash_timer -= 1  # count down each frame

            if not(score < medium_high_score) and medium_high_score != 0: #flag to check if high score has been beaten (for sound effect)
                high_score_active=1

            # Update display
            pygame.display.flip()
            clock.tick(60)  # Maintain 60 frames per second

        elif play_state == "easy":
            ball_movement("easy")
            player_movement()

            if score == 0:  # When starting the game, info to restart and go back to the menu
                draw_text("Press SPACE to Restart (GameOver)", smaler_font, TEXT_COL, 40)
                draw_text("Press ESC to go back to menu", smaler_font, TEXT_COL, 60)
                draw_text("EASY", score_font, TEXT_COL, 200)

            if not(score < easy_high_score) and easy_high_score != 0: #flag to check if high score has been beaten (for sound effect)
                high_score_active=1

            # Update display
            pygame.display.flip()
            clock.tick(60)  # Maintain 60 frames per second

        elif play_state == "hard":
            # Game Logic
            ball_movement("hard")
            player_movement()

            if score == 0:  # When starting the game, info to restart and go back to the menu
                draw_text("Press SPACE to Restart (GameOver)", smaler_font, TEXT_COL, 40)
                draw_text("Press ESC to go back to menu", smaler_font, TEXT_COL, 60)
                draw_text("HARD", score_font, TEXT_COL, 200)

            if flash_timer > 0:  # Display for that the speed changed
                draw_text("SPEED UP!", basic_font, TEXT_COL, 200)
                flash_timer -= 1  # count down each frame

            if not (score < hard_high_score) and hard_high_score != 0:  # flag to check if high score has been beaten (for sound effect)
                high_score_active = 1

            # Update display
            pygame.display.flip()
            clock.tick(60)  # Maintain 60 frames per second

        elif play_state == "endless":
            # Game Logic
            ball_movement("endless")
            player_movement()

            if morewidth_powerup_active:
                screen.blit(morewidth_powerup_img, morewidth_powerup_rect)
                if sound_played == 0:
                    morewidth_sound = pygame.mixer.Sound("music/morewidth_powerup.wav")
                    morewidth_sound.play()
                    sound_played = 1

                if player.colliderect(morewidth_powerup_rect):
                    player.width += shrink_amount
                    player.x -= shrink_amount // 2
                    morewidth_powerup_active = False
                    morewidth_powerup_rect = None
                    sound_played = 0

            if less_speed_powerup_active:
                screen.blit(less_speed_powerup_img, less_speed_powerup_rect)
                if sound_played == 0:
                    morewidth_sound = pygame.mixer.Sound("music/morewidth_powerup.wav")
                    morewidth_sound.play()
                    sound_played = 1

                if player.colliderect(less_speed_powerup_rect):
                    ball_speed_x/=1.5
                    ball_speed_y /= 1.5
                    less_speed_powerup_active = False
                    less_speed_powerup_rect = None
                    sound_played = 0



            if score == 0:  # When starting the game, info to restart and go back to the menu
                draw_text("Press SPACE to Restart (GameOver)", smaler_font, TEXT_COL, 40)
                draw_text("Press ESC to go back to menu", smaler_font, TEXT_COL, 60)
                draw_text("ENDLESS", score_font, TEXT_COL, 200)

            if flash_timer > 0:  # Display for that the speed changed
                if play_state=="medium":
                    draw_text("SPEED UP!", basic_font, TEXT_COL, 200)
                    flash_timer -= 1  # count down each frame
                elif play_state in ["hard", "endless"]:
                    draw_text("SPEED UP!", basic_font, TEXT_COL, 200)
                    draw_text("LESS PADDLE!", basic_font, TEXT_COL, 300)
                    flash_timer -= 1  # count down each frame`

            if not (score < endless_high_score) and endless_high_score != 0 :  # flag to check if high score has been beaten (for sound effect)
                high_score_active = 1

            # Update display
            pygame.display.flip()
            clock.tick(60)  # Maintain 60 frames per second

        else:
            pygame.mixer.music.stop()