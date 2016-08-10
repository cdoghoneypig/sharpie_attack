from PIL import Image
from PIL import ImageEnhance
import os
import imghdr

b_thresh = 200
brighten_factor = 1.2
contrast_factor = 1.5
valid_pic_formats = ["jpg","gif","png", "jpeg"]
the_folder = "sharpie"

# print("Brightness threshold = ",b_thresh)
user_thresh = input("Brightness threshdold (200?): ")
try: b_thresh = int(user_thresh)
except: 
    print("uh no")
    pass

def attack(fn):
    n = Image.open(the_folder + "/" + fn)

    #increase brightness and contrast
    brighter = ImageEnhance.Brightness(n)
    n = brighter.enhance(brighten_factor)
    contraster = ImageEnhance.Contrast(n)
    n = contraster.enhance(contrast_factor)

    n = n.convert("RGBA")
    m = n.load()
    s = n.size

    print("pixel adjustments...")
    # iterate through x and y (every pixel) 
    for x in range(0,s[0]):
        for y in range(0,s[1]):
            r,g,b,a = m[x,y]
            
            #determine brightness with average of rgb values
            # brightness = (r+g+b)/3

            # luminosity method preferred
            brightness = .21*r + .72*g + .07*b
            if brightness > b_thresh:
                m[x,y] = r,g,b,0
            else:
                # turns colors into black with alpha
                m[x,y] = 0,0,0,int(255-brightness)
    print("done adjusting")

    n.save(the_folder + "/" + "attacked_" + fn.split(".")[0] + ".png", "PNG")
 



for each_file in os.listdir(the_folder):
    if each_file.split(".")[1] in valid_pic_formats and "attacked" not in each_file.split(".")[0]:
        print("Processing", each_file)
        attack(each_file)
