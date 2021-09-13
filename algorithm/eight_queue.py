# 检测皇后之间的位置关系
def conflict(queen_str, current_queen):
    """
    :param queen_str: str-->指代当前皇后存放之前的所有皇后的集合
    :param current_queen: int-->指代当前皇后想要存放的位置
    :return:Flag: boolean-->指代当前位置的皇后是否与之前所有位置的皇后有冲突
    """
    # 此处的queen_length既是之前保存的queen_list集合的长度，也可以理解为当前current_queen皇后的行下标
    queen_length = len(queen_str)
    # 定义是否有位置冲突的标签
    Flag = False
    for index in range(queen_length):
        # queen_length - index主要是控制相邻两行的皇后不能处于对角线上，其他的就没要求
        if abs(current_queen-int(queen_str[index])) in(0, queen_length-index):
            Flag = True
            break
    return Flag


# 定义执行皇后问题的主函数
def queens(nums=8, queen_str=""):
    """
    :param nums: int-->指代整个棋盘中想要存放皇后的个数
    :param queen_str: str-->指代当前皇后存放之前的所有皇后的集合
    :return:final_queens: List[int]-->指代最后符合要求的皇后的位置
    """
    final_queens = []

    # 定义递归函数，获取所有八皇后的值
    def back(queen_str):
        # 出口条件
        if len(queen_str) == nums:
            final_queens.append(queen_str)
            return
        for index in range(nums):
            Flag = conflict(queen_str, index)
            # 如果当前位置的皇后是否与之前所有位置的皇后没有冲突，则执行下述代码
            if Flag is False:
                back(queen_str+str(index))

    back(queen_str)
    return final_queens


if __name__ == "__main__":
    final_queens = queens()
    print(final_queens)
    print(len(final_queens))