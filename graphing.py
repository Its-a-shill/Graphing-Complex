from PIL import Image
import math
import os

# Width and height in pixels
# Step is number of pixels
WIDTH = 500
HEIGHT = 500

# Rectangle of domain
minReDom = -8
maxReDom = 8
minImDom = -8
maxImDom = 8

# Max important modulus in range
highest = 40


# Defines u and v (u is func1, v is func2)
def func1(inX, inY):
    return math.cos(inY)*(math.exp(-inX)-math.exp(inX))/2


def func2(inX, inY):
    return -math.sin(inY)*(math.exp(-inX)+math.exp(inX))/2


def sequence(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step


# Generates a blank image
image = Image.new('RGB', (WIDTH, HEIGHT))
imagePxls = list(image.getdata())

for xPos in range(0, WIDTH):
    for yPos in range(0, HEIGHT):
        # Gets x and y
        x = xPos * (maxReDom - minReDom) / WIDTH + minReDom
        y = maxImDom - yPos * (maxImDom - minImDom) / HEIGHT

        # Calculates u and v
        u = func1(x, y)
        v = func2(x, y)

        # If out of bounds of graph, do nothing
        if xPos < 0 or xPos >= WIDTH or yPos < 0 or yPos >= HEIGHT:
            continue

        # Calculate color and graph that color
        theta = math.atan2(v, u)
        if theta < 0:
           theta += 2 * math.pi
        imagePxls[yPos * WIDTH + xPos] = (int(128 / math.pi * theta),
                                          0,
                                          int(256 * math.sqrt(math.pow(u, 2) +
                                                              math.pow(v, 2)) / highest))

    # Prints progress as a percent, can be commented out safely
    print(int((x - minReDom) / (maxReDom - minReDom) * 10000) / 100, '%', sep='')

# Saves and closes the new image
image.putdata(imagePxls)
os.remove("graphed2.png")
image.save("graphed2.png")
image.close()
