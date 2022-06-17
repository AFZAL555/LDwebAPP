from PIL import Image
class test1:
    def __init__(self):
        self.mydataset_values=""
        self.staticpath="home\\afzal\\Desktop\\LDwebapp\\static\\"
        self.result=""

    def find_result(self,filename):
        self.mydataset_values = self.staticpath + "uploads\\"+ filename

        img = Image.open(self.mydataset_values)
        imgGray = img.convert('L')
        imgGray.save(self.staticpath + 'test_gray.jpg')

        import cv2

        img_gray = cv2.imread(self.staticpath + 'test_gray.jpg', 2)
        ret, bw_img = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)
        img_binary = cv2.imwrite(self.staticpath + 'binary_image.jpg', bw_img)

        import numpy as np

        img_binary1 = cv2.imread(self.staticpath + 'binary_image.jpg', 0)
        kernel = np.ones((5, 5), np.uint8)
        opening = cv2.morphologyEx(img_binary1, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(img_binary1, cv2.MORPH_CLOSE, kernel)
        img_binary2 = cv2.imwrite(self.staticpath + 'morphological.jpg', closing)

        ds = cv2.bitwise_not(closing)
        contour, hier = cv2.findContours(ds, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        for Cnt in contour:
            cv2.drawContours(ds, [Cnt], 0, 255, -1)
        gray = cv2.bitwise_not(ds)
        a = cv2.imwrite(self.staticpath + "Fill.jpg", gray)

        from skimage import io
        from skimage import img_as_ubyte
        from skimage.feature import greycomatrix, greycoprops

        rgbImage = io.imread(self.staticpath + "Fill.jpg")
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



        from DBConnection import Db


        test_value=[[K,l,m,n]]
        db=Db()
        res=db.select("SELECT*FROM dataset_features")
        train_features=[]
        train_labels=[]
        for row in res:
            train_labels.append(row['label'])
            ar=[]
            ar.append(row['ASM'])
            ar.append(row['contrast'])
            ar.append(row['correlation'])
            ar.append(row['energy'])
            train_features.append(ar)

        from sklearn.ensemble import RandomForestClassifier
        clf=RandomForestClassifier(n_estimators=100)


        clf.fit(train_features,train_labels)
        y_pred=clf.predict(test_value)

        if y_pred==[0] :
            print("Negative")
            self.result="Result---> Negative"

        else:
            
            print("Positive")
            if((K>0.36 and K<=0.55)and(l>1983 and l<2567)and(m>0.90 and m<=0.93)and(n>0.60 and n<=0.71)):
                print("stage-1")
                st="stage-1"
            elif((K>0.55 and K<=0.75)and(l>1084 and l<1243)and(m>0.93 and m<=0.95)and(n>0.71 and n<=0.81)):
                 print("stage-2")
                 st="stage-2"
            elif((K>0.75 and K<0.90)and(l>179 and l<499)and(m>0.95 and m<0.98)and(n>0.81 and n<0.95)):
                print("stage-3")
                st="stage-3"
            else:
                print("cannot identified the stage")
                st="cannot identified the stage"
            self.result=" Postive , Current"+st
        print("Test Completed")
        return self.result


