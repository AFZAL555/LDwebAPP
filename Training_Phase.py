import os
from DBConnection import Db

staticpath="/home/afzal/Desktop/LDwebapp/static/"
mydataset=os.listdir(staticpath+"Train/")
for entry in mydataset:
    filename=entry.split(".") [0]
    label=filename.split("_") [1]

    mydataset_values = staticpath + "Train/" + entry

    from PIL import Image

    img = Image.open(mydataset_values)
    imgGray = img.convert('L')
    imgGray.save(staticpath + 'test_gray.jpg')

    import cv2

    img_gray = cv2.imread(staticpath + 'test_gray.jpg', 2)
    ret, bw_img = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
    img_binary = cv2.imwrite(staticpath + 'binary_image.jpg', bw_img)

    import numpy as np

    img_binary1 = cv2.imread(staticpath + 'binary_image.jpg', 0)
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(img_binary1, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(img_binary1, cv2.MORPH_CLOSE, kernel)
    img_binary2 = cv2.imwrite(staticpath + 'morphological.jpg', closing)

    ds = cv2.bitwise_not(closing)
    contour, hier = cv2.findContours(ds, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    for Cnt in contour:
        cv2.drawContours(ds, [Cnt], 0, 255, -1)
    gray = cv2.bitwise_not(ds)
    a = cv2.imwrite(staticpath + "Fill.jpg", gray)

    from skimage import io
    from skimage import img_as_ubyte
    from skimage.feature import greycomatrix, greycoprops

    rgbImage = io.imread(staticpath + "Fill.jpg")
    greyImage = img_as_ubyte(rgbImage)
    distances = [1, 2, 3]
    Angles = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
    properties = ['ASM', 'contrast', 'correlation', 'energy']
    glcm = greycomatrix(greyImage,
                        distances=distances,
                        angles=Angles,
                        symmetric=True,
                        normed=True)
    feats1 = np.hstack([greycoprops(glcm, 'ASM').ravel() for prop in properties])
    feats2 = np.hstack([greycoprops(glcm, 'contrast').ravel() for prop in properties])
    feats3 = np.hstack([greycoprops(glcm, 'correlation').ravel() for prop in properties])
    feats4 = np.hstack([greycoprops(glcm, 'energy').ravel() for prop in properties])

    K = np.mean(feats1)
    l = np.mean(feats2)
    m = np.mean(feats3)
    n = np.mean(feats4)
    
    db=Db()
    db.insert("INSERT INTO dataset_features(NAME,ASM,contrast,correlation,energy,label)VALUES('"+entry+"','"+str(K)+"','"+str(l)+"','"+str(m)+"','"+str(n)+"','"+label+"')")


print("Training Completed")

