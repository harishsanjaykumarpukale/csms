import cv2
import pytesseract
from pdf2image import convert_from_bytes
import numpy as np

def get_string(roi):
    rgb = cv2.cvtColor(roi,cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(rgb)

    return text.split()

def get_student_details(pdfbytes):

    # pages = convert_from_path(filepath, 350)
    pages  = convert_from_bytes(pdfbytes, 350)
    # pages[0].save("page1.jpg","JPEG")

    # img = cv2.imread("page1.jpg")
    img = np.array(pages[0])

    # print(type(img))

    student = {}

    '''roi for student name'''
    roi = img[1590:1690,1200:2200]
    student['f_name'] = get_string(roi)[0]
    student['l_name'] = get_string(roi)[1]

    '''roi for student usn'''
    roi = img[1760:1860,1200:2200]
    student['usn'] = get_string(roi)[0]

    '''roi for student email-id'''
    roi = img[1850:1950,1200:2200]
    student['s_email'] = get_string(roi)[0]

    '''roi for student's counsellor email-id'''
    roi = img[2500:2600,1200:2200]
    student['c_email'] = get_string(roi)[0]

    return student


# print(get_student_details("5_6138656761713787275.pdf"))