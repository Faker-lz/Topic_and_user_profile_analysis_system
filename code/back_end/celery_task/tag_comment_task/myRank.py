def LeaderRank(LR_dic, undirected, degree_dic, temp_account):
    temp_number = 0
    for i in temp_account:
        for j in undirected[i]:
            temp_number += LR_dic[j] / degree_dic[j]
        LR_dic[i] = temp_number
        temp_number = 0
    return LR_dic


def proTask(database_dict, redatabase_dict, account):
    ground_node = "G"
    degree_dic = dict()
    undirected = dict()
    temp_account_list = []
    for i in account:
        if i in database_dict.keys():
            for j in database_dict[i]:
                temp_account_list.append(j)

        if i in redatabase_dict.keys():
            for j in redatabase_dict[i]:
                temp_account_list.append(j)

        temp = list(set(tuple(temp_account_list)))
        temp.append(ground_node)
        undirected[i] = temp
        degree_dic[i] = len(temp)
        temp_account_list = []

    degree_dic[ground_node] = len(account)

    undirected[ground_node] = account

    temp_account = account[:]

    temp_account.append(ground_node)

    LR_dic = dict()
    # 节点赋值
    for i in account:
        LR_dic[i] = 1

    LR_dic[ground_node] = 0

    return LR_dic, undirected, degree_dic, temp_account


def startRank(database_dict, redatabase_dict, account):
    LR_dic, undirected, degree_dic, temp_account = proTask(database_dict, redatabase_dict, account)
    temp = LR_dic
    for i in range(100):

        temp1 = list(temp.values())

        temp = LeaderRank(temp, undirected, degree_dic, temp_account)

        counter = 0

        temp2 = list(temp.values())

        for i in range(len(temp1)):
            try:

                if 0.9 <= temp1[i] / temp2[i] <= 1.1:
                    counter += 1
            except:
                pass
        if counter == len(temp1):
            break
    # print(sorted(list(temp.values()), reverse=True))
    return sorted(temp.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)[0:10]
    #
    # f = open(r'LR', 'w')
    # f.write(str(temp))
    # f.close()

if __name__=='__main__':
    pass









