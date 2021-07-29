# 汉诺塔
def hanoi(n, a , b, c):
    if n > 0:
        hanoi(n-1, a, c, b)
        print("moving from %s to %s." % (a, c))
        hanoi(n-1, b, a, c)

li = list(range(10000000))

# 顺序查找
def Linear_search(li, val):
    for i,v in enumerate(li):
        if v==val:
            return i
    else:
        return None
print('linear_search:', Linear_search(li, 9))


# 二分查找
def binary_search(li, val):
    left = 0
    right = len(li) - 1
    while left <= right:
        mid = (left + right)//2
        if li[mid] < val:
            left = mid + 1
        elif li[mid] > val:
            right = mid - 1
        elif li[mid] == val:
            return mid
    else:
        return None
print('binary_search:', binary_search(li, 9))


li = [3, 2, 4, 6, 5, 9, 8, 7, 1]
# 冒泡排序
def bubble_sort(li):
    # 循环n-1次
    for i in range(len(li) - 1):
        # 放一个标记,防止有一次排好序,再循环
        chang_flag = False
        for j in range(len(li) - 1 - i):
        # 内层再循环把最大的放有序区的最前面
            if li[j] > li[j + 1]:
                li[j], li[j + 1] = li[j + 1], li[j]
                chang_flag = True
        if not chang_flag:
            return


bubble_sort(li)
print('bubble_sort:', li)


li = [3, 2, 4, 6, 5, 9, 8, 7, 1]
# 选择排序
def select_sort(li):
    # 循环n-1次,一个时不用再排序
    for i in range(len(li) - 1):
        # 记录要放的位置
        min_loc = i
        for j in range(i+1, len(li)):
            # 循环在要放的位置后面找出最小值
            if li[j] < li[min_loc]:
                # 找到时把最小值的位置记录下来
                min_loc = j
        if min_loc != i:
            # 如果找到最小值,把最小值和坑位值对调
            li[i], li[min_loc] = li[min_loc], li[i]


# 插入排序
def insert_sort(li):
    # 循环n-1次,从第二位开始
    for i in range(1, len(li)):
        # 拿到最新未排序的值
        tmp = li[i]
        # 获得排序的最后一位的位置
        j = i - 1
        # 从排好的最后一位往前找位置
        while j >= 0 and tmp < li[j]:
            # 找到最新牌的插入位置
            li[j + 1] = li[j]
            j = j - 1
        # 最新牌插入找到的位置
        li[j + 1] = tmp


# 快速排序
def partition(li, left, right):
    tmp = li[left]
    while left < right:
        while left < right and li[right] >= tmp: # 从右边找比tmp小的数
            right -= 1          # 往右走一步
        li[left] = li[right]    # 把右边的值写到左边空位上
        while left < right and li[left] <= tmp:
            left += 1
        li[right] = li[left]    # 把左边的值写到右边空位上
    li[left] = tmp              # 把tmp归位
    return left     # mid 是 这个函数返回left值的目的


# 快速排序-框架
def quick_sort(li, left, right):
    if left < right:    # 至少2个元素
        mid = partition(li, left, right)    # 这个函数返回left值的目的
        quick_sort(li, left, mid - 1)   # 左边部分
        quick_sort(li, mid + 1, right)  # 右边部分
