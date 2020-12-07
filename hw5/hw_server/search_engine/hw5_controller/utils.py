def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def parse_mesh_func():
    mesh = open('../c2020.bin')

    # read covid-19 related NM
    f = open('../mesh_nm')
    _covid_term = f.readlines()
    # remove newline
    covid_term = []
    for i in range(len(_covid_term) - 1):
        covid_term.append(_covid_term[i][:-1])

    covid_term.append(_covid_term[len(_covid_term) - 1])

    # deal with the first line
    line = mesh.readline()

    # word : [Synonyms]
    index = {}

    # Synonym : word
    inverted_index = {}

    _index = ''
    while line:
        line = mesh.readline()
        if line == '*NEWRECORD\n':
            _index = ''
        elif line[:2] == 'NM' and line[:5] != 'NM_TH':
            # print(line, end='')
            _index = line[5:-1]
            #         print(_index)

            # create a synonyms index
            index[_index] = []

        elif line[:2] == 'SY':
            # print(line, end='')

            # append to synonyms index
            index[_index].append(line[5:].split('|')[0])
            # create a inverted index
            inverted_index[line[5:].split('|')[0]] = _index

    # return index, inverted_index

    # filter out words without covid19
    # filter out words without covid19
    filt_index = {}
    for i in index.keys():
        if i in covid_term:
            filt_index[i] = index[i]

    filt_inv_index = {}
    for i in filt_index.keys():
        for j in filt_index[i]:
            filt_inv_index[j] = i

    return filt_index, filt_inv_index