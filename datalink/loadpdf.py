from datalink.model import *
import os,time

def cur_datetime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

def bulk_insert(session,datas):
    try:
        session.bulk_insert_mappings(MT_TJ_FILE_ACTIVE, datas)
        session.commit()
        print('%s 批量插入成功！' %cur_datetime())
    except Exception as e:
        session.rollback()
        print('%s 批量插入失败！错误代码：%s' %(cur_datetime(),e))   # Cannot insert duplicate key row
        for data in datas:
            try:
                session.bulk_insert_mappings(MT_TJ_FILE_ACTIVE, [data])
                session.commit()
            except Exception as e:
                session.rollback()
                print('单个插入失败！错误代码：%s' %e)
                print(data)

#初始化-查找文件
def fileiter(root_path):
    for root, dirs, files in os.walk(root_path):
        if files and not dirs:                      #必须是指定目录的下级目录
            for file in files:
                yield os.path.join(root,file),file

if __name__ =="__main__":
    engine = create_engine('mssql+pymssql://bsuser:admin2389@10.8.200.201:1433/tjxt', encoding='utf8', echo=False)
    session = sessionmaker(bind=engine)()

    root_path =r'E:\activefile\report'

    tmp = []
    count = 0
    for i, j in fileiter(root_path):
        if count == 500:
            bulk_insert(session,tmp)
            count = 0
            tmp =[]
        else:
            info ={}
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(i).st_mtime))
            tjbh = os.path.splitext(os.path.basename(i))[0]
            info['tjbh'] = tjbh
            info['dwbh'] = tjbh[0:5]
            info['ryear'] = dt[0:4]
            info['rmonth'] = dt[0:7]
            info['rday'] = dt[0:10]
            info['localfile'] = i
            info['ftpfile'] = i[21:]
            info['filename'] = j
            info['filetypename'] = '体检报告'
            info['filesize'] = round(os.path.getsize(i) / float(1024 * 1024), 2)
            info['filemtime'] = os.stat(i).st_mtime
            info['createtime'] = dt

            tmp.append(info)
            count = count+1

    if tmp:
        bulk_insert(session, tmp)
