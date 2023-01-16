from PIL import ImageDraw, Image
import random 
import os 

def main(images_dir, size_img) : 

    for filename in os.listdir(images_dir):
        if filename.endswith('.png'):
            # Pick and resize the image 
            this_image = Image.open(images_dir+filename)
            new_width = (int(size_img[0]))
            new_height = int(this_image.size[1]*new_width/this_image.size[0])
            this_image = this_image.resize((new_width, new_height))
            # Calculate the mean color 
            colors = this_image.getcolors(this_image.size[0]*this_image.size[1])
            mean_color = [int(sum(x[1][i] * x[0] for x in colors) / sum(x[0] for x in colors)) for i in range(3)]
            # Create the background
            background = Image.new('RGB', (size_img[0], size_img[1]),tuple(mean_color))
            chemin_results = images_dir + "/prepared/"
            # Paste the image 
            background.paste(this_image, (0, int((size_img[1]-new_height)/2)))
            # Save the image
            if not os.path.exists(chemin_results):
                os.makedirs(chemin_results)
            background.save(chemin_results + filename)




main("../echantillon_images/done/",(1080,1920))