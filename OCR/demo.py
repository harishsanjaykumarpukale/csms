import cv2
import pytesseract
img = cv2.imread("Page_1.jpg")
# roi = img[1500:2000,1040:2300]
# roi = img[1600:2000,1100:2500]
roi = img[1590:1690,1200:2200]
cv2.imshow("img",roi)
# # Exiting the window if 'q' is pressed on the keyboard. 
if cv2.waitKey(0) & 0xFF == ord('q'):  
    cv2.destroyAllWindows() 
rgb = cv2.cvtColor(roi,cv2.COLOR_BGR2RGB)

text = pytesseract.image_to_string(rgb)


print(text)

l = text.split()

print(l)


'''usn'''

roi = img[1760:1860,1200:2200]
cv2.imshow("img",roi)
# # Exiting the window if 'q' is pressed on the keyboard. 
if cv2.waitKey(0) & 0xFF == ord('q'):  
    cv2.destroyAllWindows() 
rgb = cv2.cvtColor(roi,cv2.COLOR_BGR2RGB)

text = pytesseract.image_to_string(rgb)

print(text)

l = text.split()

print(l)


'''email'''
roi = img[1850:1950,1200:2200]
cv2.imshow("img",roi)
# # Exiting the window if 'q' is pressed on the keyboard. 
if cv2.waitKey(0) & 0xFF == ord('q'):  
    cv2.destroyAllWindows() 
rgb = cv2.cvtColor(roi,cv2.COLOR_BGR2RGB)

text = pytesseract.image_to_string(rgb)


print(text)

l = text.split()

print(l)


'''counsellor's email'''

roi = img[2500:2600,1200:2200]
cv2.imshow("img",roi)
# # Exiting the window if 'q' is pressed on the keyboard. 
if cv2.waitKey(0) & 0xFF == ord('q'):  
    cv2.destroyAllWindows() 
rgb = cv2.cvtColor(roi,cv2.COLOR_BGR2RGB)

text = pytesseract.image_to_string(rgb)


print(text)

l = text.split()

print(l)