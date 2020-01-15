import matplotlib.pyplot as plt
import pandas as pd
import sys


def read_file(path):
    df = pd.read_csv(path, header=None, sep=' ')  # 第一列=0.2，选2、3
    return df


def relation_plot(df, path):
    df = df[df.iloc[:, 0] == 0.2][:200]
    col_1 = df[df.columns[2]]
    col_2 = df[df.columns[3]]
    plt.xlabel('x')
    plt.ylabel('u')
    _ = plt.plot(col_1, col_2)
    plt.title("Burgers Equation:\nrelation between x and u with v=0.2")
    save_path = path + "relation_burg.png"
    print(save_path)
    plt.savefig(save_path)


# ----------------------------------------------------------
#                   Burgers折线图
# 函数功能：读入burgers方程的txt数据，画出折线图
# 参数(1个)：1.path: txt数据路径，str类型
# ----------------------------------------------------------
def execute(path, name):
    file_path = path + name
    print("file_path", file_path)
    df = read_file(file_path)
    relation_plot(df, path)


def main():
    # 获取文件路径和文件名参数
    pyArgs = []
    pyArgs.append(sys.argv[1])
    pyArgs.append(sys.argv[2])

    print("pyArgs 0:", pyArgs[0])
    print("pyArgs 1:", pyArgs[1])
    execute(pyArgs[0], pyArgs[1])


if __name__ == '__main__':
    main()
