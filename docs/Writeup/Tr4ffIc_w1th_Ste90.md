# Tr4ffIc_w1th_Ste90

题目附件加压得到

![image-20241207172327812](assets/image-20241207172327812.png)

根据题目hint，开始流量分析，找小明丢失的视频

![image-20241207172434835](assets/image-20241207172434835.png)

搜video，找到视频的流量

追踪UDP流

![image-20241207172628545](assets/image-20241207172628545.png)

选择原始数据

![image-20241207172733696](assets/image-20241207172733696.png)

根据提示，视频的格式为obs的默认格式，也就是mkv

导出视频后我们可以得到压缩包的密码

![74c57ae4d4aabbdafa0348e5828920e](assets/74c57ae4d4aabbdafa0348e5828920e.png)

解压压缩包，里面有两个文件

![776d8637a6e25874e0a0dacb95094ff](assets/776d8637a6e25874e0a0dacb95094ff.png)

一个是加密后的图片，一个是加密算法

根据加密算法我们可以写一个解密脚本，同时根据脚本里的暗示我们可以知道seed在50-70之间，我们输出所有的照片

```python
import numpy as np
import cv2
import sys
import random


def decode(input_image, output_image_prefix, seed):
    np.random.seed(seed)
    encoded_image = cv2.imread(input_image)
    if encoded_image is None:
        print(f"Error: Unable to load image {input_image}")
        exit(1)
    encoded_array = np.asarray(encoded_image)

    row_num = encoded_array.shape[0]
    col_num = encoded_array.shape[1]

    original_row_indices = list(range(row_num))
    original_col_indices = list(range(col_num))
    np.random.shuffle(original_row_indices)
    np.random.shuffle(original_col_indices)

    reversed_row_order = np.argsort(original_row_indices)
    restored_array = encoded_array[reversed_row_order, :]

    reversed_col_order = np.argsort(original_col_indices)
    restored_array = restored_array[:, reversed_col_order]

    output_image = f"{output_image_prefix}_{seed}.png"
    cv2.imwrite(output_image, restored_array)
    print(f"Decoded image with seed {seed} saved as {output_image}")


def main():
    if len(sys.argv)!= 3:
        print('error! Please provide input image path and output image prefix as command-line arguments.')
        exit(1)
    input_image = sys.argv[1]
    output_image_prefix = sys.argv[2]
    for seed in range(50, 71):
        decode(input_image, output_image_prefix, seed)


if __name__ == '__main__':
    main()
    
```

![image-20241207173256605](assets/image-20241207173256605.png)

我们可以得到一个二维码

扫码得到

> I randomly found a word list to encrypt the flag. I only remember that Wikipedia said this word list is similar to the NATO phonetic alphabet.
>
> crumpled chairlift freedom chisel island dashboard crucial kickoff crucial chairlift drifter classroom highchair cranky clamshell edict drainage fallout clamshell chatter chairlift goldfish chopper eyetooth endow chairlift edict eyetooth deadbolt fallout egghead chisel eyetooth cranky crucial deadbolt chatter chisel egghead chisel crumpled eyetooth clamshell deadbolt chatter chopper eyetooth classroom chairlift fallout drainage klaxon

根据提示：only remember that Wikipedia said this word list is similar to the NATO phonetic alphabet.

我们找到一个叫**PGP**的单词表

![image-20241207173742526](assets/image-20241207173742526.png)

根据单词表我们将单词转换成HEX

```
44 30 67 33 78 47 43 7B 43 30 4E 39 72 41 37 55 4C 61 37 31 30 6E 35 5F 59 30 55 5F 48 61 56 33 5F 41 43 48 31 33 56 33 44 5F 37 48 31 35 5F 39 30 61 4C 7D
```

再转换成中文字符得到flag

![image-20241207173903877](assets/image-20241207173903877.png)
