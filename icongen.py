import os
import argparse
from datetime import datetime
try:
    from PIL import Image
except ImportError as ie:
    try:
        import subprocess
        import sys
        subprocess.check_call([sys.executable,'-m','pip','install','Pillow'])
    except Exception as ex:
        print('Network Error:\
            \n\tTry after connecting to network')



def image_creator(image,size,folder,name='ic_launcher.png'):
    tmp=image.resize(size)
    tmp.save(os.path.join(folder,name))


if __name__=='__main__':
    parser = argparse.ArgumentParser("Creates icons compatible to Android and iOS projects from an input image")
    parser.add_argument('--img',dest='img',required=True,help='Image to create icons from')
    parser.add_argument('--output',dest='output',required=False,help='Target folder name <<optional>> (Careful,\\\nOverwrites the existing contents of the directory if the directory is present             )')
    parser.add_argument('--android',required=False,type=lambda x: x in ['y','yes','true','True','Y'],default=True,help="Boolean Flag for Android \n\t['y','yes','true','True','Y']\t for True anything else for False")
    parser.add_argument('--ios',required=False,default=False,type=lambda x:x in ['y','yes','true','True','Y'],help="Boolean flag for iOS\n\t['y','yes','true','True','Y']\t for True anything else for False")
    args = parser.parse_args()

    img = Image.open(args.img)
    uniq = str(datetime.timestamp(datetime.now()))
    target_folder = 'AppIcons('+uniq+')'
    if args.output:
        target_folder = args.output
    path = os.getcwd()
    os.mkdir(os.path.join(path, target_folder))
    android_path,ios_path = '', ''
    if args.android:
        img.save(os.path.join(os.path.join(path, target_folder), 'playstore.png'))
        img = Image.open(os.path.join(os.path.join(path, target_folder), 'playstore.png'))
        os.mkdir(os.path.join(os.path.join(path, target_folder), 'android'))
        android_path = os.path.join(os.path.join(path, target_folder), 'android')
    if args.ios:
        img.save(os.path.join(os.path.join(path, target_folder), 'appstore.png'))
        img = Image.open(os.path.join(os.path.join(path, target_folder), 'appstore.png'))
        os.mkdir(os.path.join(os.path.join(path, target_folder), 'Assets.xcassets'))
        ios_path = os.path.join(os.path.join(os.path.join(path, target_folder), 'Assets.xcassets'), 'AppIcon.appiconset')
        os.mkdir(ios_path)
    if android_path:
        folder_names = [('mipmap-mdpi',(48,48)),('mipmap-hdpi',(72,72)),('mipmap-xhdpi',(96,96)),('mipmap-xxhdpi',(144,144)),('mipmap-xxxhdpi',(192,192))]
        for name,size in folder_names:
            folder = os.path.join(android_path, name)
            os.mkdir(folder)
            image_creator(img, size, folder)
    if ios_path:
        sizes = [(29,29),(40,40),(57,57),(58,58),(60,60),(80,80),(87,87),(114,114),(120,120),(180,180),(1024,1024)]
        for size in sizes:
            image_creator(img, size, ios_path, str(size[0])+'.png')


##End of the Script