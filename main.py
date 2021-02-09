import csv
print("개쩌는 강의 시간표 수립 도우미")
print(" Greatest lecture tImetable eSTablishing helper")
print("...shortly GIST")
print("made by 임혁준\n")
#----------------------------------------------
f = open('개설강좌정보.csv', 'r')
r = csv.reader(f)
data_dic = {};
for _line in r:
    if(_line[0]=="NO"):
        continue
    if(not _line[3] in data_dic):
        data_dic[_line[3]] = []
    data_dic[_line[3]].append({
        'opened': _line[1],
        'code': _line[2],
        'title': _line[3],
        'docter': _line[6].split('\n'),
        #'lect': _line[8].split('/')[0],
        #'exp': _line[8].split('/')[1],
        'credit': _line[8].split('/')[2],
        'room': _line[10],
        'capacity': _line[11],
        'language': _line[14]
    })
    data_dic[_line[3]][-1]['time'] = [];
    for _s in _line[9].split('\n'):
        if(_s==""): continue
        data_dic[_line[3]][-1]['time'].append({
                'day': _s.split(' ')[0],
                's_t': _s.split(' ')[1].split('~')[0],
                'e_t': _s.split(' ')[1].split('~')[1],
             })
#print(data_dic)
f.close()
print("###데이터를 성공적으로 불러왔습니다###\n")
#----------------------------------------------
lect_name = []
for _k in data_dic.keys():
    lect_name.append(_k)
#----------------------------------------------
inputC1 = True
inp_arr = []
gong_day = "없음"
while(inputC1):
    inputC1= False
    for i in range(0,len(lect_name) ):
        print("["+str(i) + "] "+ lect_name[i] + "            (분반 개수:" + str(len(lect_name[i])) + ")")
    print("\n###수강을 원하시는 강의의 번호를 적어주세요. (예: '1 3 4' 입력)")
    inputC = True

    while(inputC):
        inputC = False
        inp = input()
        inp_arr = inp.split(" ")
        for _i in inp_arr:
            if(not _i.isdecimal()):
                inputC = True
                print("숫자를 입력해주세요")
                break
    print("###공강을 최우선으로 맞추고 싶은 요일을 하나만 입력하세요. 해당 기능을 적용하지 않고 싶다면 요일 외의 아무거나 입력해주세요. (예: '금' 입력)")
    gong_day = "없음"
    inp = input()
    if(inp == '월'):
        gong_day = "월"
    if (inp == '화'):
        gong_day = '화'
    if (inp == '수'):
        gong_day = '수'
    if (inp == '목'):
        gong_day = '목'
    if (inp == '금'):
        gong_day = '금'
    print("###입력한 내용을 확인해주세요. 계속 진행을 원하신다면 'y'를, 다시 입력하고 싶다면 'n'을 입력해주세요\n")
    print("-수강을 원하는 강의")
    for i in inp_arr:
        print("["+str(i) + "] "+ lect_name[int(i)])
    print("-공강을 원하는 요일 : " + gong_day)
    inp = input()
    if(inp!='y'):
        inputC1 = True
#--------------------------------------------------

print("###조건에 맞는 시간표를 찾는 중입니다...")
result = {}
index_arr = []
def d(n,cond_score):
    if(n==len(inp_arr)):
        if(not cond_score in result.keys()):
            result[cond_score] = []
        result[cond_score].append(index_arr.copy())
        #print(index_arr)
        return
    sub = lect_name[int(inp_arr[n])]

    for i in range(0,len(data_dic[sub])):
        temp_dat = data_dic[sub][i]
        score = 0
        for times in temp_dat['time']:
            if(times['day'] == gong_day):
                score = score + 1
        cond = True
        for j in index_arr:
            for times in j['time']:
                for times2 in temp_dat['time']:
                    if(times['day'] != times2['day']):
                        continue
                    if(times['e_t']<=times2['s_t'] or times['s_t']>=times2['e_t']):
                        continue
                    cond = False
        if(cond):
            index_arr.append(temp_dat)
            d(n+1,cond_score + score)
            index_arr.pop()
d(0,0)
key_num = sorted(result.keys())
for i in key_num:
    for j in result[i]:
        credit = 0
        print("/-----------------------------")
        for k in j:
            str_r = "=" + k['title'] + "  (" + k['code'] + ")    ( "
            for h in k['docter']:
                str_r += h + " "
            str_r += ")"
            print(str_r)
            print("정원: " + k['capacity'])
            str_r = "시간 :"
            for h in k['time']:
                str_r += h['day'] + " " + h['s_t'] + "~" + h['e_t'] + "    "
            print(str_r)
            credit += int(k['credit'])
        print("\n총 학점:"+str(credit))
if(len(result)==0):
    print("###조건에 부합하는 시간표가 없습니다.")
else:
    print("###조건에 부합하는 시간표를 모두 출력하였습니다.")