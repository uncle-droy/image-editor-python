import pygame, os
from PIL import Image
# undo_number = 1
# save_path = "output.png"
# Initialize Pygame

def text_add(image_path, undo_number, save_path):
    pygame.init()
    pygame.font.init()
    fps = 120
    clock = pygame.time.Clock()
    # Set up display dimensions
    WINDOW_WIDTH, WINDOW_HEIGHT = 850, 600
    screen = pygame.display.set_mode((WINDOW_WIDTH, 700))
    increase = False
    decrease = False
    pygame.display.set_caption("Add Text")
    pygame.display.set_icon(pygame.image.load(os.path.join('assets', 'mamba.png')))
    pil_img = Image.open(image_path)
    # Load the background image
    pillow_image_mode = pil_img.mode
    pillow_image_size = pil_img.size
    print(pillow_image_mode)
    # pillow_image_rgba = pil_img.convert("RGB")
    image_data = pil_img.tobytes()
    # bg_image_path = "output.jpg"  # Path to your background image
    bg_image = pygame.image.fromstring(image_data, pillow_image_size, pillow_image_mode)

    # Calculate the scale factor to fit the image inside the window
    image_width, image_height = bg_image.get_width(), bg_image.get_height()
    scale_factor = min(850 / image_width, 550 / image_height)
    scaled_width, scaled_height = int(image_width * scale_factor), int(image_height * scale_factor)

    # Create a scaled version of the background image
    scaled_bg_image = pygame.transform.rotozoom(bg_image, 0, scale_factor)
    
    img_x, img_y = ((WINDOW_WIDTH - scaled_width) // 2, (WINDOW_HEIGHT - scaled_height) // 2)
    text_x, text_y = img_x, img_y
    string = "Type something:"
    print(string)
    fonts = ['assets/calligraffitti.ttf', 'assets/roboto.ttf', 'assets/poppins.ttf', 'assets/indie_flower.ttf', 'assets/open_sans.ttf']
    font_num = 0
    size = 30
    font = pygame.font.Font(fonts[font_num], size)
    
    alphabets = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", " ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "!", "\\", "$", "#","%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<", "=", ">", "?", "@", "[", "]", "^", "_", "`", "{", "|", "}"]
    addText = True
    # dest = r'~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
    # src = r"`1234567890-=qwertyuiop[]\asdfghjkl;\'zxcvbnm,./"

    colors = ['white', 'blue','red', 'green', 'aqua','black', 'burlywood1','hotpink', 'orange', 'purple', 'yellow']
    col_index = 0
    index = 0
    text_list = [string]
    text = font.render(text_list[index], True, colors[col_index])
    
    while addText:
        
        screen.fill((255, 255, 255)) 
        screen.blit(scaled_bg_image, (img_x, img_y)) # Fill screen with white background
        for i in range(0, len(text_list)):
            text = font.render(text_list[i], True, colors[col_index])
            screen.blit(text, (text_x, text_y+(i*size)))
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                print("Text adding cancelled")
                addText = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    font_num+=1
                    if font_num == 5:
                        font_num = 0
                    print(f'font size change to {fonts[font_num]}')
                if event.button == 1:
                    col_index+=1
                    if col_index == 11:
                        col_index = 0
                    print(f'current color is: {colors[col_index]}')

                    
            elif event.type == pygame.MOUSEWHEEL:
                if event.y == -1:
                    size -= 1
                if event.y == +1:
                    size += 1
                print(size)
            
            elif event.type == pygame.KEYDOWN:
                
                mods = pygame.key.get_mods()                
                key = pygame.key.name(event.key)
                font = pygame.font.Font(fonts[font_num], int(size))

                if event.key == pygame.K_UP:
                    text_y-=5
                if event.key == pygame.K_DOWN:
                    text_y+=5
                if event.key == pygame.K_LEFT:
                    text_x-=5
                if event.key == pygame.K_RIGHT:
                    text_x+=5
                if event.key == pygame.K_RETURN:
                    print('New Line')
                    index+=1
                    text_list.append("")
                
                if event.key == pygame.K_s and mods & pygame.KMOD_CTRL:
                    print('Ctrl Key pressed')
                    undo_number+=1
                    text_x = (text_x - ((WINDOW_WIDTH - scaled_width) // 2))//scale_factor
                    text_y = (text_y - ((WINDOW_HEIGHT - scaled_height) // 2))//scale_factor
                    size = size//scale_factor
                    font = pygame.font.Font(fonts[font_num], int(size))
                    for i in range(0, len(text_list)):
                        text = font.render(text_list[i], True, colors[col_index])
                        print(text_list[i])
                        print(text_x, text_y+(i*size))
                        bg_image.blit(text, (text_x, text_y+(i*size)))
                    bg_image = bg_image
                    pygame.image.save(bg_image, save_path)
                    print("Image saved")
                    addText = False
                    # pygame.quit()

                if mods & pygame.KMOD_SHIFT and not mods & pygame.KMOD_CTRL:  # Check if Shift is pressed
                    if event.key >= pygame.K_a and event.key <= pygame.K_z:
                        capital_letter = chr(event.key).upper()
                        text_list[index] = text_list[index] + capital_letter
                        for i in range(0, len(text_list)):
                            text = font.render(text_list[i], True, colors[col_index])
                            screen.blit(text, (text_x, text_y+(i*size)))
                    elif key in alphabets:
                        text_list[index] = text_list[index] + str(key)
                        for i in range(0, len(text_list)):
                            text = font.render(text_list[i], True, colors[col_index])
                            screen.blit(text, (text_x, text_y+(i*size)))
            
                else:
                    if event.key >= pygame.K_a and event.key <= pygame.K_z and not mods & pygame.KMOD_CTRL:
                        lower_letter = chr(event.key)
                        text_list[index] = text_list[index] + lower_letter
                        for i in range(0, len(text_list)):
                            text = font.render(text_list[i], True, colors[col_index])
                            screen.blit(text, (text_x, text_y+(i*size)))
                    elif key in alphabets:
                        text_list[index] = text_list[index] + str(key)
                        for i in range(0, len(text_list)):
                            text = font.render(text_list[i], True, colors[col_index])
                            screen.blit(text, (text_x, text_y+(i*size)))
                
                if key == "backspace":                    
                    if text_list[index]=="":
                        index-=1
                    text_list[index] = text_list[index][0:-1]
                    screen.blit(scaled_bg_image, (img_x, img_y))
                    for j in range(0, len(text_list)):
                        text = font.render(text_list[j], True, colors[col_index])
                        screen.blit(text, (text_x, text_y+(i*size)))


                elif event.key == pygame.K_SPACE:
                    text_list[index] = text_list[index] + " "
                    for l in range(0, len(text_list)):
                        text = font.render(text_list[l], True, colors[col_index])
                        screen.blit(text, (text_x, text_y+(i*size)))
                else:
                    pass

                
            elif event.type == pygame.KEYUP:
                increase = False
                decrease = False
        
        pygame.display.flip()
        clock.tick(fps)
    
    pygame.quit()
    return undo_number

