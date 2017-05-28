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
import random


class AssertionPredictor(object):
    def unit_test_assembler(self, assert_sequence, feature_list, u_type):

        assertion_dictionary_type1 = []
        assertion_dictionary_type2 = []

        with open("namelist.txt") as myfile:
            for line in myfile:
                name, var = line.partition("=")[::2]
                assertion_dictionary_type1[name.strip()] = float(var)

        with open("namelist.txt") as myfile:
            for line in myfile:
                name, var = line.partition("=")[::2]
                assertion_dictionary_type2[name.strip()] = float(var)

        unit_test = ["describe('<add description>', function(){"]

        for feature, u_assert in zip(feature_list, assert_sequence):

            print(feature, u_assert)
            mock_feature = []

            if "function" in feature and unit_test == 0:
                header = self.get_unit_element(0, u_type)
                header.replace("description", feature.split(' ')[1])

            elif "function" not in feature and unit_test == 0:
                mock_feature.append(feature)

            elif "if" in feature:
                mock_var = self.generate_mock_var(feature, mock_feature)
                call_f = assertion_dictionary_type1[u_assert]
                unit_test.append(call_f + ' (' + str(mock_var[0]) + ', ' + str(mock_var[1]) + ")")

            elif "return" in feature:
                unit_test.append(assertion_dictionary_type1[u_assert])

        unit_test.append("})")
        unit_test.append("})")

    def generate_mock_var(self, feature, mock_feature):

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

    def assert_generator(self, u_assert):
        pass
