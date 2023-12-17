from flask import Flask, request
import cv2
from PIL import Image

app1 = Flask(__name__)
app2 = Flask(__name__)

new_width, new_height = 128, 128
# 9x5 = 288x160
# 5x3 = 160x96
# 3x3 = 96x96
# 2x2 = 64x64
# 1x1 = 32x32

cap = cv2.VideoCapture(0)

def capture_frame():
    ret, frame = cap.read()
    resized_frame = cv2.resize(frame, (new_width, new_height))
    rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_frame)
    rgb_values = list(pil_image.getdata())
    return rgb_values

def split_and_format(rgb_values):
    num_values = len(rgb_values)
    half_point = num_values // 2
    first_part = rgb_values[:half_point]
    second_part = rgb_values[half_point:]

    formatted_first_part = ';'.join([','.join(map(str, rgb)) for rgb in first_part])
    formatted_second_part = ';'.join([','.join(map(str, rgb)) for rgb in second_part])

    return formatted_first_part, formatted_second_part

@app1.route('/')
def speed1():
    speed = request.args.get('speed', type=str)

    if speed == "Ok":
        captured_rgb_values = capture_frame()
        formatted_first_part, _ = split_and_format(captured_rgb_values)
        return formatted_first_part

@app2.route('/')
def speed2():
    speed = request.args.get('speed', type=str)

    if speed == "Ok":
        captured_rgb_values = capture_frame()
        _, formatted_second_part = split_and_format(captured_rgb_values)
        return formatted_second_part

if __name__ == '__main__':
    app1.run(host='0.0.0.0', port=80, debug=True)
    app2.run(host='0.0.0.0', port=8080, debug=True)