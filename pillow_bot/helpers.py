'''
The funcion draws a chosen character on vahta bg in the chosen cell
'''


from PIL import Image

async def pillow_draw(char, h, w):
    w = int(w)
    h = int(h)
    # Open the character image
    img = Image.open(f"pillow_bot/{char}.png")
    img_w, img_h = img.size

    # Opening the bg
    background = Image.open("pillow_bot/vahta.jpg")
    bg_w, bg_h = background.size

    # Setting the position
    offset = (bg_w // 7 * w - img_w // 3 * 2, bg_h // 10 * (1 + h))

    # Drawing and saving
    background.paste(img, offset, img)
    background.save("pillow_bot/vahta.jpg")


