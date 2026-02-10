import glob
import os
import random

def generate_html_text(directory):
    files = glob.glob(os.path.join(directory, '*.jpeg'))
    random.shuffle(files)
    text = ""
    for file in files:
        text = text + """<div class="swiper-slide">\n"""
        text = text + """    <img src=""" +file+ """ alt="">\n"""
        text = text + """</div>\n"""
        text = text + "\n"
    return text

if __name__ == "__main__":
    directory = "./header_images/photos_for_website/"
    #<div class="swiper-slide">
    #   <img src="images2/image2.jpg" alt="">
    #</div>
    #<div class="col-4"><span class="image fit"><img src="images/pic01.jpg" alt="" /></span></div>
    print("\n\n\n")
    a = generate_html_text(directory)
    print(a)
    pass
