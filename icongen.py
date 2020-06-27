import os
import argparse
import sys
from datetime import datetime
try:
    from PIL import Image
except ImportError as ie:
    print('PIL Not Found\nTrying to install Pillow library..........')
    try:
        import subprocess
        import importlib
        import site
        subprocess.check_call([sys.executable,'-m','pip','install','Pillow'])
        importlib.reload(site)
    except Exception as ex:
        print('Probably Network Error:\
            \n\tTry after connecting to network\
            \nStack Trace:\t',ex)
        print('This script does not work without PIL library\nExiting.................')
        sys.exit(1)
finally:
    from PIL import Image



def image_creator(image,size,folder,name='ic_launcher.png'):
    '''Creates image of given size with given name in the given directory
    Arguments:
        image  : <class 'PIL.JpegImagePlugin.JpegImageFile'>
        size   : <class 'tuple'>
        folder : <class 'str'>
        name   : <class 'str'>
    Return Type:
        None'''
    tmp=image.resize(size)
    tmp.save(os.path.join(folder, name))


def parse_arguments():
    '''Parses the arguments from command line 
    Arguments:
        None
    Return Type:
        <class 'argparse.Namespace'>'''
    parser = argparse.ArgumentParser(description="Creates icons compatible to Android and iOS projects \
        from an input image")
    parser.add_argument('--img', dest='img', required=True,help='Image to create icons from')
    parser.add_argument('--output', dest='output', required=False, help='Target folder name <<optional>> ')
    parser.add_argument('--android', dest='android',action='store_true', required=False, default=False,\
        help="Boolean Flag for Android ")
    parser.add_argument('--ios', dest='ios', action='store_true', required=False, default=False, \
        help="Boolean flag for iOS")
    return parser.parse_args()

def main():
    '''Utility function to create required directories and icons
    Arguments:
        None
    Return Type:
        None'''
    args=parse_arguments()
    print("Arguments:")
    for element in vars(args):
        print(f'\t{element:<10}:  {getattr(args,element)}')
    
    img = Image.open(args.img)
    target_folder = 'AppIcons('+str(datetime.timestamp(datetime.now()))+')'    #Creating timestamp for uniqueness
    if args.output:
        target_folder = args.output
    path = os.getcwd()
    try:
        os.mkdir(os.path.join(path, target_folder))
    except FileExistsError as fe:
        print('Target Folder already present')
        print('StackTrace :',fe,'\nExiting..................')
        sys.exit(1)
    android_path,ios_path = '', ''
    if args.android:
        img.save(os.path.join(os.path.join(path, target_folder), 'playstore.png'))
        img = Image.open(os.path.join(os.path.join(path, target_folder), 'playstore.png'))
        android_path = os.path.join(os.path.join(path, target_folder), 'android')
        os.mkdir(android_path)
    if args.ios:
        img.save(os.path.join(os.path.join(path, target_folder), 'appstore.png'))
        img = Image.open(os.path.join(os.path.join(path, target_folder), 'appstore.png'))
        os.mkdir(os.path.join(os.path.join(path, target_folder), 'Assets.xcassets'))
        ios_path = os.path.join(os.path.join(os.path.join(path, target_folder),\
             'Assets.xcassets'), 'AppIcon.appiconset')
        os.mkdir(ios_path)
    if android_path:
        folder_names = [('mipmap-mdpi',(48,48)),('mipmap-hdpi',(72,72)),('mipmap-xhdpi',(96,96)),\
            ('mipmap-xxhdpi',(144,144)),('mipmap-xxxhdpi',(192,192))]
        for name,size in folder_names:
            folder = os.path.join(android_path, name)
            os.mkdir(folder)
            image_creator(img, size, folder)
    if ios_path:
        sizes = [(29,29),(40,40),(57,57),(58,58),(60,60),(80,80),(87,87),(114,114),(120,120),\
            (180,180),(1024,1024)]
        for size in sizes:
            image_creator(img, size, ios_path, str(size[0])+'.png')
if __name__=='__main__':
    sys.exit(main())


##End of the Script