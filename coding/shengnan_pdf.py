import pandas as pd
import re



def handle_content(df):
    df_content = pd.DataFrame ({})
    factors = {}
    for i in range (len (df)):
        # factors['filepath'] = df.iloc[i]['filepath']
        # factors['filename'] = df.iloc[i]['filename']
        # factors['filetime'] = df.iloc[i]['filetime']
        with open ('D:\\辅助项目\\15爬虫项目\\9、胜男的数据分析\\年报TXT\\\\300024机器人：2013年年度报告.txt', 'r', encoding='utf8', errors='ignore') as f:
            first_factor = []
            second_factor = []
            content = f.readlines ()
            for j, line in enumerate (content):
                # print(i,line)
                # print (df.iloc[i]['firstindex'],df.iloc[i]['secondindex'], df.iloc[i]['thirdindex'])
                if j >= int (df.iloc[i]['firstindex']) and j < int (df.iloc[i]['secondindex']):
                    first_factor.append (re.sub('\d+.','',line.replace (' ', '')).replace('\r\n','').replace('\n',''))
                if j >= int (df.iloc[i]['secondindex']) and j < int (df.iloc[i]['thirdindex']):
                    second_factor.append (line.replace (' ', ''))
            # print(first_factor)
            for mm in first_factor:
                a = ''.join(mm)
                print(a)
            first_factors = ' '.join (sentence for sentence in first_factor)
            second_factors = ' '.join (sentence for sentence in second_factor)
            factors['firstfactor'] = first_factors

            factors['secondfactor'] = second_factors
            factors['firstsentence'] = len (re.findall ('。', first_factors)) + len (re.findall (';', first_factors)) + len (re.findall ('；', first_factors))
            factors['secondsentence'] = len (re.findall ('。', second_factors)) + len (re.findall (';', second_factors)) + len (re.findall ('；', second_factors))
            print(i,factors['firstfactor'],len(factors['firstfactor']))
            # print(i,factors['firstfactor'])
        # print(i,factors['firstsentence'],factors['secondsentence'],factors['filename'])
        df_content = df_content.append (factors, ignore_index=True)
        df_content.to_csv (r'data\test2.csv', encoding='gbk')


factors = {}
df = pd.DataFrame ({})
with open ('D:\\辅助项目\\15爬虫项目\\9、胜男的数据分析\\年报TXT\\\\300020银江股份：2013年年度报告.txt', 'r', encoding='utf8',
           errors='ignore') as f:
    content = f.readlines ()
    for i, line in enumerate (content):
        # print(line)

        if '第四节董事会报告' in line.replace (' ', '') and len (line.replace (' ', '')) < 10:
            factors['firstindex'] = int (i)
            print (int (i))

        if '二、公司未来发展的展望' in line.replace (' ', '') and len (line.replace (' ', '')) < 13:
            # print('m',m)
            # print(i,line.replace(' ',''),one)
            factors['secondindex'] = int (i)

        if '公司未来发展的展望' in line.replace (' ', '') and len (line.replace (' ', '')) < 30:
            # print('m',m)
            # print(i,line.replace(' ',''),one)
            factors['secondindex'] = int (i)

        if '三、公司未来发展的展望' in line.replace (' ', '') and len (line.replace (' ', '')) < 13:
            # print('m',m)
            # print(i,line.replace(' ',''),one)
            factors['secondindex'] = int (i)

        if '三、董事会、监事会对会计师事务所本报告期“非标准审计报告”的说明' in line.replace (' ', ''):
            # print('存在')
            factors['thirdindex'] = int (i)
        if '三、公司利润分配及分红派息情况' in line.replace (' ', ''):
            # print('存在')
            factors['thirdindex'] = int (i)
        if '三、董事会关于报告期会计政策、会计估计变更或重要前期差错更正的说明' in line.replace (' ', ''):
            # print('存在')
            factors['thirdindex'] = int (i)
        if '三、董事会对会计师事务所本报告期“非标准审计报告”的说明' in line.replace (' ', ''):
            # print('存在')
            factors['thirdindex'] = int (i)
        if '三、报告期财务会计报告审计情况及会计政策、会计估计变更以及会计差错更正的说明' in line.replace (' ', ''):
            # print('存在')
            factors['thirdindex'] = int (i)

        if '四、董事会、监事会对会计师事务所本报告期“非标准审计报告”的说明' in line.replace (' ', ''):
            # print('存在')
            factors['thirdindex'] = int (i)
        if '四、公司利润分配及分红派息情况' in line.replace (' ', ''):
            # print('存在')
            factors['thirdindex'] = int (i)
        if '四、董事会关于报告期会计政策、会计估计变更或重要前期差错更正的说明' in line.replace (' ', ''):
            # print('存在')
            factors['thirdindex'] = int (i)
        if '四、董事会对会计师事务所本报告期“非标准审计报告”的说明' in line.replace (' ', ''):
            # print('存在')
            factors['thirdindex'] = int (i)
        if '四、报告期财务会计报告审计情况及会计政策、会计估计变更以及会计差错更正的说明' in line.replace (' ', ''):
            # print('存在')
            factors['thirdindex'] = int (i)

    print (factors)
    df = df.append (factors, ignore_index=True)
    handle_content (df)