import matplotlib.pyplot as plt
import pandas as pd
import sys


def read_file(path):
    df = pd.read_csv(path)  # 第一列=0.2，选2、3
    df = df.drop('Global_Index', 1)
    return df


def relation_plot(df, path, c1, c2):
    col_1 = df[df.columns[c1]]
    col_2 = df[df.columns[c2]]
    coo_1 = df.columns[c1]
    coo_2 = df.columns[c2]
    plt.xlabel(coo_1)
    plt.ylabel(coo_2)
    _ = plt.plot(col_1, col_2)
    plt.title("NS Equation:\nrelation between %s and %s" % (coo_1, coo_2))
    save_path = path + "relation_ns_csv.png"
    print(save_path)
    plt.savefig(save_path)


# ----------------------------------------------------------
#                   NS的flow_surface.csv文件的折线图
# 函数功能：NS的flow_surface.csv文件数据，画出折线图
# 参数(3个)：1.path: txt数据路径，str类型
#           2.col_1: 横轴
#           3.col_2: 纵轴
# ----------------------------------------------------------
def execute(path, name, col_1, col_2):
    file_path = path + name
    df = read_file(file_path)
    relation_plot(df, path, col_1, col_2)


def main():
    pyArgs = []
    pyArgs.append(sys.argv[1])
    pyArgs.append(sys.argv[2])
    pyArgs.append(int(sys.argv[3]))
    pyArgs.append(int(sys.argv[4]))

    execute(pyArgs[0], pyArgs[1], pyArgs[2], pyArgs[3])


if __name__ == '__main__':
    main()
