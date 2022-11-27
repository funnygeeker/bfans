import json
import time

import matplotlib.pyplot as plt
import requests

mid = 122879  # 用户ID
length = 20  # 最大长度
cycle = 60  # 刷新周期（单位：秒）


def get_follower():
    """通过API获取敖厂长剩余粉丝数"""
    result = requests.get(url=f'https://api.bilibili.com/x/web-interface/card?mid={mid}').text
    result = json.loads(result)  # str 转 dict
    # result = json.dumps(result, ensure_ascii=False, indent=4)
    result = result['data']['follower']
    return result


def get_location():  # 修改并获取Y轴注解位置
    global location
    location = not location
    return int(location)


plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
fig = plt.figure()  # 定义画布
ax = fig.add_subplot(1, 1, 1)  # 添加网格

ax.set_xlabel('时间')  # X轴标签
ax.set_ylabel('粉丝数')  # Y轴标签
ax.set_title('Bilibili敖厂长实时粉丝数')  # 标题

ax.ticklabel_format(style='plain', axis='y')  # Y轴显示原始数据

plt.grid(True)  # 添加网格
plt.ion()  # 启用交互模式

# 初始化变量
line = None
location = 0
follower = get_follower()
x_coordinate = 0
x_points = []
y_points = []
start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
old_follower = follower
max_follower = 1
min_follower = 0

while True:
    x_coordinate += 1  # 表示当前X坐标
    old_follower = follower  # 将原来的粉丝数代入旧粉丝数，并更新新粉丝数
    follower = get_follower()  # 获取敖厂长粉丝数
    if follower >= max_follower:  # 如果当前的粉丝大于程序启动以来最大的粉丝数，
        max_follower = follower  # 更新最大粉丝数
    if follower <= min_follower or min_follower == 0:  # 如果当前的粉丝小于程序启动以来最小的粉丝数，
        min_follower = follower  # 更新最小粉丝数
    height = follower * 0.01  # 通过粉丝量调整图标最高值和最低值和实际值的距离

    print(f"""===【{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}】===
统计开始时间：{start_time}
当前粉丝数：{follower}
最高粉丝数：{max_follower}
最低粉丝数：{min_follower}
总共掉粉数：{max_follower - min_follower}
本次掉粉数：{old_follower - follower}
""")
    now_time = time.strftime('%H:%M\n(%S)', time.localtime(time.time()))  # 当前时间
    x_points.append(now_time)  # 增加X坐标
    y_points.append(follower)  # 增加Y坐标

    if len(x_points) >= length * 100:  # 如果超过长度则删除多余的部分
        del x_points[0]
    if len(y_points) >= length * 100:  # 如果超过长度则删除多余的部分
        del y_points[0]

    if line is None:
        line = ax.plot(x_points, y_points, '-g', marker='*')[0]

    line.set_xdata(x_points)  # 设置X点坐标
    line.set_ydata(y_points)  # 设置Y点坐标

    ax.set_xlim([x_coordinate - length - 1, x_coordinate + 1])  # 设置X坐标宽度
    ax.set_ylim([min_follower - height * 2, max_follower + height * 3])  # 设置Y坐标高度
    ax.annotate(follower, xy=(now_time, follower),
                xytext=(now_time, follower + height + get_location() * height))  # 标注当前粉丝数值
    ax.annotate(follower - old_follower, xy=(now_time, follower), xytext=(now_time, follower - height))  # 标注粉丝数增减情况
    plt.pause(cycle)  # 每cycle秒刷新一次
