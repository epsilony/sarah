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

class GeneralGetter(object):

    def __init__(self):
        self.find_funcs()
    
    def find_funcs(self):
        name_and_methods = inspect.getmembers(self.__class__, predicate=inspect.ismethod)
        self._funcs = []
        for name, method in name_and_methods:
            if name.find(Constants.COMMON_METHOD_PRE()) == 0:
                self._funcs.append(method)
    
    def self_and_setter(self, value_index):
        self.value_index = value_index
        return (self, self.setter_func)
    
    def setter_func(self, gas_spring, value):
        gas_spring._math_property_datas[self.value_index] = value
    
    def get_value(self, gas_spring):
        return gas_spring._math_property_datas[self.value_index]
    
    def set_being_a_function(self, gas_spring, value):
        gas_spring._math_property_as_function_list[self.value_index] = value
    
    def is_being_a_function(self, gas_spring):
        return gas_spring._math_property_as_function_list[self.value_index]
    
    def __call__(self, gas_spring):
        value = self.get_value(gas_spring)
        if not value is None:
            return value
        elif self.is_being_a_function(gas_spring):
            raise LoopCallException(self)
        else:
            self.set_being_a_function(gas_spring, True)
            try:
                result = self.main_func(gas_spring)
            except LoopCallException as e:
                if e.source_obj is None:
                    e.source_obj = self
                elif self is not e.source_obj:
                    e.lack_value_objects.add(self)
                raise e
            finally:    
                self.set_being_a_function(gas_spring, False)
            return result
    
    def main_func(self, gas_spring):
        size = len(self._funcs)
        if size == 0:
            raise LoopCallException()
        i = 0
        for func in self._funcs:
            try:
                return func(self, gas_spring)
            except LoopCallException as e:
                if i >= size - 1:
                    raise e
            finally:
                i += 1
    
    def yufunc(self, gas_spring):
        return self.__call__(gas_spring)
    
    @classmethod
    def default(cls):
        return None
    
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
        i = 0
        new_cls.default_property_values=[]
        for _name, func_cls in all_property_classes:
            new_cls.default_property_values.append(func_cls.default())
            setattr(new_cls, func_cls.get_math_name(), property(*(func_cls().self_and_setter(i))))
            i += 1
        new_cls.math_property_names = [func_cls.get_math_name() for _name, func_cls in all_property_classes]     
        return new_cls

    @classmethod
    def get_all_property_classes(cls, new_cls):
        clsmembers = inspect.getmembers(sys.modules[new_cls.__module__], inspect.isclass)
        result = [name_cls for name_cls in clsmembers if name_cls[0].find(Constants.COMMON_REAL_CLASS_PRE()) == 0]
        return result
    
class AutoMathFunction(object):
    __metaclass__ = AutoMathFunctionMeta
    
    def __init__(self):
        self._math_property_datas = list(self.default_property_values)
        self._math_property_as_function_list = [False for _i in xrange(len(self._math_property_datas))]
    
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
    
    @classmethod   
    def get_math_property_names(cls):
        return cls.math_property_names
    
    @classmethod
    def get_max_math_property_names_len(cls):
        result = 0
        for name in cls.get_math_property_names():
            name_len = len(name)
            if name_len > result:
                result = name_len
        return result
