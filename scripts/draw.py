import pygame, PIL
from PIL import Image
# Initialize Pygame
def draw(image_path, undo_number, save_path):
    pygame.init()

    # Set up display dimensions
    WINDOW_WIDTH, WINDOW_HEIGHT = 850, 600
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Annotate")
    pygame.display.set_icon(pygame.image.load('icon.png'))
    img = Image.open(image_path)
    # Load the background image
    # global img, pg_factor, undo_number
    pillow_image_mode = img.mode
    pillow_image_size = img.size
    # pillow_image_rgba = img.convert("RGB")
    image_data = img.tobytes()
    # bg_image_path = "output.jpg"  # Path to your background image
    bg_image = pygame.image.fromstring(image_data, pillow_image_size, img.mode)

    # Calculate the scale factor to fit the image inside the window
    image_width, image_height = bg_image.get_width(), bg_image.get_height()
    scale_factor = min(850 / image_width, 550 / image_height)
    scaled_width, scaled_height = int(image_width * scale_factor), int(image_height * scale_factor)

    # Create a scaled version of the background image
    scaled_bg_image = pygame.transform.rotozoom(bg_image, 0, scale_factor)

    # Initialize drawing variables
    drawing = False
    brush_size = [12 , 25, 45, 70, 100]
    t=0

    brush_color = 'white'  # Initial brush color (black)
    color = ['white', 'red', 'cyan', 'green', 'black', 'magenta', 'orange', 'purple', 'yellow']
    c=0
    fps = 60
    clock = pygame.time.Clock()

    # pg_factor = 1

    # Main loop
    running = True
    while running:
        pygame.display.set_caption(f"Brush Color is: {brush_color} and Brush Size is: {brush_size[t]}")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button to start drawing
                    drawing = True
                elif event.button == 3:
                    if t<= 3:
                        t+=1
                    elif t>=4:
                        t=0
                    print(brush_size[t])
                    
                # pygame.display.set_caption(f"Brush Color is: {brush_color[c]} and Brush Size is: {brush_size[t]}")
                # print(brush_color[c])

            elif event.type == pygame.MOUSEWHEEL:
                if c >= 8:
                    c=0
                    brush_color=color[0] # Change color to red (RGB: 255, 0, 0)
                elif c <= 7:
                    c+=1
                    brush_color=color[c]
                

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button released to stop drawing
                    drawing = False
                    undo_number += 1
                    pygame.image.save(bg_image, save_path)
                    
                    print("Image saved successfully.")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    undo_number += 1
                    pygame.image.save(bg_image, save_path)
                    
                    print("Image saved successfully.")
                    running = False
                    
        # Draw the scaled background image centered within the window
        screen.fill((255, 255, 255))  # Fill screen with white background
        screen.blit(scaled_bg_image, ((WINDOW_WIDTH - scaled_width) // 2, (WINDOW_HEIGHT - scaled_height) // 2))

        # Draw on the screen (directly on the window)
        if drawing:
            mouse_pos = pygame.mouse.get_pos()
            mouse_x, mouse_y = mouse_pos

            pygame.draw.circle(bg_image, brush_color, (int((mouse_x) - (WINDOW_WIDTH - scaled_width)/2)/scale_factor, int((mouse_y) - (WINDOW_HEIGHT - scaled_height)/2)/scale_factor), brush_size[t])
            print(mouse_x, mouse_y), mouse_pos
            pygame.draw.circle(scaled_bg_image, brush_color, (mouse_x - (WINDOW_WIDTH - scaled_width) // 2, mouse_y - (WINDOW_HEIGHT - scaled_height) // 2), (brush_size[t])*scale_factor)

        pygame.display.update()
        clock.tick(fps)

    # Quit Pygame
    pygame.quit()