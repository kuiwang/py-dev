# -*- coding:utf-8 -*-

'''
Created on 2019年8月26日

@author: user
'''
import os, sys, logging
from importlib import reload
import numpy as np

reload(sys)

PY_GEN_PATH = "D:/data/priv".replace('/', os.sep)
logger = logging.getLogger('np_dev')
LOG_FILE = 'np_dev.log'
# LOG_FORMATTER = '%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(threadName)s - %(process)d - %(name)s - %(levelname)s - %(message)s'
LOG_FORMATTER = '%(message)s'


def config_logger():
    logger.setLevel(logging.DEBUG)
    if not os.path.exists(PY_GEN_PATH):
        logger.info("文件夹不存在,已自行创建")
        os.makedirs(PY_GEN_PATH, 777)
    handler = logging.FileHandler(os.path.join(PY_GEN_PATH, LOG_FILE))
    handler.setLevel(logging.DEBUG)
    fmter = logging.Formatter(LOG_FORMATTER)
    handler.setFormatter(fmter)
    logger.addHandler(handler)

    # 控制台打印
    console = logging.StreamHandler()
    console.setLevel(level=logging.DEBUG)  # 设置为INFO级别
    console.setFormatter(fmter)
    logger.addHandler(console)


# ndarray:N维数组类型
def ndarray_operate():
    # 一个维度
    # output: [1 2 3]
    a = np.array([1, 2, 3])
    logger.info(a)
    
    # 多个维度的数组
    # output: 
    '''
    [[1 2 6]
     [3 4 5]]
    '''
    a = np.array([[1, 2, 6], [3, 4, 5]])
    logger.info(a)
    
    # minimum dimensions
    # output: [[[1 2 3 4 5]]]
    a = np.array([1, 2, 3, 4, 5], ndmin=3)
    logger.info(a)
    
    # dtype 参数
    # output: [1.+0.j 2.+0.j 3.+0.j]
    a = np.array([1, 2, 3], dtype=complex)
    logger.info(a)

# numpy数据类型

'''
        数据类型:
    bool_: 布尔；
    int_: 默认整数类型，与C Long相同，通常是int64或int32
    intc: 与C int相同，通常为int32 或 int64
    intp: 用于索引的整数，与C ssize_t相同，通常为int32 或 int64
    int8: 字节(-128～127)
    int16: 整数(-32768～32767)
    int32: 整数(-214748368～2147483647)
    int64: 整数(-9223372036854775808～9223372036854775807)
    uint8: 无符号整数(0～255)
    uint16: 无符号整数(0～65535)
    uint32: 无符号整数(0～4294967295)
    uint64: 无符号整数(0～18446744073709551615)
    float_: 同float64
    float16: 半精度浮点：符号位、5位指数、10位尾数
    float32: 单精度浮点：符号位、8位指数、23位尾数
    float64: 双精度浮点：符号位、1位指数、52位尾数
    complex_: 同complex128
    complex64: 复数，由2个32位浮点数（实部和虚部）
    complex128: 复数，由2个64位浮点数（实部和虚部）
'''


def np_datatype():
    dt = np.dtype(np.int32)
    logger.info(dt)
    
    # int8,int16,int32,int64可以使用i1,in2,i4,i8等代替
    dt = np.dtype('i1')
    logger.info(dt)
    dt = np.dtype('i2')
    logger.info(dt)
    dt = np.dtype('i4')
    logger.info(dt)
    dt = np.dtype('i8')
    logger.info(dt)
    
    # 字节顺序由前缀'<'或'>'到数据类型，
    # '<'意味着编码是小端(最小有效存储在最小地址中)
    # '>'意味着编码是big-endian(最重要的字节存储在最小地址中)
    dt = np.dtype('>i4')
    print(dt)
    
    # first created structured data type
    dt = np.dtype([('age', np.int8)])
    logger.info(dt)
    # 将数据类型使用到数组中
    a = np.array([(10,), (20,), (30,)], dtype=dt)
    logger.info(a)
    logger.info(a['age'])
    
    # 定义了一个student结构,字符串name、整数age、浮点mark
    student = np.dtype([('name', 'S20'), ('age', 'i1'), ('marks', 'f4')])
    logger.info(student)
    a = np.array([('Zhao', 23, 50.1), ('Qian', 20, 49.0)], dtype=student)
    logger.info(a)


# 数组属性
def array_attribute():
    # shape: 数组的行数和列数
    a = np.array([[1, 2, 3], [14, 240, 23]])
    shape = a.shape
    logger.info(a)
    logger.info(shape)
    
    # 调整数组的行和列，会影响数组元素的分布
    a.shape = (3, 2)
    logger.info(a)
    
    # reshape(): 调整数组大小
    a = np.array([[1, 2, 3], [4, 5, 6]])
    b = a.reshape(3, 2)
    logger.info(b)
    
    # ndim: 返回数组维数
    a = np.arange(24)
    logger.info(a)
    dim = a.ndim
    logger.info(dim)
    # 重新调整数组
    b = a.reshape(2, 4, 3)
    logger.info(b)
    dim = b.ndim
    logger.info(dim)
    
    # numpy.itemsize
    # 以字节为单位返回数组中每个元素的长度
    # 目前数据类型是int8
    x = np.array([1, 2, 3, 4, 5], dtype=np.int8)
    logger.info(x.itemsize)
    # 现在改为int64
    x = np.array([1, 2, 3, 4, 5], dtype=np.int64)
    logger.info(x.itemsize)
    
    # numpy.flags:
    '''
    C_CONTIGUOUS(C): 数据在一个单一的C风格的连续段
    F_CONTIGUOUS(F): 数据在一个单一的Fortran风格的连续段
    OWNDATA(O): 数组拥有它使用的内存或从另一个对象中借用内存
    WRITEABLE(W): 数据区可以写入，将其设置为False会锁定数据，使其成为只读
    ALIGNED(A): 数据和所有元素都针对硬件进行了适当的对齐
    UPDATEIFCOPY(U): 该数组是其他数组的副本，当这个数组被解除分配时，基数组被更新为这个数组的内容
    '''
    x = np.array([1, 2, 3, 4, 5])
    logger.info(x.flags)


# 生成数组函数
def gen_array():
    '''
    numpy.empty(shape,dtype=float,order='C'):
    order: C=>rowmajor ; F=>columnmajor
        创建一个空数组示例
    '''
    x = np.empty([3,2],dtype=int)
    logger.info(x)
    
    '''
    #numpy.zeros(shape,dtype=float,order='C'):
    #返回指定大小的新数组，填充0
    '''
    y = np.zeros(5)
    logger.info(y)
    y=np.zeros(5,dtype=int)
    logger.info(y)
    
    #customer type
    x = np.zeros((2,2),dtype=[('x','i4'),('y','i8')])
    logger.info(x)
    logger.info(x['x'])
    logger.info(x['y'])
    
    '''
    #numpy.ones(shape,dtype=None,order='C')::返回指定大小的新数组，填充1
    '''
    x = np.ones(5)
    logger.info(x)
    
    x = np.ones([2,4],dtype=int)
    logger.info(x)
    
    '''
    numpy.asarray(a,dtype=None,order=None):将python序列转换为ndarray时很有用
    a:以任何形式输入数据：如：列表、元组列表、元组元组
    '''
    x = [1,3,5,7,8]
    #将列表转换为ndarray
    a = np.asarray(x)
    logger.info(a)
    a = np.asarray(x,dtype=float)
    logger.info(a)
    
    #将元组转换为ndarray
    x=(2,4,5,7)
    a = np.asarray(x,dtype=float)
    logger.info(a)
    
    #将元组列表转换为ndarray
    x=[(1,3,5),(2,4)]
    a = np.asarray(x)
    logger.info(a)
    
    #numpy.frombuffer: 
    #将缓冲区解释为一维数组
    '''
    buf = 'hello world'
    a = np.frombuffer(buf,dtype='S1')
    logger.info(a)
    '''
    #numpy.fromiter: 可从任何可迭代对象构建一个ndarray对象，返回一个新的一维数组
    #numpy.fromiter(iterable,dtype,count=-1)
    lst = range(10)
    print(lst)
    logger.info(lst)
    it=iter(lst)
    x = np.fromiter(it,dtype=float)
    logger.info(x)
    
    #numpy.arange(start,stop,step,dtype):
    #返回一个从start开始到stop-1结束，步长为step的数组
    x = np.arange(5)
    logger.info(x)
    x = np.arange(5,dtype=float)
    logger.info(x)
    x=np.arange(10,20,2,dtype=float)
    logger.info(x)
    
    #numpy.linspace(start,stop,num,endpoint,retstep,dtype):
    #num: 要生成的均匀间隔样本的数量,默认为50
    #endpoint: 若为真，则最后一个值(stop)包含在样本中
    x= np.linspace(10,40,5,dtype=float)
    logger.info(x)
    
    #numpy.logspace(start,stop,num,endpoint,base,dtype):
    #num: 要生成的均匀间隔样本的数量,默认为50
    #base:默认为10
    x = np.logspace(1.0,2.0,num=10)
    logger.info(x)


#索引和切片
def index_slice():
    #字段访问、基本切片、高级索引
    a = np.arange(10)
    s = slice(2,7,3)
    logger.info(a[s])
    #通过直接向冒号对象提供由冒号分隔的切片参数(start:stop:step)也可以
    b = a[2:7:3]
    logger.info(b)
    c = a[:2]
    logger.info(c)
    d = a[2:]
    logger.info(d)
    e = a[2:6]
    logger.info(e)
    a = np.array([[1,3,5],[7,9,11],[2,4,6]])
    logger.info(a[1:])
    
    #Attention:
    #切片还可以使用省略号(...)以制作与数组维度长度相同的选择元组，
    #如果在行位置使用省略号，将返回包含行中项目的ndarray
    a = np.array([[1,3,5],[7,9,11],[2,4,6]])
    logger.info('a:')
    logger.info(a)
    #返回第二列
    col2 = a[...,1] #可以理解为：所有行的第二列
    logger.info('col2:')
    logger.info(col2)
    #返回第二行
    row2 = a[1,...] #可以理解为：第二行的所有列
    logger.info('row2:')
    logger.info(row2)
    #返回第一列及往后的数据
    col1 = a[...,1:] #可以理解为：所有行的第二列以及后面的列
    logger.info('col1:')
    logger.info(col1)


if __name__ == '__main__':
    config_logger()
    
    # ndarray_operate()
    # np_datatype()
    # array_attribute()
    #gen_array()
    index_slice()
