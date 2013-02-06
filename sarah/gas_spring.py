'''
Created on 2013-2-3

@author: Man YUAN <epsilonyuan@gmail.com>
@author: Sarah YU <yyu.seu@gmail.com>
'''

from math import cos, sin, acos, degrees, radians

import numpy as np

from sarah.auto_function import GeneralGetter, AutoMathFunctionMeta, LoopCallException
def vector(*args):
    return np.array(args, dtype=np.double)

class Sarah_ori(GeneralGetter):
    def __init__(self):
        super(Sarah_ori, self).__init__()
        self.value = vector(0, 0)
    pass

class Sarah_pt_a(GeneralGetter):
    pass

class Sarah_len_ao(GeneralGetter):
    def yufunc(self, gas_spring):
        vec = gas_spring.ori - gas_spring.pt_a
        return np.dot(vec, vec) ** 0.5

class Sarah_theta(GeneralGetter):
    def yufunc(self, gas_spring):
        vec = gas_spring.pt_a - gas_spring.ori
        return np.arctan2(vec[1], vec[0])

class Sarah_pt_b(GeneralGetter):
    def yufunc(self, gas_spring):
        r = gas_spring.len_brd
        alpha_b = gas_spring.alpha_b
        return np.array((r * cos(alpha_b), r * sin(alpha_b))) + gas_spring.ori

class Sarah_len_brd(GeneralGetter):
    def yufunc(self, gas_spring):
        vec = gas_spring.pt_c - gas_spring.ori
        return np.dot(vec, vec) ** 0.5

class Sarah_alpha_b(GeneralGetter):
    def yufunc(self, gas_spring):
        return gas_spring.alpha_c - gas_spring.alpha_delta
        

    def yufunc_2(self, gas_spring):
        vec = gas_spring.pt_b - gas_spring.ori
        return np.arctan2(vec[1], vec[0])
    
    def yufunc_3(self, gas_spring):
        r = gas_spring.len_brd
        d = gas_spring.len_ao
        len_spr_b = gas_spring.len_spr_b
        theta = gas_spring.theta
        angle_aob = acos((len_spr_b ** 2 - r ** 2 - d ** 2) / (2 * d * r))
        return  theta + angle_aob  
    
class Sarah_len_spr_b(GeneralGetter):
    def yufunc(self, gas_spring):
        vec = gas_spring.pt_b - gas_spring.pt_a
        return np.dot(vec, vec) ** 0.5
    
    def yufunc_2(self, gas_spring):
        return gas_spring.len_spr_c - gas_spring.len_spr_delta

class Sarah_pt_c(GeneralGetter):
    def yufunc(self, gas_spring):
        r = gas_spring.len_brd
        alpha_c = gas_spring.alpha_c
        return np.array((r * cos(alpha_c), r * sin(alpha_c)), dtype=np.double)

class Sarah_len_spr_c(GeneralGetter):
    def yufunc(self, gas_spring):
        vec = gas_spring.pt_c - gas_spring.pt_a
        return np.dot(vec, vec) ** 0.5
    
    def yufunc_2(self, gas_spring):
        return gas_spring.len_spr_b + gas_spring.len_spr_delta

class Sarah_alpha_delta(GeneralGetter):
    def yufunc(self, gas_spring):
        return gas_spring.alpha_c - gas_spring.alpha_b

class Sarah_alpha_c(GeneralGetter):
    def yufunc(self, gas_spring):
        return gas_spring.alpha_b + gas_spring.alpha_delta     
    
    def yufunc_2(self, gas_spring):
        vec = gas_spring.pt_c - gas_spring.ori
        return np.arctan2(vec[1], vec[0])
    
    def yufunc_3(self, gas_spring):
        len_spr_c = gas_spring.len_spr_c
        r = gas_spring.len_brd
        d = gas_spring.len_ao
        theta = gas_spring.theta
        angle_aoc = acos((len_spr_c ** 2 - d ** 2 - r ** 2) / (2 * d * r))
        return theta + angle_aoc

class Sarah_len_spr_delta(GeneralGetter):
    def yufunc(self, gas_spring):
        return gas_spring.len_spr_c - gas_spring.len_spr_b

class Sarah_arm_b(GeneralGetter):    
    def yufunc(self, gas_spring):
        vec_bo = gas_spring.ori - gas_spring.pt_b
        vec_ba = gas_spring.pt_a - gas_spring.pt_b
        len_ba = np.dot(vec_ba, vec_ba) ** 0.5
        return np.cross(vec_bo, vec_ba) / len_ba

        
class GasSpring(object):
    __metaclass__ = AutoMathFunctionMeta
    
    def show_status(self):
        print self.status()
    
    def status(self):
        result = "property status:\n"
        max_name_len = self.get_max_math_property_names_len()
        result_head = "\t%" + str(max_name_len) + "s: "

        result += result_head % "(PUEV" + "part of unspecified necessary values)\n"   

        for name in self.get_math_property_names():
            result += result_head % name
            try:
                value = getattr(self, name)
            except LoopCallException as e:
                if(len(e.lack_value_names())) > 0:
                    result += "PUEV" + str(e.lack_value_names())
                else:
                    result += "unspecified basic value"
            except AttributeError as e:
                result += "ERROR! " + e.message
            else:
                result += str(value)
            result += "\n"
        return result

    def get_math_property_names(self):
        return self.math_property_names
    
    def get_max_math_property_names_len(self):
        result = 0
        for name in self.get_math_property_names():
            name_len = len(name)
            if name_len > result:
                result = name_len
        return result  

if __name__ == '__main__':
    gs = GasSpring()
    print "haven't set any property"
    gs.show_status()
    gs.pt_a = vector(20, -5)
    gs.alpha_b = 0
    gs.alpha_delta = radians(80)
    gs.len_spr_c = 205
    gs.len_brd = 200
    gs.show_status()

