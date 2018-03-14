from PIL import Image
import math

# Width and height in pixels
# Step is number of pixels
WIDTH = 544
HEIGHT = 544
xStep = 0.002
yStep = 0.002

# Rectangle of domain
minReDom = -1
maxReDom = 1
minImDom = 0
maxImDom = 2*math.pi

# Rectangle of range
minReRan = -math.e
maxReRan = math.e
minImRan = -math.e
maxImRan = math.e


# Defines u and v (u is func1, v is func2)
def func1(inX, inY):
    return math.exp(inX)*math.cos(inY)


def func2(inX, inY):
    return math.exp(inX)*math.sin(inY)


def sequence(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step


# Generates a blank image
image = Image.new('RGB', (WIDTH, HEIGHT))
imagePxls = list(image.getdata())

for x in sequence(minReDom, maxReDom, xStep):
    for y in sequence(minImDom, maxImDom, yStep):
        # Calculates u and v
        u = func1(x, y)
        v = func2(x, y)

        # Gets pixel location to plot
        uPos = int(WIDTH * (u - minReRan) / (maxReRan - minReRan))
        vPos = int(HEIGHT * (maxImRan - v) / (maxImRan - minImRan))

        # If out of bounds of graph, do nothing
        if uPos < 0 or uPos >= WIDTH or vPos < 0 or vPos >= HEIGHT:
            continue

        # Calculate color and graph that color
        theta = math.atan2(y, x)
        if theta < 0:
            theta += 2 * math.pi
        imagePxls[vPos * WIDTH + uPos] = (int(128 / math.pi * theta),
                                          0,
                                          int(362 * math.sqrt(math.pow(x / max(abs(maxReDom), abs(minReDom)), 2) +
                                                              math.pow(y / max(abs(maxImDom), abs(minImDom)), 2))))

    # Prints progress as a percent, can be commented out safely
    print(int((x-minReDom) / (maxReDom-minReDom) * 10000)/100, '%', sep='')

# Saves and closes the new image
image.putdata(imagePxls)
image.save("graphed.png")
image.close()
