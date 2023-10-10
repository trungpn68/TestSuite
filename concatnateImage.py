from PIL import Image, ImageDraw, ImageFont
import io

def drawDict(dic):
    string = ""
    for key, value in dic.items():
        if type(value) == dict:
            value = drawDict(value)
        string += f"{key}: {value}\n"
    return string

def concatNimageAndText(input_images, paramDict, output_image):
    if not input_images:
        return

    images = []
    for image in input_images:
        temp = Image.open(io.BytesIO(image))
        temp.thumbnail((1024, 1024))
        images.append(temp)

    image_text_width = 800
    image_text_height = max([image.height for image in images] + [1024])
    # Create an image with the text
    font_size = 16
    font_color = (255, 255, 255)  # White color
    background_color = (0, 0, 0)  # Black background color

    font = ImageFont.truetype('JetBrainsMonoNerdFont-Bold.ttf', font_size)
    image_with_text = Image.new("RGB", (image_text_width, image_text_height), background_color)
    draw = ImageDraw.Draw(image_with_text)
    text_position = (0, 0)
    text = drawDict(paramDict)
    draw.text(text_position, text, fill=font_color, font=font)


    # Calculate the dimensions of the merged image
    widths = [0]
    for image in images:
        widths.append(widths[-1] + image.width)

    # Create a blank image with the calculated dimensions
    merged_image = Image.new("RGB", (widths[-1]+image_text_width, image_text_height))

    for i in range(len(images)):
        merged_image.paste(images[i], (widths[i], 0))

    merged_image.paste(image_with_text, (widths[-1] + 50 , 50))

    # Save the merged image
    merged_image.save(output_image)

# Open the two images you want to merge
def concat2imageAndText(image1, image2, paramDict, output_image):
    image1 = Image.open(io.BytesIO(image1))
    image2 = Image.open(io.BytesIO(image2))

    image1.thumbnail((1024, 1024))
    image2.thumbnail((1024, 1024))

    image_text_width = max(image1.width, image2.width)
    image_text_height = max(image1.height, image2.height)
    # Create an image with the text
    font_size = 16
    font_color = (255, 255, 255)  # White color
    background_color = (0, 0, 0)  # Black background color

    font = ImageFont.truetype('JetBrainsMonoNerdFont-Bold.ttf', font_size)
    image_with_text = Image.new("RGB", (image_text_width, image_text_height), background_color)
    draw = ImageDraw.Draw(image_with_text)
    text_position = (0, 0)
    text = ""
    for key, value in paramDict.items():
        text += f"{key}: {value}\n"
    draw.text(text_position, text, fill=font_color, font=font)


    # Calculate the dimensions of the merged image
    width = image1.width + image2.width + image_with_text.width
    height = max(image1.height, image2.height, image_with_text.height)

    # Create a blank image with the calculated dimensions
    merged_image = Image.new("RGB", (width, height))

    # Paste the images onto the merged image
    merged_image.paste(image1, (0, (height - image1.height) // 2))
    merged_image.paste(image2,  (image1.width, (height - image_with_text.height) // 2))
    merged_image.paste(image_with_text, (image1.width + image_with_text.width, (height - image2.height) // 2))

    # Save the merged image
    merged_image.save(output_image)

if __name__ == "__main__":
    with open("image1.png", "rb") as im1:
        image1 = im1.read()

    with open("image2.jpg", "rb") as im2:
        image2 = im2.read()
    
    concatNimageAndText([image1, image2], {
        "Trung": "Name",
        "Age": 45,
        "Style": "Naruto"
    }, "output.jpg")