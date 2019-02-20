from PIL import Image
import glob
import random
import json

mosaic_size = 30, 17  # You just have to edit these in the code - sorry
tessera_width = 150  # Check out that cool new vocab I just learned
total_images = mosaic_size[0] * mosaic_size[1]

result_image = Image.new("RGB", (mosaic_size[0] * tessera_width,
                                 mosaic_size[1] * tessera_width))

# Get a list of png files in the folder
file_names = glob.glob("*.png")

# Create a shuffled (and repeated if necessary) list of images to use
image_order = []
for i in range(total_images // len(file_names)):
    random.shuffle(file_names)
    image_order += file_names
random.shuffle(file_names)
image_order += file_names[:total_images - len(image_order)]

# Add each image to the result image
for i in range(total_images):
    file_name = image_order[i]
    im_position = ((i % mosaic_size[0]) * tessera_width,
                   (i // mosaic_size[0]) * tessera_width)

    # Crop and resize the image
    im = Image.open(file_name)
    cropped_width = min(im.size)
    im = im.crop(((im.size[0] - cropped_width) / 2,
                  (im.size[1] - cropped_width) / 2,
                  (im.size[0] - cropped_width) / 2 + cropped_width,
                  (im.size[1] - cropped_width) / 2 + cropped_width))
    im = im.resize((tessera_width, tessera_width), resample=Image.BICUBIC)

    # Paste the edited image into the result image
    result_image.paste(im, im_position)  # MAL: NMatt94

# Save the result image and the order of the images used
result_image.save("result.png")
with open("image_order.json", "w") as opf:
    json.dump(image_order, opf, indent=2)
