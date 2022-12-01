import io

values = []
i = 0

while True:
    number = 0
    values.append(0)
    try:
        number = int(input())
        stopping = False
    except Exception:
        values.append(0)
        i+=1
        if stopping:
            break
        stopping = True
        pass
    if number:
        values[i] += number

top_inx = values.sort(reverse=True)

print(values[0] + values[1] + values[2])
