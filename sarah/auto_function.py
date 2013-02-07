'''
Created on 2013-2-6

@author: Man YUAN <epsilonyuan@gmail.com>
@author: Sarah YU <yyu.seu@gmail.com>
'''
import inspect
import sys

class AutoFunctionConstants(object):
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
        return [obj.get_property_name() for obj in self.lack_value_objects]
    
    def source_name(self):
        return self.source_obj.get_property_name()
    
    def __str__(self):
        return self.source_name() + ' needs value of: ' + self.lack_value_name()

class AutoFunctionPropertyBack(object):

    def __init__(self, value_index):
        self.value_index = value_index
        self.find_funcs()
    
    def get_setter_and_getter(self):
        return (self, self.setter_func)
    
    def find_funcs(self):
        name_and_methods = inspect.getmembers(self.__class__, predicate=inspect.ismethod)
        self._funcs = []
        for name, method in name_and_methods:
            if name.find(AutoFunctionConstants.COMMON_METHOD_PRE()) == 0:
                self._funcs.append(method)    
        self._last_func_index = 0
    
    def setter_func(self, inst, value):
        inst._auto_func_property_datas[self.value_index] = value
    
    def get_value(self, inst):
        return inst._auto_func_property_datas[self.value_index]
    
    def set_being_a_function(self, inst, value):
        inst._auto_func_property_as_functions[self.value_index] = value
    
    def is_being_a_function(self, inst):
        return inst._auto_func_property_as_functions[self.value_index]
    
    def is_source(self, inst):
        return self.get_value(inst) != None
    
    def is_conflicting_with_other_source(self, inst):
        if not self.is_source(inst):
            raise ValueError()
        backup_value = self.get_value(inst)
        self.setter_func(inst, None)
        result = False
        try:
            self.__call__(inst)
            result = True
        except LoopCallException:
            result = False
        finally:
            self.setter_func(inst, backup_value)
            return result      
        
    def __call__(self, inst):
        value = self.get_value(inst)
        if not value is None:
            return value
        elif self.is_being_a_function(inst):
            raise LoopCallException(self)
        else:
            self.set_being_a_function(inst, True)
            try:
                result = self.main_func(inst)
            except LoopCallException as e:
                if e.source_obj is None:
                    e.source_obj = self
                elif self is not e.source_obj:
                    e.lack_value_objects.add(self)
                raise e
            finally:    
                self.set_being_a_function(inst, False)
            return result
    
    def main_func(self, inst):
        size = len(self._funcs)
        if size == 0:
            raise LoopCallException()
        start = self._last_func_index
        for i in xrange(size):
            func_index = (i + start) % size
            func = self._funcs[func_index]
            try:
                value = func(self, inst)
                self._last_func_index = func_index
                return value
            except LoopCallException as e:
                if i >= size - 1:
                    raise e
            finally:
                i += 1
    
    def yufunc(self, inst):
        return self.__call__(inst)
    
    @classmethod
    def default(cls):
        return None
    
    @classmethod
    def get_property_name(cls):
        class_name = cls.__name__
        if class_name.find(AutoFunctionConstants.COMMON_REAL_CLASS_PRE()) != 0:
            raise ValueError('class name should begin with"' + AutoFunctionConstants.COMMON_REAL_CLASS_PRE() + '"')
        return class_name[len(AutoFunctionConstants.COMMON_REAL_CLASS_PRE()):]

class AutoMathFunctionMeta(type):
    def __new__(self, cls_name, bases, attrs):
        new_cls = type.__new__(self, cls_name, bases, attrs)
        all_property_classes = self.get_all_property_classes(new_cls)
        value_index = 0
        new_cls.default_auto_func_property_values = []
        new_cls.auto_func_property_backs = []
        for _name, property_cls in all_property_classes:
            new_cls.default_auto_func_property_values.append(property_cls.default())
            property_name = property_cls.get_property_name()
            property_back = property_cls(value_index)
            new_cls.auto_func_property_backs.append(property_back)
            setattr(new_cls, property_name, property(*(property_back.get_setter_and_getter())))
            value_index += 1
        return new_cls

    @classmethod
    def get_all_property_classes(cls, new_cls):
        clsmembers = inspect.getmembers(sys.modules[new_cls.__module__], inspect.isclass)
        result = [name_cls for name_cls in clsmembers if name_cls[0].find(AutoFunctionConstants.COMMON_REAL_CLASS_PRE()) == 0]
        return result

class AutoFunctionPropertyStatus(object):
    def __init__(self, property_back, inst):
        self.property_back = property_back
        self.inst = inst
    
    def get_head_name_value_string(self):
        property_back = self.property_back
        inst = self.inst
        head = None
        name = property_back.get_property_name()
        value_str = None
        if property_back.is_source(inst):
            head = self.get_source_head_string()
            value_str = str(property_back(inst))
            if property_back.is_conflicting_with_other_source(inst):
                value_str += " **CONFILCTING with other source properties**"
        else:
            try:
                value = property_back(inst)
                value_str = str(value)
                head = self.get_function_value_head_string()
            except LoopCallException as e:
                if(len(e.lack_value_names())) > 0:
                    head = self.get_lack_of_dependence_value_head_string()
                    value_str = str(e.lack_value_names())
                else:
                    head = self.get_unspecified_basis_value_head_string()
                    value_str = "unspecified basic source property"
            except Exception as e:
                value_str = "ERROR! " + e.message
        head = self.get_head_string_template() % head
        return (head, name, value_str)
        
    @classmethod
    def get_source_head_string(cls):
        return "SRC"
    
    @classmethod
    def get_lack_of_dependence_value_head_string(cls):
        return "LDEP"
    
    @classmethod
    def get_function_value_head_string(cls):
        return "F"
    
    @classmethod
    def get_max_head_length(cls):
        return 4;
    
    @classmethod
    def get_head_string_template(cls):
        return "%4s"
    
    @classmethod
    def get_unspecified_basis_value_head_string(cls):
        return "USPS"
    
    @classmethod
    def get_conflict_post_string(cls):
        return 'CONFILCTING with other value sources'
    
    @classmethod
    def get_head_and_instructions(cls):
        result = []
        result.append([cls.get_source_head_string(), "property value as source"])
        result.append([cls.get_lack_of_dependence_value_head_string(), "can't get value,"])
        result.append(["","part of the absent necessary property is shown as value"])
        result.append([cls.get_function_value_head_string(), "a function value"])
        return result
    
class AutoFunction(object):
    __metaclass__ = AutoMathFunctionMeta
    
    def __init__(self):
        self._auto_func_property_datas = list(self.default_auto_func_property_values)
        self._auto_func_property_as_functions = [False for _i in xrange(len(self._auto_func_property_datas))]
    def show_status(self):
        print self.status_str()
    
    @classmethod
    def get_status_str_gap_len(cls):
        return 2
    
    def status_str(self):
        result = self.__class__.__name__ + " auto math function property status:\n"
        head_len = AutoFunctionPropertyStatus.get_max_head_length()
        head_instructions = AutoFunctionPropertyStatus.get_head_and_instructions()
        gap_len = self.get_status_str_gap_len()
        name_len = self.get_max_math_property_names_len()        
        instruction_template = "%" + str(2+head_len + gap_len + name_len) + "s: %s\n"
        for head, instr in head_instructions:
            result += instruction_template % (head, instr)
        result += "="*(2+head_len+name_len+gap_len) + "\n"  

        status_template = "|%" + str(head_len) + "s|%" + str(gap_len + name_len) + "s: %s\n"
        for property_status in self.get_auto_function_property_status():
            head, name, value_str = property_status.get_head_name_value_string()
            result += status_template % (head, name, value_str)
        return result
    
    def get_auto_function_property_status(self):
        return [AutoFunctionPropertyStatus(property_back, self) 
                for property_back in self.get_auto_function_property_backs()]
    
    @classmethod   
    def get_auto_function_property_names(cls):
        return [property_back.get_property_name() for property_back in cls.auto_func_property_backs]
    
    @classmethod
    def get_auto_function_property_backs(cls):
        return cls.auto_func_property_backs
    
    @classmethod
    def get_max_math_property_names_len(cls):
        result = 0
        for name in cls.get_auto_function_property_names():
            name_len = len(name)
            if name_len > result:
                result = name_len
        return result
