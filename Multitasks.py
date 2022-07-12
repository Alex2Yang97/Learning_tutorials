import concurrent.futures
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import time
from urllib.request import urlopen

# https://python-parallel-programmning-cookbook.readthedocs.io/zh_CN/latest/chapter4/02_Using_the_concurrent.futures_Python_modules.html
number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def evaluate_item(x):
        # 计算总和，这里只是为了消耗时间
        result_item = count(x)
        # 打印输入和输出结果
        return result_item

def  count(number) :
        for i in range(0, 10000000):
                i=i+1
        return i * number

# ================================================================
# https://github.com/bfortuner/ml-study/blob/master/multitasking_python.ipynb
def multithreading(func, args, workers):
    begin_time = time.time()
    with ThreadPoolExecutor(max_workers=workers) as executor:
        res = executor.map(func, args, [begin_time for i in range(len(args))])
    return list(res)
        
def multiprocessing(func, args, workers):
    begin_time = time.time()
    with ProcessPoolExecutor(max_workers=workers) as executor:
        res = executor.map(func, args, [begin_time for i in range(len(args))])
    return list(res)

def download(url, base):
    start = time.time() - base
    try:
        resp = urlopen(url)
    except Exception as e:
        print ('ERROR: %s' % e)
    stop = time.time() - base
    return start,stop

N = 16
URL = 'http://scholar.princeton.edu/sites/default/files/oversize_pdf_test_0.pdf'
urls = [URL for i in range(N)]

if __name__ == "__main__":
        # 顺序执行
        start_time = time.time()
        for item in number_list:
                print(evaluate_item(item))
        print("Sequential execution in " + str(time.time() - start_time), "seconds")
        # 线程池执行
        start_time_1 = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(evaluate_item, item) for item in number_list]
                for future in concurrent.futures.as_completed(futures):
                        print(future.result())
        print ("Thread pool execution in " + str(time.time() - start_time_1), "seconds")
        # 进程池
        start_time_2 = time.time()
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
                futures = [executor.submit(evaluate_item, item) for item in number_list]
                for future in concurrent.futures.as_completed(futures):
                        print(future.result())
        print ("Process pool execution in " + str(time.time() - start_time_2), "seconds")

        # ================================================================
        res = multithreading(download, urls, 1)
        print(res)