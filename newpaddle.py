# from paddleocr import PaddleOCR
import re 
# import cv2
import datetime
# # import fitz
# import os
# import glob


# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order.

def OCR(img_path, ocr):
    words = []
    result = ocr.ocr(img_path, cls=True)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            words.append(line[1][0])
            # print(line[1][0])
    # print(words)
    return words

# def pdfconverter(fname, folder):
#     dpi = 300  # choose desired dpi here
#     zoom = dpi / 72  # zoom factor, standard: 72 dpi
#     magnify = fitz.Matrix(zoom, zoom)  # magnifies in x, resp. y direction
#     doc = fitz.open(fname)  # open document
#     for page in doc:
#         pix = page.get_pixmap(matrix=magnify)  # render page to an image
#         pix.save(f"{folder}/page-{page.number}.png")

def parsing(words_list):
    is_name_detected = False
    is_dob_detected = False
    is_doine_detected = False
    is_id_detected = False
    fname="Not Detected"
    lname="Not Detected"
    id="Not Detected"
    dob="Not Detected"
    doi="Not Detected"
    doe="Not Detected"
    list_of_dates = []
    
    
    for word in words_list:
        word=str(word)
        if re.findall(r"^[0-9].*[a-zA-Z]$", word) and not is_id_detected:
            id = word
            is_id_detected = True
            continue
            

        if word.isupper() == True and not is_name_detected:
            if " " in word:
                name = word
                fname = name.split(" ")[0]
                lname = name.split(" ")[-1]
                # print(name,fname,lname)
                is_name_detected = True
                continue
            else:
                fname=word
                is_name_detected = True
                continue
                
        try:
            word=word.replace(".","-")
            if datetime.datetime.strptime(word, "%Y-%m-%d") and not is_dob_detected:
                dob = word
                is_dob_detected = True
                continue
        except:
            pass

        if re.findall(r'^[\d.-]+$', word):
            list_of_dates.append(re.findall(r'^[\d.-]+$', word))
            continue

    # print("dates: ",list_of_dates)
    # print(len(list_of_dates))
    
    if len(list_of_dates) == 2:
        if is_dob_detected:
            dates_without_chars=[]
            for element in list_of_dates:
                element=element[0]
                dates_without_chars.append(int(str(element).replace("-","").replace(".","").replace("[","").replace("]","").replace("'","")))
            sorted_dates = sorted(dates_without_chars)
            # conveert each elem of list to str
            sorted_dates = [str(i) for i in sorted_dates]
            doi=f"{sorted_dates[0][0:4]}-{sorted_dates[0][4:6]}-{sorted_dates[0][6:8]}"
            doe=f"{sorted_dates[1][0:4]}-{sorted_dates[1][4:6]}-{sorted_dates[1][6:8]}"
            is_doine_detected = True
        else:
            dates_without_chars=[]
            for element in list_of_dates:
                element=element[0]
                dates_without_chars.append(int(str(element).replace("-","").replace(".","").replace("[","").replace("]","").replace("'","")))
            sorted_dates = sorted(dates_without_chars)
            
            dob=f"{str(sorted_dates[0])[0:4]}-{str(sorted_dates[0])[4:6]}-{str(sorted_dates[0])[6:8]}"
            doi=f"{str(sorted_dates[1])[0:4]}-{str(sorted_dates[1])[4:6]}-{str(sorted_dates[1])[6:8]}"
            doe=f"{str(sorted_dates[1])[8:12]}-{str(sorted_dates[1])[12:14]}-{str(sorted_dates[1])[14:16]}"
            is_dob_detected = True
            is_doine_detected = True
    elif len(list_of_dates) == 1: 
        if is_dob_detected:
            word = str(list_of_dates[0]).strip('[]').strip("'")
            full = word.replace("-", "")
            full = full.replace(".", "")
            doi = f"{full[0:4]}-{full[4:6]}-{full[6:8]}"
            doe = f"{full[8:12]}-{full[12:14]}-{full[14:16]}"
            is_doine_detected = True
        else:
            word = str(list_of_dates[0]).strip('[]').strip("'")
            full = word.replace("-", "")
            full = full.replace(".", "")
            dob = f"{full[0:4]}-{full[4:6]}-{full[6:8]}"
            is_dob_detected = True
    elif len(list_of_dates) == 3:
        dates_without_chars=[]
        for element in list_of_dates:
            element=element[0]
            dates_without_chars.append(int(str(element).replace("-","").replace(".","").replace("[","").replace("]","").replace("'","")))
        sorted_dates = sorted(dates_without_chars)
        sorted_dates = [str(i) for i in sorted_dates]
        dob=f"{sorted_dates[0][0:4]}-{sorted_dates[0][4:6]}-{sorted_dates[0][6:8]}"
        doi=f"{sorted_dates[1][0:4]}-{sorted_dates[1][4:6]}-{sorted_dates[1][6:8]}"
        doe=f"{sorted_dates[2][0:4]}-{sorted_dates[2][4:6]}-{sorted_dates[2][6:8]}"
        is_doine_detected = True
        is_dob_detected = True

    response_dict = {
        "First Name": fname,
        "Last Name": lname,
        "Health Card ID": id,
        "DoB": dob,
        "DoI": doi,
        "Doe": doe

    }
    return response_dict

# def empty_directory(directory):
#     files = glob.glob(f'{directory}/*')
#     for f in files:
#         os.remove(f)

# if __name__ == "__main__":
#     ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory
#     img_path = "images/IMG_6637.jpg"
#     list_of_words = OCR(img_path, ocr)
#     final_results = parsing(list_of_words)
#     print(final_results)
