#!/usr/bin/python3

from PIL import Image
from random import randint
import numpy as np

def avg (lst):
	s = sum(lst)
	return s // len(lst)

def conv_to_grayscale_array (f, num_colors):

	# print("conv_to_grayscale_array:", f, num_colors)

	im = Image.open(f)

	# print("conv_to_grayscale_array:", im)

	a = np.asarray(im)

	# print("conv_to_grayscale_array:", a)

	(m,n) = a.shape # PREVIOUSLY WAS (m,n,_)

	# print("conv_to_grayscale_array:", m, n)
	
	b = np.empty((m,n),dtype=np.uint8)

	# print("conv_to_grayscale_array:", b)
	
	for y in range(m):
		for x in range(n):

			# print("HERE1")
			# avg = avg(a[y][x])
			# print(a[y][x])
			
			# print("HERE2")
			real_val = (a[y][x] / 256)
			b[y][x] = real_val * num_colors

	# print("conv_to_grayscale_array:", b)
			
	return b

	
def array_to_img (a):
	return Image.fromarray(a)

# encrypts a file t with the given key; 
# returns encrypted array
def encrypt (t,key):
	(m,n) = t.shape
	
	c = np.empty((m,n),dtype=np.uint8)
	
	for y in range(m):
		for x in range(n):
			c[y][x] = key[t[y][x]]


	return c

# open file f, scale the number of colors to num_colors,
# generate a random encryption key, and return the triple
#   (t,c,key)
# where t is the plaintext array, c is the cyphertext array,
# and key is the substitution cypher key
def encrypt_image (f, num_colors):

	# print("encrpyt_image:", f, num_colors)

	t = conv_to_grayscale_array(f, num_colors)

	# print("encrpyt_image:", t)

	# random key: permute all the colors
	key = np.random.permutation(num_colors)

	c = encrypt(t,key)
	
	return (t,c,key)

# finds the inverse of the given key
def inverse (key):
	(num_colors,) = key.shape
	inv = np.empty((num_colors),dtype=np.uint8)
	for n in range(num_colors):
		inv[key[n]] = n
		
	return inv

# reverses the order of a key.  Your code to crack the
# cypher may naturally produce a key which, when decrypting,
# will give the negative of the original image.  If this
# happens, decrypting with the key's reverse will give the
# original image.
def reverse (key):
	(num_colors,) = key.shape
	rev = np.empty((num_colors),dtype=np.uint8)
	for n in range(num_colors):
		rev[n] = key[num_colors-n-1]
		
	return rev
	

def decrypt (c, key):
	inv = inverse(key)
	return encrypt(c,inv)


# linearly scales an array from num_colors to 256 colors
# without this scaling, images with only 32 colors would appear
# very dark, since the maximum brightness of a pixel is just 32 out
# of 256.
def scale_array(a, num_colors):
	(m,n) = a.shape
	
	b = np.empty((m,n),dtype=np.uint8)
	for y in range(m):
		for x in range(n):
			b[y][x] = a[y][x] * (256 / num_colors)
			
	return b

def display (c,key):
	pt = decrypt(c,key)
	pts = scale_array(pt,len(key))
	im = array_to_img(pts)
	im.show()

def randomkey (num_colors):
	return np.random.permutation(num_colors)

def identkey (num_colors):
	return np.arange(num_colors)

	
# opens file f, converts to an image with 'depth' colors,
# encrypts the file and displays the image, then decrypts 
# and displays the image
def encrypt_decrypt_demo (f, depth):

	# print("encrypt_decrypt_demo:", f, depth)

	t,c,key=encrypt_image(f, depth)

	# print("encrypt_decrypt_demo:", t, c, key)
	
	# display encrypted image
	display(c,identkey(depth))
	
	# display decrypted image
	display(c,key)
	
	return c,key


def encrypt_image_file(in_file, out_file, depth):
	plaintext,cyphertext,key=encrypt_image(in_file, depth)
	ident_key=identkey(depth)
	display(cyphertext,ident_key)
	display(cyphertext,key)
	im = array_to_img(cyphertext)
	im.save(out_file)


#Assumes f is a grayscale PNG file.
#You can use this function to load the A.png,
# B.png, C.png, and D.png images
# from the assignment.
#
# it returns an array with the image data
def open_image (f):
	im = Image.open(f)
	a = np.asarray(im)

	return a

# examples:
# c = open_image("A.png")

# Kollin's code starts here

# The following 3 variables can be changed by the user to get different results
keySize = 256 # Size for the key
bound = 2 # Amount of variation allowed for adjacent pixel key values when searching
imageName = "D.png" # The name for the image to use


imageArray = open_image(imageName) # Open the image with the given name

keys = []
for x in range(keySize):
	keys.append(-1)

newKey = (int)(keySize / 2)
# newKey = 0
print("newKey: ", newKey)
count = 0
first = True

for i in range(0, imageArray.shape[0]):
	for j in range(0, imageArray.shape[1]):
		if keys[imageArray[i][j]] == -1:
			counter = 1
			notFirst = True
			if j - 1 >= 0:
				notFirst = False
				keyVal = imageArray[i][j - 1]
				while (keyVal + counter < len(keys) or keyVal - counter >= 0) and counter < bound:
					if keyVal + counter < len(keys):
						# if keys[keyVal + counter] == -1:
						tester = True
						for p in keys:
							if p == keyVal + counter:
								tester = False
								break

						if tester == True:
							# print(keyVal + counter)

							keys[imageArray[i][j]] = keyVal + counter
							break
					elif keyVal - counter >= 0:
						# if keys[keyVal - counter] == -1:
						tester = True
						for p in keys:
							if p == keyVal - counter:
								tester = False
								break

						if tester == True:

							keys[imageArray[i][j]] = keyVal - counter
							break
					counter = counter + 1

			if i - 1 >= 0 and (counter >= bound or notFirst == True):
				keyVal = imageArray[i - 1][j]
				counter = 1
				while keyVal + counter < len(keys) or keyVal - counter >= 0:
					if keyVal + counter < len(keys):
						# if keys[keyVal + counter] == -1:
						tester = True
						for p in keys:
							if p == keyVal + counter:
								tester = False
								break

						if tester == True:

							keys[imageArray[i][j]] = keyVal + counter
							break
					elif keyVal - counter >= 0:
						# if keys[keyVal - counter] == -1:
						tester = True
						for p in keys:
							if p == keyVal - counter:
								tester = False
								break

						if tester == True:

							keys[imageArray[i][j]] = keyVal - counter
							break
					counter = counter + 1
			if first == True:
				keys[imageArray[i][j]] = newKey
				first = False



print(keys)
# keys.reverse()

theKey = np.array(keys)

print(theKey)

c = decrypt(imageArray,theKey)

display(imageArray, theKey)