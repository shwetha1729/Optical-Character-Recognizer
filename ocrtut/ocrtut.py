import cv2
list1=[]
grid1=[]
letters=list(letter for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ");	#English letters, change this to digits if recognising digits, and change the template file to the appropriate file
ipfile=input("Enter the image");
img = cv2.imread(ipfile);
C,H,W = img.shape[::-1];

gray =cv2.cvtColor(img,cv2.COLOR_BGR2GRAY);
ret, thresh =cv2.threshold(gray,47,255,cv2.THRESH_BINARY);
contours,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE);
for i in range(len(contours)):
	perimeter=cv2.arcLength(contours[i],True);
	if(perimeter>250 and perimeter<350):	#approx size of letters we're looking for, on removing this condition, we get all possible contours: see SCREENSHOTS/lettercontours.png
		cv2.drawContours(img,contours,i,(0,255,0),2);
		list1.append(i);
cv2.imshow("contours",img);
print "Number of segments found: "
print str(len(list1))
count=0
for x in list1:
	count+=1
	M =cv2.moments(contours[x]);
	cx =int(M['m10']/M['m00'])
	cy =int(M['m01']/M['m00'])
	cropped = img[cy-40:cy+40,cx-40:cx+40]
	cv2.imwrite("cropped"+str(count)+ipfile, cropped) #this is for demo purposes only, You need not write each cropped segment to a file, we did it to make sure it is recognising correctly.
	print "cropped created" + str(count)
	w,h,c =cropped.shape
	for i in range(26):	#range of templates : number of alphabets
		temp="plain-alpha/"+letters[i]+".png";		#to recognise a custom template image, we would change the filename here -- for different language alphabets
		template=cv2.imread(temp);
		result = cv2.matchTemplate(cropped,template,cv2.TM_CCOEFF_NORMED)
		minval,maxval,minloc,maxloc = cv2.minMaxLoc(result)
		print "letter is" +letters[i]+"maxval is "+str(maxval)
		if(maxval>0.5):		#change this to whatever threshold seems approppriate for your image
			grid1.append(letters[i])
print "grid1: "
print grid1
#cv2.imshow("thresh",thresh);
#cv2.imshow("original",img);

cv2.waitKey(0);
cv2.destroyAllWindows();
