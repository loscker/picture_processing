import os
from PIL import Image, ImageDraw
import cv2

output_folder = r"C:\Users\wxx\Desktop\picture_processing"
input_folder = r"C:\Users\wxx\Desktop\picture_processing\input_image"


def process_images_comprehensive(input_folder, output_folder, target_size=(300, 300)):
    """
    综合使用Pillow和OpenCV处理图像

    Args:
        input_folder (str): 输入图像文件夹路径
        output_folder (str): 输出图像文件夹路径
        target_size (tuple): 目标尺寸 (width, height)
    """
    # 创建不同的输出子文件夹
    # os.path.join 函数是用于生成路径的函数,它会将参数依据系统拼接成对应的路径
    pillow_output = os.path.join(output_folder, "pillow_results")
    opencv_output = os.path.join(output_folder, "opencv_results")

    for folder in [pillow_output, opencv_output]:
        if not os.path.exists(folder):  # 检查路径是否存在
            os.makedirs(folder)  # 若不存在，则创建对应的文件夹

    # 获取所有图像文件
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    #下面是一个列表推导式，第一个f代表要把什么放入列表中，相当于未知数x，后面接一个遍历循环，最后是一个判断条件，符合要求的f放入列表中
    image_files = [f for f in os.listdir(input_folder)  #os.listdir会返回一个包含目标文件夹内所有条目名称的一个列表
                   if f.lower().endswith(image_extensions)]     #f.lower是将文件名转换为小写，endwith是检查其是否以元组内的扩展名结尾
    #接下来对每一个文件进行处理
    for image_file in image_files:
        #首先获取每个输入文件的路径
        input_path = os.path.join(input_folder, image_file)

        # 使用Pillow处理
        try:
            #image.open函数用于打开一个图像文件并创建一个image对象
            with Image.open(input_path) as img:
                # 缩放，resize用于按照指定的尺寸进行重采样并改变图像的分辨率，参数1为包含长宽尺寸的元组，参数二为使用的重采样算法，为可选项，这里使用的为默认算法
                resized_img = img.resize(target_size, Image.Resampling.LANCZOS)

                # 绘制矩形
                #ImageDraw.Draw用于创建一个绘图对象，由此可以对其使用一系列方法进行绘制
                draw = ImageDraw.Draw(resized_img)
                width, height = resized_img.size
                rect_coords = [width // 4, height // 4, 3 * width // 4, 3 * height // 4]
                draw.rectangle(rect_coords, outline="red", width=3)

                # 保存
                output_path = os.path.join(pillow_output, f"processed_{image_file}")
                resized_img.save(output_path)
        except Exception as e:
            print(f"Pillow处理 {image_file} 时出错: {str(e)}")

        # 使用OpenCV处理
        try:
            #读取图像
            img = cv2.imread(input_path)
            if img is not None:
                # 缩放
                resized_img = cv2.resize(img, target_size, interpolation=cv2.INTER_LANCZOS4)

                # 绘制矩形
                height, width = resized_img.shape[:2] #获取其高度和宽度，其shape属性是一个数组，按顺序为高度、宽度、通道数，这里是获取前两个数
                pt1 = (width // 4, height // 4)
                pt2 = (3 * width // 4, 3 * height // 4)
                cv2.rectangle(resized_img, pt1, pt2, (0, 0, 255), 3)

                # 保存
                output_path = os.path.join(opencv_output, f"processed_{image_file}")
                cv2.imwrite(output_path, resized_img)
        except Exception as e:
            print(f"OpenCV处理 {image_file} 时出错: {str(e)}")

    print("所有图像处理完成!")


# 使用示例
if __name__ == "__main__":
    input_dir = r"C:\Users\wxx\Desktop\picture_processing\input_image"  # 替换为你的输入文件夹路径
    output_dir =  r"C:\Users\wxx\Desktop\picture_processing\out_image"  # 替换为你的输出文件夹路径

    process_images_comprehensive(input_dir, output_dir, (800, 400))
