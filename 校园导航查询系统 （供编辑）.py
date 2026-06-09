# ==========================================
# 校园导航查询系统 V4.0（二叉树优化版）
# 数据结构：
# List + Dictionary + BST
#
# 算法：
# KMP
# BM
# BST
# ==========================================

campus_places = [
    {"id": 1, "name": "弘义楼", "location": "教学楼"},
    {"id": 2, "name": "致远楼", "location": "教学楼"},
    {"id": 3, "name": "明德楼", "location": "教学楼"},
    {"id": 4, "name": "明理楼", "location": "教学楼"},
    {"id": 5, "name": "明志楼", "location": "教学楼"},
    {"id": 6, "name": "明善楼", "location": "教学楼"},
    {"id": 7, "name": "图书馆", "location": "校内图书阅览中心"},
    {"id": 8, "name": "筑梦活动中心", "location": "校内活动场所"},
    {"id": 9, "name": "旭日餐厅", "location": "校内食堂"},
    {"id": 10, "name": "体育场", "location": "校内运动场地"},
    {"id": 11, "name": "看台", "location": "体育场附属设施"},
    {"id": 12, "name": "1A宿舍楼", "location": "学生宿舍"},
    {"id": 13, "name": "1B宿舍楼", "location": "学生宿舍"},
    {"id": 14, "name": "2A宿舍楼", "location": "学生宿舍"},
    {"id": 15, "name": "2B宿舍楼", "location": "学生宿舍"},
    {"id": 16, "name": "3A宿舍楼", "location": "学生宿舍"},
    {"id": 17, "name": "3B宿舍楼", "location": "学生宿舍"},
]

# ==========================================
# KMP算法
# ==========================================

def get_next(pattern):

    nxt = [0] * len(pattern)

    j = 0

    for i in range(1, len(pattern)):

        while j > 0 and pattern[i] != pattern[j]:
            j = nxt[j - 1]

        if pattern[i] == pattern[j]:
            j += 1

        nxt[i] = j

    return nxt


def kmp(text, pattern):

    if pattern == "":
        return True

    nxt = get_next(pattern)

    j = 0

    for i in range(len(text)):

        while j > 0 and text[i] != pattern[j]:
            j = nxt[j - 1]

        if text[i] == pattern[j]:
            j += 1

        if j == len(pattern):
            return True

    return False


############################################
# BM算法
############################################

def build_bad(pattern):

    bad = {}

    for i in range(len(pattern)):
        bad[pattern[i]] = i

    return bad


def BM(text, pattern):

    n = len(text)
    m = len(pattern)

    if m == 0:
        return True

    bad = build_bad(pattern)

    s = 0

    while s <= n - m:

        j = m - 1

        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            return True

        else:

            c = text[s + j]

            s += max(1, j - bad.get(c, -1))

    return False


############################################
# 查看所有地点
############################################

def show_all_places():

    print("\n=====全部地点=====")

    for p in campus_places:
        print(
            f"[{p['id']}] "
            f"{p['name']} - "
            f"{p['location']}"
        )

    print("地点总数:", len(campus_places))


############################################
# KMP名称查询
############################################

def search_by_name():

    key = input("输入地点名称:")

    found = False

    for p in campus_places:

        if KMP(p["name"], key):

            print(
                f"\n编号:{p['id']}"
            )

            print(
                f"名称:{p['name']}"
            )

            print(
                f"位置:{p['location']}"
            )

            found = True

    if not found:
        print("未找到")


############################################
# BM模糊查询
############################################

def fuzzy_search():

    key = input("输入关键字:")

    result = []

    for p in campus_places:

        text = (
            p["name"] +
            p["location"]
        )

        if BM(text, key):

            result.append(p)

    print("\n=====查询结果=====")

    if len(result):

        for p in result:

            print(
                f"[{p['id']}] "
                f"{p['name']} - "
                f"{p['location']}"
            )

        print(
            f"\n找到{len(result)}个地点"
        )

    else:
        print("未找到")


############################################
# 分类查询（保留V2）
############################################

def search_by_category():

    category=input(
        "输入类别:"
    )

    count=0

    for p in campus_places:

        if category in p["location"]:

            print(
                f"[{p['id']}]"
                f"{p['name']}"
            )

            count+=1

    print(
        f"共{count}个"
    )


############################################
# 添加
############################################

def add_place():

    id=int(
        input("编号:")
    )

    name=input(
        "名称:"
    )

    loc=input(
        "位置:"
    )

    campus_places.append(
        {
            "id":id,
            "name":name,
            "location":loc
        }
    )

    print("添加成功")


############################################
# 删除
############################################

def delete_place():

    id=int(
        input("输入编号:")
    )

    for p in campus_places:

        if p["id"]==id:

            campus_places.remove(p)

            print("删除成功")

            return

    print("未找到")


############################################
# 修改
############################################

def modify_place():

    id=int(
        input("输入编号:")
    )

    for p in campus_places:

        if p["id"]==id:

            p["name"]=input(
                "新名称:"
            )

            p["location"]=input(
                "新位置:"
            )

            print("修改成功")

            return

    print("未找到")


############################################
# 排序
############################################

def sort_places():

    campus_places.sort(
        key=lambda x:x["name"]
    )

    print("排序完成")


############################################
# 统计（保留V2）
############################################

def statistics():

    print(
        "\n地点总数:",
        len(campus_places)
    )


############################################
# 菜单
############################################

def show_menu():

    print("\n======V3.0======")

    print("1 查看地点")

    print("2 KMP名称查询")

    print("3 BM模糊查询")

    print("4 分类查询")

    print("5 添加地点")

    print("6 删除地点")

    print("7 修改地点")

    print("8 名称排序")

    print("9 地点统计")

    print("0 退出")


############################################
# 主函数
############################################

def main():

    while True:

        show_menu()

        choice=input(
            "输入:"
        )

        if choice=="1":
            show_all_places()

        elif choice=="2":
            search_by_name()

        elif choice=="3":
            fuzzy_search()

        elif choice=="4":
            search_by_category()

        elif choice=="5":
            add_place()

        elif choice=="6":
            delete_place()

        elif choice=="7":
            modify_place()

        elif choice=="8":
            sort_places()

        elif choice=="9":
            statistics()

        elif choice=="0":

            print(
                "系统退出"
            )

            break

        else:
            print(
                "输入错误"
            )


if __name__=="__main__":

    main()
