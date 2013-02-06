'''
Created on 2013-2-6

@author: epsilon
'''
import inspect
import sys

class Constants(object):
    @classmethod
    def COMMON_REAL_CLASS_PRE(cls):
        return "Sarah_"
    
    @classmethod
    def COMMON_METHOD_PRE(cls):
        return "yufunc"

class LoopCallException(Exception):
    def __init__(self, source_obj):
        self.source_obj = source_obj
        self.lack_value_objects = set()
    
    def lack_value_names(self):
        return [obj.get_math_name() for obj in self.lack_value_objects]
    
    def source_name(self):
        return self.source_obj.get_math_name()
    
    def __str__(self):
        return self.source_name() + ' needs value of: ' + self.lack_value_name()

class GeneralSetter(object):
    def __init__(self, getter):
        self.getter = getter;
    def __call__(self, gas_spring, value):
        self.getter.value = value

class GeneralGetter(object):

    def __init__(self):
        self.being_a_function = False
        self.value = None
        self.find_funcs()
    
    def find_funcs(self):
        name_and_methods=inspect.getmembers(self.__class__, predicate=inspect.ismethod)
        self._funcs=[]
        for name,method in name_and_methods:
            if name.find(Constants.COMMON_METHOD_PRE())==0:
                self._funcs.append(method)
    
    def self_and_setter(self):
        return (self, GeneralSetter(self))
    
    def __call__(self, gas_spring):
        if not self.value is None:
            return self.value
        elif self.being_a_function:
            raise LoopCallException(self)
        else:
            self.being_a_function = True
            try:
                result = self.main_func(gas_spring)
            except LoopCallException as e:
                if e.source_obj is None:
                    e.source_obj=self
                elif self is not e.source_obj:
                    e.lack_value_objects.add(self)
                raise e
            finally:    
                self.being_a_function = False
            return result
    
    def main_func(self,gas_spring):
        size=len(self._funcs)
        if size==0:
            raise LoopCallException()
        i=0
        for func in self._funcs:
            try:
                return func(self,gas_spring)
            except LoopCallException as e:
                if i>=size-1:
                    raise e
            finally:
                i+=1
    
    def yufunc(self, gas_spring):
        return self.__call__(gas_spring)
    
    @classmethod
    def get_math_name(cls):
        class_name = cls.__name__
        if class_name.find(Constants.COMMON_REAL_CLASS_PRE()) != 0:
            raise ValueError('class name should begin with"' + Constants.COMMON_REAL_CLASS_PRE() + '"')
        return class_name[len(Constants.COMMON_REAL_CLASS_PRE()):]

class AutoMathFunctionMeta(type):
    def __new__(self, cls_name, bases, attrs):
        new_cls = type.__new__(self, cls_name, bases, attrs)
        all_property_classes = self.get_all_property_classes(new_cls)
        for _name, func_cls in all_property_classes:
            setattr(new_cls, func_cls.get_math_name(), property(*(func_cls().self_and_setter())))
        new_cls.math_property_names=[func_cls.get_math_name() for _name,func_cls in all_property_classes]     
        return new_cls

    @classmethod
    def get_all_property_classes(cls,new_cls):
        clsmembers = inspect.getmembers(sys.modules[new_cls.__module__], inspect.isclass)
        result = [name_cls for name_cls in clsmembers if name_cls[0].find(Constants.COMMON_REAL_CLASS_PRE()) == 0]
        return result  