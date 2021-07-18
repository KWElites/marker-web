import qrcode.image.svg
from io import BytesIO
import zipfile
import qrcode
import os

def extractPackage(uploadedZip):
    images = ['jpg', 'png', 'jpeg']
    newDir='media/package/packages/'+str(uploadedZip.id)
    os.mkdir(newDir)
    uploadedZip.packageImages = 'package/packages/'+str(uploadedZip.id)
    uploadedZip.save()
    with zipfile.ZipFile(uploadedZip.packageItems, 'r') as z:
        for i in z.namelist():
            tempFileType = i.split('.')[-1]
            tempFileType = tempFileType.lower()
            if tempFileType in images:
                z.extract(i, newDir)


def getPackageItems(zip_path, path):
    validExtensions = ['jpg','png','jpeg']
    image_list = []
    with zipfile.ZipFile(zip_path,'r') as z:
        for file in z.namelist():
            print(file)
            ext = file.split('.')[-1]
            ext = ext.lower()
            if ext in validExtensions:
                img_path = (path+'/'+file).replace(" ", "%20")
                image_list.append(img_path)
    return image_list

def generatePackageQRCode(host, file_name):
    factory = qrcode.image.svg.SvgImage
    img = qrcode.make('http://'+host + file_name, image_factory=factory, box_size=17)
    stream = BytesIO()
    img.save(stream)
    return stream.getvalue().decode()
