'''
Файл должен иметь вид формата:
номер.число
номер.число
К примеру:
1.00000
2.00001
И т.д.
'''

def CutStr(stroka):
    cube = list()
    separator = line.find(".") 
    cube.append(line[0:separator])
    for i in range(separator + 1, len(line)): 
        if line[i] != '\n':
            if line[i] == 'x': cube.append(line[i])
            else: cube.append(int(line[i]))
    return cube

def Equals(old, new):
    cube1 = old
    cube2 = new
    different = 0
    number = str(cube1[0] + '-' + str(cube2[0]))
    res_cube = list()
    for i in range(1, 7):
        if cube1[i] != cube2[i]: different += 1
    if different == 1:
        res_cube.append(number)
        for i in range(1, 7):
            if cube1[i] != cube2[i]: res_cube.append('x')
            else: res_cube.append(cube1[i])
    if len(res_cube) != 0: file1.write(str(res_cube) + '\n')

source = list()
file1 = open("data.txt", "r")
for line in file1: source.append(CutStr(line))
file1.close()
file1 = open("out.txt", "w")
for i in range(0, len(source) - 1):
    for j in range (i + 1, len(source)):
        Equals(source[i], source[j])