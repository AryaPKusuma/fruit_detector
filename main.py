import cv2, numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def fruit_detector2(image):
    # rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_mean = image.copy()
    dst = cv2.pyrMeanShiftFiltering(img_mean, 10, 50)
    dst_rgb = cv2.cvtColor(dst, cv2.COLOR_BGR2RGB)
    dst_hsv = cv2.cvtColor(dst, cv2.COLOR_BGR2HSV)
    cv2.imshow('aseli', dst_hsv)
    hsv_image = cv2.cvtColor(dst_rgb, cv2.COLOR_RGB2HSV)

    lower_color = np.array([160, 50, 80])
    upper_color = np.array([180, 255, 255])

    lower_apple = np.array([0, 150, 100])
    upper_apple = np.array([11, 255, 255])

    mask1 = cv2.inRange(hsv_image, lower_color, upper_color)
    mask2 = cv2.inRange(hsv_image, lower_apple, upper_apple)
    mask = mask1 + mask2
    
    kernel = np.ones((5, 5), np.uint8)
    img_opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=4)
    img_dilated = cv2.dilate(img_opening, kernel, iterations=2)
    img_close = cv2.morphologyEx(img_dilated, cv2.MORPH_CLOSE, kernel, iterations=1)

    final_mask = img_close

    contour_count = 0
    contours, _ = cv2.findContours(final_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.drawContours(image,contours,-1,(255,0,0),1)
    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        contour_count = contour_count + 1

    resized_mask = cv2.resize(final_mask, (700, 700))
    cv2.imshow('Masking',resized_mask)
    resized_img = cv2.resize(image, (700, 700))
    cv2.imshow(f"Jumlah Deteksi : {contour_count}", resized_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def increase_saturation(image, saturasi_factor):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:,:,1] = np.clip(hsv[:,:,1] * saturasi_factor, 0, 255).astype(np.uint8)
    hasil = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return hasil

def on_convert_button_click():
    file_path = file_path_var.get()
    if file_path:
        img = cv2.imread(file_path)
        img = increase_saturation(img, 1.2)
        fruit_detector2(img)

def on_select_button_click():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    if file_path:
        file_path_var.set(file_path)
        display_selected_image(file_path)

def display_selected_image(file_path):
    image = Image.open(file_path)
    image = image.resize([300, 300])
    tk_image = ImageTk.PhotoImage(image)
    selected_image_label.config(image=tk_image)
    selected_image_label.image = tk_image


root = tk.Tk()
root.title("Fruit Detector App")
file_path_var = tk.StringVar()

select_button = tk.Button(root, text="Pilih Gambar", command=on_select_button_click)
select_button.pack(pady=10)

selected_image_label = tk.Label(root)
selected_image_label.pack(pady=10)

convert_button = tk.Button(root, text="hitung", command=on_convert_button_click)
convert_button.pack(pady=10)

root.mainloop()