# coding:utf-8

# -----------------------------------------------------------------------------
# 小工具，基于源图片，生成指定尺寸的图片, 直接覆盖源图片

# 运行方式：

# python resize_pic.py file_name (width, height)
# 若 width 或 height 其中之一为0， 则自动按原图像比例进行缩放
# -----------------------------------------------------------------------------

from optparse import OptionParser
from PIL import Image
import os


def get_all_files(folder_name, exts=None):
    """
    获得某目录下，指定扩展名的所有文件列表
        inputs：
            folder_name : 目录名
            exts        : 扩展名列表 ['.jpg','.png'], 若为None，则不考虑扩展名的限制。缺省为 None
        outputs:
            files 列表， 包含所有满足条件的全称文件名

        Samples:
            files = get_all_files('c:\\users\\edwin\\')
    """
    files = []

    def get_one_folder(source_dir):
        sub_files = [x for x in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, x))]
        for f in sub_files:
            full_name = os.path.join(source_dir, f)
            ext_name = os.path.splitext(f)[1]

            if exts is None or ext_name in exts:
                files.append(full_name)

        sub_dirs = [y for y in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, y))]
        for sub in sub_dirs:
            sub_folder_name = os.path.join(source_dir, sub)
            get_one_folder(sub_folder_name)

    get_one_folder(folder_name)

    return files


def resize_picture(file_name, size, keep_ratio):
    size = eval(size)
    width = int(size[0])
    height = int(size[1])
    keep_ratio = int(keep_ratio)

    fname, fext = os.path.splitext(file_name)

    if not os.path.exists(file_name):
        print("Input file is not exists !")
        return

    if fext not in (['.jpg', '.png', '.bmp']):
        print('Input file is not a picture file !')
        return

    if width <= 0 and height <= 0:
        print('Input picture resize is not valid !')
        return

    img = Image.open(file_name)
    img_width = img.width
    img_height = img.height

    # 若width, height 有一个为0， 则不为0的固定，调整设置为0的尺寸
    if width <= 0 < height:
        width = int((img_width / img_height) * height)
    elif height <= 0 < width:
        height = int((img_height / img_width) * width)
    else:
        if keep_ratio == 1:
            if 0 <= img_width < img_height:
                width = int((img_width / img_height) * height)
            elif 0 <= img_height < img_width:
                height = int((img_height / img_width) * width)

    img_sized = img.resize((width, height))
    img_sized.save(file_name)


def batch_resize(size, keep_ratio):
    """
        size = (width, height), (width, 0), (0, height)
    """
    files = get_all_files(".", exts=['.jpg',' .png'])
    for fname in files:
        print(fname)
        resize_picture(fname, size, keep_ratio)


parser = OptionParser()

parser.add_option("-s", "--size", dest="size", help="target_size = (width, height)")
parser.add_option("-k", "--keep", dest="keep_ratio", help="keep ratio (1) or not (0)", default="1")

(options, args) = parser.parse_args()

batch_resize(options.size, options.keep_ratio)


# if __name__ == "__main__":
#     size = sys.argv[1]         # (width, height)
#     keep_ratio = sys.argv[2]   # 1 - keep ratio,  2 = (width, height)
#     batch_resize(size, keep_ratio)



