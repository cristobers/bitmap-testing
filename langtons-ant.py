# Example code implementing langtons ant using the bitmap library.
from bitmaps import BMP

def langton(n):
    file = BMP("Untitled.bmp")
    width, height = file.size()
    white, black = [255, 255, 255], [0, 0, 0]

    x = width // 2
    y = height // 2

    position = 3 
    counter = 0

    # 0 up 1 right 2 down 3 left   
    for i in range(0, n):
        if file.read_pixel( (x, y) ) == white:
            file.draw_pixel((x, y), black)
            counter = position + 1
            position = counter % 4

        elif file.read_pixel( (x, y) ) == black:
            file.draw_pixel( (x, y), white)
            counter = position - 1
            position = counter % 4

        match position:
            case 0:
                y += 1
            case 1:
                x += 1
            case 2:
                y -= 1
            case 3:
                x -= 1

langton(11000)
