from screeninfo import get_monitors
for m in get_monitors():
    res = str(m)
    print(res)

width = res[24:28]
height = res[37:41]
print(width,'x',height)
