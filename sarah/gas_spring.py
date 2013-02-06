'''
Created on 2013-2-3

@author: Man YUAN <epsilonyuan@gmail.com>
@author: Sarah YU <yyu.seu@gmail.com>
'''

from math import cos, sin,acos,degrees,radians

import numpy as np

from sarah.auto_function import GeneralGetter, AutoMathFunctionMeta, LoopCallException
def vector(*args):
    return np.array(args, dtype=np.double)

class Sarah_ori(GeneralGetter):
    def __init__(self):
        super(Sarah_ori, self).__init__()
        self.value = np.zeros((2,), dtype=np.double)
    pass

class Sarah_pt_a(GeneralGetter):
    pass

class Sarah_pt_d(GeneralGetter):
    def func(self,gas_spring):
        vec=  gas_spring.ori-gas_spring.pt_a
        return np.dot(vec,vec)**0.5

class Sarah_theta(GeneralGetter):
    def func(self,gas_spring):
        vec=  gas_spring.pt_a-gas_spring.ori
        return np.arctan2(vec[1],vec[0])

class Sarah_pt_b(GeneralGetter):
    def func(self, gas_spring):
        r = gas_spring.r
        alpha_b = gas_spring.alpha_b
        return np.array((r * cos(alpha_b), r * sin(alpha_b))) + gas_spring.ori

class Sarah_r(GeneralGetter):
    def func(self, gas_spring):
        vec = gas_spring.pt_c - gas_spring.ori
        return np.dot(vec, vec) ** 0.5

class Sarah_alpha_b(GeneralGetter):
    def func(self, gas_spring):
        try:
            return gas_spring.alpha_c-gas_spring.delta_alpha
        except LoopCallException:
            return self.func_2(gas_spring)

    def func_2(self,gas_spring):
        try:
            vec = gas_spring.pt_b - gas_spring.ori
            return np.arctan2(vec[1], vec[0])
        except LoopCallException:
            self.func_3(gas_spring)
    
    def func_3(self,gas_spring):
        r=gas_spring.r
        d=gas_spring.d
        len_g_b=gas_spring.len_g_b
        theta=gas_spring.theta
        angle_aob=acos((len_g_b**2-r**2-d**2)/(2*d*r))
        return  theta+angle_aob  
    
class Sarah_len_g_b(GeneralGetter):
    def func(self, gas_spring):
        vec = gas_spring.pt_b - gas_spring.pt_a
        return np.dot(vec, vec) ** 0.5

class Sarah_pt_c(GeneralGetter):
    def func(self, gas_spring):
        r = gas_spring.r
        alpha_c = gas_spring.alpha_c
        return np.array((r * cos(alpha_c), r * sin(alpha_c)), dtype=np.double)

class Sarah_len_g_c(GeneralGetter):
    def func(self, gas_spring):
        vec = gas_spring.pt_c - gas_spring.pt_a
        return np.dot(vec, vec) ** 0.5

class Sarah_delta_alpha(GeneralGetter):
    def func(self, gas_spring):
        return gas_spring.alpha_c - gas_spring.alpha_b

class Sarah_alpha_c(GeneralGetter):
    def func(self,gas_spring):
        try:
            return gas_spring.alpha_b + gas_spring.delta_alpha     
        except LoopCallException:
            return self.func_2(gas_spring)
    
    def func_2(self,gas_spring):
        try:
            vec=gas_spring.pt_c-gas_spring.ori
            return np.arctan2(vec[1],vec[0])
        except LoopCallException:
            self.func_3(gas_spring)
    
    def func_3(self,gas_spring):
        len_g_c=gas_spring.len_g_c
        r=gas_spring.r
        d=gas_spring.d
        theta=gas_spring.theta
        angle_aoc=acos((len_g_c**2-d**2-r**2)/(2*d*r))
        return theta+angle_aoc

class Sarah_delta_g(GeneralGetter):
    def func(self, gas_spring):
        return gas_spring.len_g_c - gas_spring.len_g_b

class Sarah_arm_b(GeneralGetter):    
    def func(self, gas_spring):
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
                value=getattr(self, name)
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
    gs.delta_alpha=radians(80)
    gs.len_g_c=205
    gs.r=200
    gs.show_status()

