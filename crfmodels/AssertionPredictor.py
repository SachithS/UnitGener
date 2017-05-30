"""
    AssertionPredictor.py - UnitGener Unit test assertions sequence generator 
    This class is responsible to generate he unit test assertions for the 
    predicted assertion sequence by the module and will complete the unit test 
    UnitGener system.

      @author      Sachith Senarathne
      @version     1.0
      @maintainer  Sachith Senarathne
      @copyright   Copyright 2017, The UnitGener Project
      @license     MIT
      @version     1.0
      @email       sachith.senarathnes@gmail.com
      @status      Development
"""
import os
import random


class AssertionPredictor(object):

    def unit_test_assembler(self, assert_sequence, feature_list, u_type):

        if u_type == 1:
            unit_test = []
            var_list = []
            assertion_dictionary_type1 = []
            dec_dictionary_type_1 = {}
            path_dir = os.path.dirname(__file__)

            with open(path_dir + "/mocha_assert.txt") as mocha_asserts:
                for line in mocha_asserts:
                    assert_id, assert_st = line.partition(":")[::2]
                    assertion_dictionary_type1.append(assert_st)

            with open(path_dir + "/declaration_mocha.txt") as declaration:
                for line in declaration:
                    dec_id, dec_st = line.partition(":")[::2]
                    dec_dictionary_type_1[dec_id] = dec_st

            unit_test.append(dec_dictionary_type_1['description'])

            for idx, remark in enumerate(assert_sequence[0]):

                if remark == 1:
                    if 'function' in feature_list[idx]:
                        unit_test.append(dec_dictionary_type_1['header'])
                        function_name = feature_list[idx].split(' ')[1]
                        continue
                    elif 'if' in feature_list[idx]:
                        f_call = dec_dictionary_type_1['function']
                        var_set = self.generate_mock_var(feature_list[idx])
                        if function_name is not None:
                            f_call = f_call.replace('func', function_name)
                        f_call = f_call.replace('var1', str(var_set[0]))
                        f_call = f_call.replace('var2', str(var_set[1]))
                        unit_test.append(f_call)
                        continue
                    else:
                        var_list.append(feature_list[idx])
                        continue

                elif remark == 2:
                    if 'true' in feature_list[idx]:
                        unit_test.append(dec_dictionary_type_1['true'])
                        continue
                    else:
                        unit_test.append(dec_dictionary_type_1['false'])
                        continue
                else:
                    if remark != 0:
                        unit_test.append(assertion_dictionary_type1[remark])
                    continue
            unit_test.append(dec_dictionary_type_1['enclose'])

            unit_test.append(dec_dictionary_type_1['enclose'])

            return unit_test

        else:
            unit_test = []
            var_list = []
            assertion_dictionary_type2 = []
            dec_dictionary_type_2 = {}
            path_dir = os.path.dirname(__file__)

            with open(path_dir + "/tape_assert.txt") as mocha_asserts:
                for line in mocha_asserts:
                    assert_id, assert_st = line.partition(":")[::2]
                    assertion_dictionary_type2.append(assert_st)

            with open(path_dir + "/declaration_tape.txt") as declaration:
                for line in declaration:
                    dec_id, dec_st = line.partition(":")[::2]
                    dec_dictionary_type_2[dec_id] = dec_st

            unit_test.append(dec_dictionary_type_2['description'])

            for idx, remark in enumerate(assert_sequence[0]):

                if remark == 1:
                    if 'function' in feature_list[idx]:
                        unit_test.append(dec_dictionary_type_2['header'])
                        function_name = feature_list[idx].split(' ')[1]
                        continue
                    elif 'if' in feature_list[idx]:
                        f_call = dec_dictionary_type_2['function']
                        var_set = self.generate_mock_var(feature_list[idx])
                        if function_name is not None:
                            f_call = f_call.replace('function', function_name)
                        f_call = f_call.replace('var1', str(var_set[0]))
                        f_call = f_call.replace('var2', str(var_set[1]))
                        unit_test.append(f_call)
                        continue
                    else:
                        var_list.append(feature_list[idx])
                        continue

                elif remark == 2:
                    if 'true' in feature_list[idx]:
                        unit_test.append(dec_dictionary_type_2['true'])
                        continue
                    else:
                        unit_test.append(dec_dictionary_type_2['false'])
                        continue
                else:
                    if remark != 0:
                        unit_test.append(assertion_dictionary_type2[remark])
                    continue
            unit_test.append(dec_dictionary_type_2['enclose'])

            unit_test.append(dec_dictionary_type_2['enclose'])

            return unit_test

    def generate_mock_var(self, feature):

            var_1, var_2 = 0, 0
            _sum_value = 0

            if "==" in feature:
                _sum_value = feature.split('==')[1]
                _sum_value = _sum_value.strip()
                if _sum_value.isdigit():
                    _sum_value_int = int(_sum_value)
                    if "+" in feature.split('==')[0]:
                        var_1 = random.randint(0, _sum_value_int)
                        var_2 = _sum_value_int - var_1
                    if "-" in feature.split('==')[0]:
                        var_1 = _sum_value_int * 2
                        var_2 = _sum_value_int
                    if "*" in feature.split('==')[0]:
                        while True:
                            count = 2
                            if _sum_value_int % count == 0:
                                var_2 = count
                                var_1 = _sum_value_int / var_2
                                break
                            count += 1
                        var_1 = random.randint(0, _sum_value_int)
                        var_2 = _sum_value_int - var_1
                    if "/" in feature.split('==')[0]:
                        var_2 = random.randint(0, 15)
                        var_1 = _sum_value_int * var_2

            return [var_1, var_2]
