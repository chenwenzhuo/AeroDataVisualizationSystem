import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class ColError(ValueError):
    pass


# 读取数据文件
def read_file(path):
    df = pd.read_csv(path, header=None, sep='\t')
    return df


def relation_plot(df, c1, c2):
    col_1 = df[df.columns[c1]]
    col_2 = df[df.columns[c2]]
    _ = plt.plot(col_1, col_2)
    save_path = "/Users/wuqiuyu/Desktop/relation_visualization.png"
    print(save_path)
    plt.savefig(save_path)
    plt.show()


# 流场图，还存在问题
# https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/plot_streamplot.html
def stream_plot(df):
    col1 = df[df.columns[0]][:4228]
    col2 = df[df.columns[1]][:4228]

    min_1 = np.floor(col1.min()) - 1
    max_1 = np.floor(col1.max())
    min_2 = np.floor(col2.min()) - 1
    max_2 = np.floor(col2.max())

    length = len(col1.index)
    lengthj = complex(len(col1.index))

    Y, X = np.mgrid[min_1:max_1:lengthj, min_2:max_2:lengthj]

    col1 = col1.values.reshape(length, 1)
    U_1 = np.tile(col1, length)

    col2 = col2.values.reshape(length, 1)
    V_1 = np.tile(col2, length)

    plt.streamplot(X, Y, U_1, V_1, density=[0.5, 1])
    save_path = "/Users/wuqiuyu/Desktop/stream_visualization.png"
    plt.savefig(save_path)
    plt.show()


def quiver_plot(df):
    col1 = df[df.columns[0]][:100]
    col2 = df[df.columns[1]][:100]

    min_1 = np.floor(col1.min()) - 1
    max_1 = np.floor(col1.max())
    min_2 = np.floor(col2.min()) - 1
    max_2 = np.floor(col2.max())
    length = len(col1.index)

    X = np.arange(min_1, max_1, 0.02)
    Y = np.arange(min_2, max_2, 0.02)

    col1 = col1.values.reshape(length, 1)
    col2 = col2.values.reshape(length, 1)

    plt.quiver(X, Y, col1, col2, scale=0.4, width=0.005)
    save_path = "/Users/wuqiuyu/Desktop/quiver_visualization.png"
    plt.savefig(save_path)
    plt.show()


def heat_map(df, c):
    df = df[:4225]
    col1 = df[df.columns[0]]
    col2 = df[df.columns[1]]
    col3 = df[df.columns[c]]
    col3 = np.floor((col3 - col3.mean()) / (col3.max() - col3.min()) * 255) - 1
    col1 = np.floor((col1 - col1.mean()) / (col1.max() - col1.min()) * 65) - 1
    col2 = np.floor((col2 - col2.mean()) / (col2.max() - col2.min()) * 65) - 1
    image = np.zeros((65, 65), dtype=float)
    for n in range(len(col1.index)):
        image[int(col1[n]), int(col2[n])] = col3[n]
    save_path = "/Users/wuqiuyu/Desktop/heat_visualization.png"
    matplotlib.image.imsave(save_path, image)
    plt.imshow(image)
    plt.show()


# 数据可视化
def visualize(df, col_1=0, col_2=1, col_3=5):
    columns_num = len(df.columns)

    if col_1 > columns_num:
        raise ColError('invalid value: %s' % col_1)
    if col_2 > columns_num:
        raise ColError('invalid value: %s' % col_2)
    if col_1 < 0 or col_2 < 0:
        raise ColError('invalid column')
    relation_plot(df, col_1, col_2)
    stream_plot(df)
    quiver_plot(df)
    heat_map(df, col_3)


def main():
    file_path = '/Users/wuqiuyu/Desktop/flow.dat'
    df = read_file(file_path)
    visualize(df, col_2=5)


if __name__ == '__main__':
    main()
