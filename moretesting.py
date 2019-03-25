from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

img = Image.open("test.png")
draw = ImageDraw.Draw(img)
# font = ImageFont.truetype(<font-file>, <font-size>)
#font = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf", 100)
# draw.text((x, y),"Sample Text",(r,g,b))
draw.text((0, 0),"Sample Text",(83,224,63),font=font)
img.show()