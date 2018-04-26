
list1 = [{'mm':90},{'mm':90},{'mm':90},{'mm':90},{'mm':90}]


while len(list1) != 0:
    l = 0
    a = list1.pop()
    # print(a)
    # print(list1)
    if len(list1) == 0:
        print('%d是最大的' % a['mm'])
        break
    for i in list1:
        l += 1
        if i['mm']>a['mm']:
            # print('%d不是最大的' % a['mm'])
            break
        if l == len(list1):
            print('%d是最大的' % a['mm'])
            list1.clear()



# K = 0
# for i in list1:
#     changdu = len(list1) + 1
#     K += 1
#     v = 0
#     for j in list1[K:changdu]:
#         if i['mm']<= j['mm']:
#             print('%d不是最大' % i['mm'])
#             v += 1
#             continue
#
#         if
#         print('最大的是%d' % i['mm'])



