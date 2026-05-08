# ==========================================
# 校园导航查询系统 V2.0（分类查询版）
# 新增功能：
# 1. 按类别查询
# 2. 模糊查询（关键字搜索）
# 3. 查询结果统计
# 4. 函数封装
# ==========================================


# 校园地点数据
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


# =========================
# 功能函数区域
# =========================

# 显示所有地点
def show_all_places():
    print("\n===== 校园全部地点 =====")

    for p in campus_places:
        print(f"[{p['id']}] {p['name']} - {p['location']}")

    print(f"\n当前共有 {len(campus_places)} 个地点。")


# 按名称精确查询
def search_by_name():
    name = input("请输入地点名称：")

    found = False

    for p in campus_places:
        if p["name"] == name:
            print("\n===== 查询结果 =====")
            print(f"编号：{p['id']}")
            print(f"名称：{p['name']}")
            print(f"位置说明：{p['location']}")
            found = True
            break

    if not found:
        print("未找到该地点。")


# 模糊查询（关键字搜索）
def fuzzy_search():
    keyword = input("请输入关键字：")

    result = []

    for p in campus_places:
        # 名称或地点说明中包含关键字
        if keyword in p["name"] or keyword in p["location"]:
            result.append(p)

    print("\n===== 模糊查询结果 =====")

    if len(result) > 0:
        for p in result:
            print(f"[{p['id']}] {p['name']} - {p['location']}")

        print(f"\n共找到 {len(result)} 个相关地点。")

    else:
        print("未找到相关地点。")


# 按类别查询
def search_by_category():
    print("\n===== 地点类别 =====")
    print("1 教学楼")
    print("2 学生宿舍")
    print("3 食堂")
    print("4 体育设施")
    print("5 图书馆")
    print("6 活动中心")

    choice = input("请选择类别：")

    category_map = {
        "1": "教学楼",
        "2": "学生宿舍",
        "3": "食堂",
        "4": "体育",
        "5": "图书馆",
        "6": "活动"
    }

    if choice not in category_map:
        print("输入无效。")
        return

    keyword = category_map[choice]

    print("\n===== 分类查询结果 =====")

    count = 0

    for p in campus_places:
        if keyword in p["location"] or keyword in p["name"]:
            print(f"[{p['id']}] {p['name']} - {p['location']}")
            count += 1

    print(f"\n共找到 {count} 个地点。")


# 查询统计
def statistics():
    total = len(campus_places)

    teaching = 0
    dormitory = 0
    sports = 0

    for p in campus_places:

        if "教学楼" in p["location"]:
            teaching += 1

        elif "宿舍" in p["location"]:
            dormitory += 1

        elif "体育" in p["location"]:
            sports += 1

    print("\n===== 校园地点统计 =====")
    print(f"地点总数：{total}")
    print(f"教学楼数量：{teaching}")
    print(f"宿舍楼数量：{dormitory}")
    print(f"体育设施数量：{sports}")


# 显示菜单
def show_menu():
    print("\n========== 校园导航查询系统 V2.0 ==========")
    print("1 查看所有地点")
    print("2 按名称精确查询")
    print("3 模糊查询")
    print("4 按类别查询")
    print("5 地点统计")
    print("0 退出系统")


# =========================
# 主函数
# =========================

def main():

    while True:

        show_menu()

        choice = input("请输入操作序号：")

        if choice == "1":
            show_all_places()

        elif choice == "2":
            search_by_name()

        elif choice == "3":
            fuzzy_search()

        elif choice == "4":
            search_by_category()

        elif choice == "5":
            statistics()

        elif choice == "0":
            print("系统已退出，欢迎下次使用。")
            break

        else:
            print("输入无效，请重新输入。")


# 程序入口
if __name__ == "__main__":
    main()