import time
import math

def count_diffs(a, b):
    n_better = 0
    n_worse = 0
    length = len(a)
    for i in range(length):
        n_better += a[i] > b[i]
        n_worse += a[i] < b[i]
    return n_better, n_worse

def skyline_bnl(input_file):
    data = []
    with open(input_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            data.append(list(map(float, line.split())))

    skyline_index = [0]

    for i in range(1, len(data)):
        to_drop = []
        is_dominate = False

        for j in skyline_index:
            n_better, n_worse = count_diffs(data[i], data[j])

            if n_worse > 0 and n_better == 0:
                is_dominate = True
                break
            if n_better > 0 and n_worse == 0:
                to_drop.append(j)

        if is_dominate:
            continue

        skyline_index = list(set(skyline_index).difference(set(to_drop)))
        skyline_index.append(i)

    skyline_points = []
    for index in skyline_index:
        skyline_points.append(data[index])

    return skyline_index, skyline_points

def skyline_sfs(input_file):
    data = []
    with open(input_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            line_data = list(map(float, line.split()))
            entropy = 0
            for i in range(len(line_data)):
                entropy += math.log(line_data[i] + 1)
            data.append([line_data, entropy])
    data.sort(key=lambda item: item[1], reverse=True)

    sfsFile = open('data/sfs_pre.txt', 'w')
    for row in data:
        sfsFile.write(" ".join(map(str, row[:-1][0])) + "\n")
    sfsFile.close()

    return skyline_bnl('data/sfs_pre.txt')



txt = 'data_3'
file = 'data/' + txt + '.txt'

bnl_start_time = time.time()
bnl_skyline_index, bnl_skyline_points = skyline_bnl(file)
print(f'BNL: {time.time() - bnl_start_time:.3f} seconds')

result_file = open('result/bnl_' + txt + '.txt', 'w')
for row in bnl_skyline_points:
    result_file.write(" ".join(map(str, row[:])) + "\n")
result_file.close()

sfs_start_time = time.time()
sfs_skyline_index, sfs_skyline_points = skyline_sfs(file)
print(f'SFS: {time.time() - sfs_start_time:.3f} seconds')

result_file = open('result/sfs_' + txt + '.txt', 'w')
for row in sfs_skyline_points:
    result_file.write(" ".join(map(str, row[:])) + "\n")
result_file.close()