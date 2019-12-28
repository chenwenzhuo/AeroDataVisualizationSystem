import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pandas as pd
import sys
import cv2


# 读取数据文件
def read_file(path):
    df = pd.read_csv(path, header=None, sep='\t')
    return df


def heat_map(df, col1, col2, col3):
    print("heat map 1")
    df = df[:4225]
    col1 = df[df.columns[col1]]
    col2 = df[df.columns[col2]]
    col3 = df[df.columns[col3]]

    col3 = np.floor((col3 - col3.mean()) / (col3.max() - col3.min()) * 255) - 1
    col1 = np.floor((col1 - col1.mean()) / (col1.max() - col1.min()) * 65) - 1
    col2 = np.floor((col2 - col2.mean()) / (col2.max() - col2.min()) * 65) - 1
    image = np.zeros((65, 65), dtype=float)
    for n in range(len(col1.index)):
        image[int(col1[n]), int(col2[n])] = col3[n]
    save_path = "./src/main/resources/static/images/heat_map.png"
    print("heat map 2")

    # cv2.imwrite(save_path, image)
    # plt.savefig(save_path)
    matplotlib.image.imsave(save_path, image)
    print("heat map 3")

    # plt.imshow(image)
    # plt.show()


if __name__ == '__main__':
    pyArgs = []
    # for i in range(1, len(sys.argv)):
    #     pyArgs.append(int(sys.argv[i]))
    pyArgs.append(sys.argv[1])
    pyArgs.append(int(sys.argv[2]))
    pyArgs.append(int(sys.argv[3]))
    pyArgs.append(int(sys.argv[4]))

    df = read_file(pyArgs[0])
    heat_map(df, pyArgs[1], pyArgs[2], pyArgs[3])

    print(pyArgs[1] + pyArgs[2] + pyArgs[3])
