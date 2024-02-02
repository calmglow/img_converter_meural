from PIL import Image
import os
import sys

def crop_to_16_9(img):
    original_width, original_height = img.size
    # For portrait images, calculated in 9:16 ratio
    if original_width >= original_height:  # Horizontal image
        target_aspect = 16 / 9
    else:  # Portrait
        target_aspect = 9 / 16  # For portrait images, reverse the ratio to
    original_aspect = original_width / original_height
    
    # Horizontal image
    if original_width >= original_height:
        if 16/6> original_aspect > target_aspect:
            # width
            new_height = original_height
            new_width = int(new_height * target_aspect)
        elif 16/12 < original_aspect < target_aspect:
            # height
            new_width = original_width
            new_height = int(new_width / target_aspect)
        else:
            return img
    # Portrait image
    else:
        if 9/19 < original_aspect < target_aspect:  
            new_width = original_width
            new_height = int(new_width * target_aspect)
        elif 9/13 > original_aspect > target_aspect:  
            new_height = original_height
            new_width = int(new_height * target_aspect)
        else:
            return img

    left = (original_width - new_width) / 2
    top = (original_height - new_height) / 2
    right = left + new_width
    bottom = top + new_height

    img = img.crop((left, top, right, bottom))
    return img

def adjust_and_crop_image(file_path):
    # Open the image file
    with Image.open(file_path) as img:
        # First, crop the image if necessary to get closer to a 16:9 ratio
        img = crop_to_16_9(img)
        
        # Then, resize or add padding to precisely adjust to 16:9 if needed
        # This part remains the same as the previous script, adjusting based on the new aspect ratio
        original_width, original_height = img.size
        target_aspect = 16 / 9
        new_width, new_height = (1920, 1080) if original_width >= original_height else (1080, 1920)
        
        # Resize image with a white background for aspect ratios far from 16:9
        new_img = Image.new("RGB", (new_width, new_height), "white")
        img.thumbnail((new_width, new_height), Image.LANCZOS)
        x = (new_width - img.size[0]) // 2
        y = (new_height - img.size[1]) // 2
        new_img.paste(img, (x, y))
        
        return new_img

def process_images(source_directory, target_directory):
    formats = ('.jpg', '.jpeg', '.png')
    
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    for filename in os.listdir(source_directory):
        if filename.lower().endswith(formats):
            file_path = os.path.join(source_directory, filename)
            img = adjust_and_crop_image(file_path)
            new_file_path = os.path.join(target_directory, filename)
            img.save(new_file_path)


if __name__ == "__main__":
    source_directory = sys.argv[1] if len(sys.argv) > 1 else 'input'
    target_directory = sys.argv[2] if len(sys.argv) > 2 else 'output'
    process_images(source_directory, target_directory)