
# distutils: language=c++
# cython: language_level=3, boundscheck=False, wraparound=False,nonecheck=False
# cython: cdivision=True

cimport numpy as np

# Vector (cpp)
from libcpp.vector cimport vector
# algorithm(cpp)
from libcpp.algorithm cimport max_element,min_element
# pointer (cython)
from cython.operator cimport dereference as deref 

# float64型
ctypedef np.float64_t DTYPE_f64

def pic_cut_calc(np.ndarray[DTYPE_f64,ndim = 2] dets,int height,int width):

    cdef: 
        np.ndarray[DTYPE_f64,ndim = 1]  final_cls_inds
        np.ndarray[DTYPE_f64,ndim = 2] final_boxes
        int count_y_axis
        int i = 0
        int people_count = 0
        vector[float] data_x_min = []
        vector[float] data_y_min = []
        vector[float] data_x_max = []
        vector[float] data_y_max = []
        float Xmin = 0
        float Ymin = 0
        float Xmax = 0
        float Ymax = 0

    final_boxes = dets[:,:4]
    final_cls_inds = dets[:,5]
    count_y_axis = final_boxes.shape[0]
    

    for i in range(0,count_y_axis):
        if final_cls_inds[i] == 0:
            data_x_min.push_back(final_boxes[i][0])
            data_y_min.push_back(final_boxes[i][1])
            data_x_max.push_back(final_boxes[i][2])
            data_y_max.push_back(final_boxes[i][3])
            people_count = people_count + 1
    if(people_count > 0):
        Xmax = deref(max_element(data_x_max.begin(),data_x_max.end()))
        Ymax = deref(max_element(data_y_max.begin(),data_y_max.end()))
        Xmin = deref(min_element(data_y_min.begin(),data_y_min.end()))
        Ymin = deref(min_element(data_x_min.begin(),data_x_min.end()))
        people_count = 0

        if(Xmin - 20 > 0):
            Xmin -= 20
        else:
            Xmin = 0
        if(Ymin - 20 > 0):
            Ymin -= 20
        else:
            Ymin = 0
        if(Xmax + 20 < width):
            Xmax += 20
        else:
            Xmax = width
        if(Ymax + 20 < height):
            Ymax += 20
        else:
            Ymax = height

        return Xmin, Ymin, Xmax, Ymax


