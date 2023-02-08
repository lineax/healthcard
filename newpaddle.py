from paddleocr import PaddleOCR,draw_ocr
import re 
import cv2
import datetime

# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order.

def OCR(img_path, ocr):
    words = []
    result = ocr.ocr(img_path, cls=True)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            # print(line[1][0])
            words.append(line[1][0])
    
    return words

def parsing(words_list):
    for word in words_list:
        if re.findall(r"^[0-9].*[a-zA-Z]$", word):
            id = word

        if word.isupper() == True:
            if " " in word:
                name = word
                fname = name.split(" ")[0]
                lname = name.split(" ")[1]

        try:
            if datetime.datetime.strptime(word, "%Y-%m-%d"):
                dob = word
        except:
            None

        if re.findall(r"^[0-9].*", word):
            word = word.strip()
            full = word.replace("-", "")
            full = full.replace(".", "")
            if len(full) > 10:
                doi = f"{full[0:4]}-{full[4:6]}-{full[6:8]}"
                doe = f"{full[8:12]}-{full[12:14]}-{full[14:16]}"

    response_dict = {
        "First Name": fname,
        "Last Name": lname,
        "Health Card ID:": id,
        "DoB": dob,
        "DoI": doi,
        "Doe": doe

    }
    return response_dict

if __name__ == "__main__":
    ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
    img_path = "images/IMG_6637.jpg"
    list_of_words = OCR(img_path, ocr)
    final_results = parsing(list_of_words)
    print(final_results)

