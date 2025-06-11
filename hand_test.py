from matplotlib import pyplot as plt
import moondream as md
from PIL import Image
from PIL import ImageDraw, ImageFont
from dotenv import load_dotenv
import requests
import os
load_dotenv()

model = md.vl(api_key=os.getenv("MOONDREAM_API_KEY"))
plt.axis('off')

if not os.path.exists('hand.png'):
    url = "https://lab.artlung.com/six-finger-ai-hand/ai-generated-hand.png"
    response = requests.get(url)
    with open('hand.png', 'wb') as f:
        f.write(response.content)
    # remove black background
    image = Image.open('hand.png')
    plt.imshow(image)
    plt.savefig('hand.png')

image = Image.open('hand.png')
image.save('output.png')

finger_names = ["thumb", "index", "middle", "ring", "pinky", "extra"]
results = [
    {'points': [{'x': 0.7119140625, 'y': 0.51171875}]},
    {'points': [{'x': 0.6123046875, 'y': 0.35546875}]},
    {'points': [{'x': 0.4619140625, 'y': 0.3056640625}]},
    {'points': [{'x': 0.3828125, 'y': 0.35546875}]},
    {'points': [{'x': 0.3046875, 'y': 0.4072265625}]},
    {'points': []},
]
font = ImageFont.truetype("arial.ttf", 30)


def hand_test(i):
    image = Image.open("output.png").convert("RGBA")
    query = f"{finger_names[i]} finger"
    print(query)
    result = model.point(image, query)
    # result = results[i]
    print(result)
    points = result["points"]

    draw = ImageDraw.Draw(image)
    width, height = image.size

    for point in points:
        x = point["x"] * width
        y = point["y"] * height
        # Draw circle
        draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill=(255, 0, 0, 180))

        # Draw text
        draw.text((x, y - 50), f"{i + 1}", fill=(255, 255, 255, 255),
                  stroke_fill=(255, 0, 0, 180), font=font, stroke_width=5)

    image.save("output.png")
    plt.imshow(image)
    plt.show()


for i in range(6):
    hand_test(i)

query = "how many fingers are there?"
result = model.query(image, query)
print(result)
