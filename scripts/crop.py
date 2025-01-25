import pygame, PIL
from PIL import Image
def crop_image(image_path, undo_number, save_path):
    pygame.init()

    # Constants
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 120
    img = Image.open(image_path)
    pillow_image_mode = img.mode
    pillow_image_size = img.size
    image_data = img.tobytes()
    # Path to your background image
    bg_image = pygame.image.fromstring(image_data, pillow_image_size, pillow_image_mode)

    # Calculate the scale factor to fit the image inside the SCREEN
    image_width, image_height = bg_image.get_width(), bg_image.get_height()
    scale_factor = min(SCREEN_WIDTH / image_width, SCREEN_HEIGHT / image_height)
    scaled_width, scaled_height = int(image_width * scale_factor), int(image_height * scale_factor)
    RECT_WIDTH = scaled_width - 200*scale_factor
    RECT_HEIGHT = scaled_height - 200*scale_factor
    # Create a scaled version of the background image
    scaled_bg_image = pygame.transform.smoothscale(bg_image, (scaled_width, scaled_height))

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Initialize the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Image Cropper")
    pygame.display.set_icon(pygame.image.load('assets/mamba_1.png'))
    clock = pygame.time.Clock()

    # Rectangle position
    rect_x = SCREEN_WIDTH // 2 - RECT_WIDTH // 2
    rect_y = SCREEN_HEIGHT // 2 - RECT_HEIGHT // 2

    moving = False
    decrease_height = False
    increase_height = False
    decrease_width = False
    increase_width = False
    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                moving = True
            elif event.type == pygame.MOUSEBUTTONUP:
                moving = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print('cropped')
                    l = int((rect_x - ((SCREEN_WIDTH - scaled_width) / 2))/scale_factor)
                    r = int(((rect_x - ((SCREEN_WIDTH - scaled_width) / 2)) + RECT_WIDTH) / scale_factor)
                    t = int((rect_y - ((SCREEN_HEIGHT - scaled_height) / 2))/scale_factor)
                    b = int(((rect_y - ((SCREEN_HEIGHT - scaled_height) / 2)) + RECT_HEIGHT) / scale_factor)
                    cropped_img = img.crop((l, t, r, b))
                    undo_number += 1
                    cropped_img.save(save_path)
                    
                    img  = Image.open(save_path)
                    running = False
                
                if event.key == pygame.K_UP:
                    decrease_height = True
                elif event.key == pygame.K_DOWN:
                    increase_height = True
                elif event.key == pygame.K_LEFT:
                    decrease_width = True
                elif event.key == pygame.K_RIGHT:
                    increase_width = True
            elif event.type == pygame.KEYUP:
                decrease_height = False
                increase_height = False
                decrease_width = False
                increase_width = False

        if decrease_height:
            RECT_HEIGHT-=1.5
        elif increase_height:
            RECT_HEIGHT+=1.5
        elif decrease_width:
            RECT_WIDTH-=1.5
        elif increase_width:
            RECT_WIDTH+=1.5

        if moving:
            # Get the current mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Limit rectangle within the screen boundaries
            rect_x = max((SCREEN_WIDTH - scaled_width) // 2, min(mouse_x, ((SCREEN_WIDTH - scaled_width) // 2) + scaled_width - RECT_WIDTH))
            rect_y = max((SCREEN_HEIGHT - scaled_height) // 2, min(mouse_y, ((SCREEN_HEIGHT - scaled_height) // 2) + scaled_height - RECT_HEIGHT))

        # Draw the rectangle and image
        
        screen.fill((255, 255, 255))
        screen.blit(scaled_bg_image, ((SCREEN_WIDTH - scaled_width) // 2, (SCREEN_HEIGHT - scaled_height) // 2))
        pygame.draw.rect(screen, (0,0,0), (rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT), 4)
        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    pygame.quit()
    