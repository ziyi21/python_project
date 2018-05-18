import pandas as pd


factors = {}
df = pd.DataFrame ({})
with open ('D:\\辅助项目\\15爬虫项目\\9、胜男的数据分析\\年报TXT\\\\300078中瑞思创：2013年年度报告.txt', 'r', encoding='utf8', errors='ignore') as f:
    content = f.readlines ()
    for i, line in enumerate (content):
        # print(line)

        if '第四节董事会报告' in line.replace (' ', '') and len (line.replace (' ', '')) < 10:

            factors['firstindex'] = int (i)

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