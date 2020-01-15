import matplotlib.pyplot as plt
import pandas as pd
import sys


# 读取数据文件
def read_file(path):
    print("py read_file: ", path)
    df = pd.read_table(path, header=None)  # 第一列=0.2，选2、3
    return df


def relation_plot(df, path, c1, c2):
    print("py relation_plot: ", path, c1, c2)
    df = df.drop([0, 1, 2])
    b = df.iloc[0].str.split(expand=True)
    df_out = b.iloc[0, :].str.rstrip(',').astype('float')
    df_out = df_out.to_frame()
    for i in range(1, len(df)):
        b = df.iloc[i].str.split(expand=True)
        d = b.iloc[0, :].str.rstrip(',').astype('float')
        d = d.to_frame()
        df_out = pd.concat([df_out, d], axis=1)
    df_out = df_out.T
    df_out.columns = ['Iteration',
                      'CL',
                      'CD',
                      'CSF',
                      'CMx',
                      'CMy',
                      'CMz',
                      'CFx',
                      'CFy',
                      'CFz',
                      'CL/CD',
                      'AoA',
                      'Custom_ObjFunc',
                      'HeatFlux_Total',
                      'HeatFlux_Maximum',
                      'Temperature_Total',
                      'Res_Flow[0]',
                      'Res_Flow[1]',
                      'Res_Flow[2]',
                      'Res_Flow[3]',
                      'Res_Flow[4]',
                      "Res_Turb[0]",
                      'Linear_Solver_Iterations',
                      'CFL_Number',
                      'Time(min)']

    col_1 = df_out.iloc[:, c1]
    col_2 = df_out.iloc[:, c2]
    plt.xlabel(df_out.columns[c1])
    plt.ylabel(df_out.columns[c2])
    plt.title("M6:\nRelation between %s and %s" % (df_out.columns[c1], df_out.columns[c2]))
    _ = plt.plot(col_1, col_2)
    save_path = path + "relation_m6_his_dat.png"  # ----------------此处需修改------------------

    print("py relation_plot, save_path", save_path)
    plt.savefig(save_path)
    print("end of py relation_plot")


# ----------------------------------------------------------
#                   M6的history.dat折线图
# 函数功能：读入M6方程的history.dat数据，画出折线图
# 参数(3个)：1.path: csv数据路径，str类型
#           2.col_1: 横轴
#           3.col_2: 纵轴
# ----------------------------------------------------------
def execute(path, name, col_1, col_2):
    print("py execute: ", path, name, col_1, col_2)
    file_path = path + name
    df = read_file(file_path)
    relation_plot(df, path, col_1, col_2)


def main():
    pyArgs = []
    pyArgs.append(sys.argv[1])
    pyArgs.append(sys.argv[2])
    pyArgs.append(int(sys.argv[3]))
    pyArgs.append(int(sys.argv[4]))

    print("py main: ", pyArgs)
    execute(pyArgs[0], pyArgs[1], pyArgs[2], pyArgs[3])


if __name__ == '__main__':
    main()
