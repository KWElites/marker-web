import zipfile

def validZip(uploadedZip):
    validExtensions = ['jpg', 'png', 'jpeg', 'obj', 'md2', 'g3d', 'g3dt']
    with zipfile.ZipFile(uploadedZip, 'r') as z:
        for i in z.namelist():
            tempFileType = i.split('.')[-1]
            tempFileType = tempFileType.lower()
            if i[-1] == '/':
                continue
            if (tempFileType not in validExtensions):
                return False
    return True