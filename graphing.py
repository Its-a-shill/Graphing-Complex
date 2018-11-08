from PIL import Image
import math
import os

# Width and height in pixels
# Step is number of pixels
WIDTH = 1920
HEIGHT = 1080
ZOOM = 15

# Rectangle of domain
minReDom = -math.pi/ZOOM*0
maxReDom = math.pi/ZOOM
minImDom = -math.pi*1080/1920/ZOOM/2
maxImDom = math.pi*1080/1920/ZOOM/2

# Max important modulus in range
highest = 90

def mod(inZ):
    r = math.sqrt(inZ[0]*inZ[0]+inZ[1]*inZ[1])
    return r

def arg(inZ):
    out = math.atan2(inZ[1],inZ[0])
    if out < 0:
        out += 2*math.pi
    return out

def recip(inZ):
    x = inZ[0]/(mod(inZ)*mod(inZ))
    y = inZ[1]/(mod(inZ)*mod(inZ))
    return x,y

def mult(inZ,inW):
    x = inZ[0]*inW[0] - inZ[1]*inW[1]
    y = inZ[1]*inW[0] + inZ[0]*inW[1]
    return x,y

def add(inZ,inW):
    return inZ[0]+inW[0],inZ[1]+inW[1]

def exp(inZ):
    x = math.cos(inZ[1])*(math.exp(inZ[0]))
    y = math.sin(inZ[1])*(math.exp(inZ[0]))
    return x,y

def sin(inZ):
    return mult((1/2,0),add(exp(mult(inZ,(0,1))),mult((-1,0),exp(mult(inZ,(0,-1))))))

def cos(inZ):
    return mult((1 / 2, 0), add(exp(mult(inZ, (0, 1))), exp(mult(inZ, (0, 1)))))

def outputMod(inZ):
    try:
        out = 256*math.log(1+mod(inZ),highest)
        if out > 1000000:
            out = 1000000
        return int(out)
    except:
        return 0

def func(inZ):
    return recip(sin(exp(recip(inZ))))


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
        try:
            w = func((x,y))
        except:
            continue

        # If out of bounds of graph, do nothing
        if xPos < 0 or xPos >= WIDTH or yPos < 0 or yPos >= HEIGHT:
            continue

        # Calculate color and graph that color
        theta = arg(w)
        if math.isnan(theta):
            theta = 0

        theta2 = theta - math.pi
        if theta2 < 0:
            theta2 += 2*math.pi

        imagePxls[yPos * WIDTH + xPos] = (int(128 / math.pi * theta),
                                          int(1 / 4 * outputMod(w)),
                                          int(128 / math.pi * theta2))

    # Prints progress as a percent, can be commented out safely
    print(int((x - minReDom) / (maxReDom - minReDom) * 10000) / 100, '%', sep='')


# Saves and closes the new image
image.putdata(imagePxls)
os.remove("graphed.png")
image.save("graphed.png")
image.close()
