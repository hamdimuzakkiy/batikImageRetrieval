__author__ = 'hamdiahmadi'

import pywt
import cv2
import numpy
import os
import xlwt
import xlrd
from xlutils.copy import copy

class wavelet:

    def __init__(self):
        pass

    def toWavelet(self,image):
        return pywt.dwt2(image,'db4')

class file:

     def __init__(self):
         pass

     def readFolder(self,path):
         return os.listdir(path)

class image:

    def __init__(self):
        pass

    def toGrayScale(self,image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def readImage(self,path):
        return cv2.imread(path)

    def showImage(self,imageName,order):
        path = 'Data Batik/'+imageName
        images = self.readImage(path)
        while len(images) < 200:
            images = cv2.pyrUp(images)
        cv2.imshow(str(order)+" - "+imageName,images)

class data:

    def __init__(self):
        pass

    def calMean(self,image):
        return numpy.mean(image)

    def calDev(self,image):
        return numpy.std(image)

    def euclid(self,data1,data2):
        res = 0
        for x in range(0,len(data1)):
            res+=pow((data1[x]-data2[x]),2)
        return numpy.sqrt(res)

    def canberra(self,data1,data2):
        res = 0
        bawah = 0
        for x in range(0,len(data1)):
            res+=abs((data1[x]-data2[x]))
            bawah+=(abs(data1[x])+abs(data2[x]))
        return float(res)/float(bawah)

class excell:
     def __init__(self):
         pass

     def write(self,path,content):
        wb = xlrd.open_workbook(filename=path)
        data = wb.sheet_by_index(0)
        wb2 = copy(wb)
        data2 = wb2.get_sheet(0)
        row = 0
        for x in content :
            col = 0
            for y in x:
                data2.write(data.nrows+row,col,y)
                col+=1
            row+=1
        wb2.save(path)

     def readDataSet(self,path):
        wb = xlrd.open_workbook(filename=path)
        data = wb.sheet_by_index(0)
        dataSets = []
        for x in range(0,data.nrows):
            content = data.row(x)
            tmp = []
            for idx,cell_obj in enumerate(content):
                tmp.append(cell_obj.value)
            dataSets.append(tmp)
        return dataSets

class main(wavelet,image,data,file,excell):

    def __init__(self):
        pass

    def do(self,path):
        img = image.readImage(self,path)
        img = image.toGrayScale(self,img)
        arr = []
        for x in range(0,5):
            img,(cH,cV,cD) = wavelet.toWavelet(self,img)
            arr.append(data.calMean(self,img))
            arr.append(data.calDev(self,img))
            arr.append(data.calMean(self,cH))
            arr.append(data.calDev(self,cH))
            arr.append(data.calMean(self,cV))
            arr.append(data.calDev(self,cV))
            arr.append(data.calMean(self,cD))
            arr.append(data.calDev(self,cD))
        return arr

    def getBatik(self,path,datasetPath,total):
        srch = self.do(path)
        dataset = excell.readDataSet(self,datasetPath)
        res = []
        for x in dataset:
            # result = data.euclid(self,srch,x)
            result = data.canberra(self,srch,x)
            res.append((result,x[40]))
        dtype = [('val', float),('name','S101')]
        res = numpy.array(res,dtype=dtype)
        res = numpy.sort(res,order='val')

        for x in res:
            print x
        path = path.split('/')[1]
        while True:
            image.showImage(self,path,"Original")
            for x in range(0,total):
                image.showImage(self,res[x][1],x+1)
                cv2.waitKey(1)




    def getDataSet(self,path):
        data = []
        for x in file.readFolder(self,path):
            x = str(x)
            length = len(x)
            num = (x[length-5])
            if (x.split('.')[1] == 'jpg'):
                if (num == '5' or num == '6'):
                    pass
                else:
                    tmp = self.do(path+'/'+x)
                    tmp.append(x)
                    data.append(tmp)
        path = 'dataset.xls'
        excell.write(self,path,data)


if __name__ == '__main__':

    mainmain = main()

    # mengambil dataset
    # path = 'Data Batik'
    # mainmain.getDataSet(path)

    # path = 'Data Batik/B44_6.jpg'
    path = 'Data Batik/'+raw_input()
    datasetPath = 'dataset.xls'
    total = 4
    mainmain.getBatik(path,datasetPath,total)
