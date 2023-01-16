from PIL import ImageDraw, Image
import random 
import os 

def main(images_dir, size_img, rows, margin=5, column_max=6) : 

    # Get all screenshots in the folder
    all_images = []
    for filename in os.listdir(images_dir):
        if filename.endswith('.png'):
            all_images.append(images_dir+filename)

    # Create a new background
    background = Image.new('RGB', (size_img[0], size_img[1]), (0, 0, 0))
    background_copy = background.copy()

    # Calculate vertical and horizontal positions (to use in the loop)
    horizontal_start = margin/100 * size_img[0]
    vertical_start = []
    general_height = (size_img[1] - 2*margin/100 * size_img[1]) / rows
    for row in range(rows):
        vertical_start.append(margin/100 * size_img[1] + row * general_height)
    

    # Fill the image with the screenshots
    nb_page = 0
    limit_horizontal = (1 - 2*(margin/100)) * (column_max-1)/column_max * size_img[0] + margin/100 * size_img[0]
    while len(all_images) > 0:
        nb_page += 1
        for row in range(rows):
            row_done = False
            this_horizontal = horizontal_start
            this_vertical = vertical_start[row]
            while not row_done and len(all_images) != 0 : 
                # Pick, resize, and paste a random image
                this_image_name = random.choice(all_images)
                this_image = Image.open(this_image_name)
                new_height = int(general_height)
                new_width = int(this_image.size[0]*new_height/this_image.size[1])
                this_image = this_image.resize((new_width, new_height))
                background.paste(this_image, (int(this_horizontal), int(this_vertical)))
                all_images.remove(this_image_name)
                this_horizontal += new_width
                if this_horizontal > limit_horizontal :
                    row_done = True
                    this_horizontal = horizontal_start
        chemin_results = images_dir + "/assembled/"
        if not os.path.exists(chemin_results):
            os.makedirs(chemin_results)
        background.save(chemin_results + "page_" + str(nb_page) + ".png")
        background = background_copy.copy()
        if (len(all_images)) == 0 : 
            break

    print(nb_page, "images created")

main("../echantillon_images/done/",(1920,1080), 3)