cython学习笔记

1.cdef 与cpdef
C函数定义使用cdef，参数是Python对象也可以是C值，返回值可以使Python对象也可以是值
cdef定义的方法只能在cython中调用
def定义的方法可以再Python和Cython中调用，但由于要经过Python API的处理，所有速度较慢
cpdef既可以在Cython中调用也可以在Python中调用，可以说是两者的结合体，但在Cython内部调用速度略低于cdef

在class中用cdef public int count,则可以通过Python的变量获取count属性，不过由于要涉及多个Python API调用，
比直接cdef要慢很多。此外public不可以用于指针。(class也是如此，添加cdef public class loop，提供python访问loop)

在cdef class中(扩展类型)，def与cdef定义的可以被继承，所以cython需要判断cpdef定义的方法是否被覆盖，这也加剧了cpdef与cdef慢。


cpdef 只用于函数(可实现复写)

cdef class Function:
    cpdef double evaluate(self, double x) except *:
        return 0

cdef class SinOfSquareFunction(Function):
    cpdef double evaluate(self, double x) except *:
        return sin(x**2)

2.cimport cython
@cython.boundscheck(False) => 关闭负数下标处理
@cython.wraparound(False) => 关闭越界检查

3.
pyd 头文件 cimport
pyi include文件 include "spamstuff.pxi"

4.
cdef char *s
s = pystring1 + pystring2 XXXX
这回产生临时变量，导致s悬疑指针

p = pystring1 + pystring2
s = p

5.内型转换
<type>a 这并不检查，直接转换
<type*>a 会检查

6.
cdef int spam() except -1 =》spam发生错误将返回-1

cdef int spam() except? -1 =》-1仅仅是可能错误，
如果返回-1，cython会调用PyErr_Occurred去判断是否有异常

cdef int spam() except * =》cython每次都会调用yErr_Occurred

7.编译时定义
DEF FavouriteFood = "spam"
DEF ArraySize = 42
DEF OtherArraySize = 2 * ArraySize + 17

cdef int a1[ArraySize]
cdef int a2[OtherArraySize

8.条件语句
IF UNAME_SYSNAME == "Windows":
    include "icky_definitions.pxi"
ELIF UNAME_SYSNAME == "Darwin":
    include "nice_definitions.pxi"
ELIF UNAME_SYSNAME == "Linux":
    include "penguin_definitions.pxi"
ELSE:
    include "other_definitions.pxi"