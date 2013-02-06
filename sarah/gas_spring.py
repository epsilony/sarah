'''
Created on 2013-2-3

@author: Man YUAN <epsilonyuan@gmail.com>
@author: Sarah YU <yyu.seu@gmail.com>
'''

from math import cos, sin, acos, degrees, radians

import numpy as np

from sarah.auto_function import GeneralGetter, AutoMathFunction
def vector(*args):
    return np.array(args, dtype=np.double)

class Sarah_ori(GeneralGetter):
    @classmethod
    def default(cls):
        return vector(0,0)
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

        
class GasSpring(AutoMathFunction):
    pass

if __name__ == '__main__':
    gs = GasSpring()
    print "haven't set any property"
    gs.show_status()
    gs.ori=vector(0,0)
    gs.pt_a = vector(20, -5)
    gs.alpha_b = 0
    gs.alpha_delta = radians(80)
    gs.len_spr_c = 205
    gs.len_brd = 200
    gs.show_status()

