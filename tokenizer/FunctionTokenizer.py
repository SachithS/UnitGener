"""
    FunctionToken.py - UnitGener Lexer 
    This class is responsible to manipulate the training data for the CRFModel. 
    It will process the data from reading file to creating features for the CRF model. 
    Will act as a Javascript lexer to the UnitGener system.

      @author      Sachith Senarathne
      @version     1.0
      @maintainer  Sachith Senarathne
      @copyright   Copyright 2017, The UnitGener Project
      @license     MIT
      @version     1.0
      @email       sachith.senarathnes@gmail.com
      @status      Development
"""

import re
import os


class FunctionTokenizer(object):

    def read_process_file(self):
        print "Start reading input file"
        path_dir = os.path.dirname(__file__)
        _result_list = []
        with open(path_dir + "/../input_functions.txt") as inputFile:
            content = inputFile.readlines()
            print content
            skip_features = ['(', ')', '{', '}']
        for line in content:
            if line != '/n':
                js_tokens = []
                string_tokens = self.pre_process_tokens(line.split())
                count = 0
                print 'Length of tokens - ' + str(len(string_tokens))
                for _token in string_tokens:
                    # print _token
                    if skip_features.__contains__(_token):
                        continue
                    elif _token == 'function':
                        js_tokens.append(_token + ' ' + string_tokens[count + 1])
                        string_tokens.pop(count + 1)
                    else:
                        js_tokens.append(_token)
                    count += 1

                variable_token_result = self.process_dec_tokens(js_tokens)
                format_result_tokens = self.conditional_token_processor(variable_token_result)
                result_tokens = self.literal_token_processor(format_result_tokens)
                trim_tokens = self.trim_process_tokens(result_tokens)
                return_tokens = self.statement_token_builder(trim_tokens)

                for token in return_tokens:
                    print token

                return return_tokens

    def pre_process_tokens(self, str_tokens):
        _return_tokens = []
        for _raw_token in str_tokens:
            temp = ''.join(c for c in _raw_token if c not in '}{')
            if temp != '':
                _return_tokens.append(temp)
        return _return_tokens

    def conditional_token_processor(self, js_tokens):
        _processed_tokens = []
        for idx, token in enumerate(js_tokens):
            if token in ('&&', '||', '!=', '==', '===', '!==', '='):
                tmp_tkn = js_tokens[idx - 1] + ' ' + token + ' ' + js_tokens[idx + 1]
                # tmp_tkn = re.sub('[)(]', '', tmp_tkn)
                if js_tokens[idx - 1] in _processed_tokens:
                    _processed_tokens.remove(js_tokens[idx - 1])
                if js_tokens[idx - 1] in js_tokens:
                    js_tokens.pop(idx + 1)
                _processed_tokens.append(tmp_tkn)
            else:
                if token != '':
                    _processed_tokens.append(token)

        return _processed_tokens

    def literal_token_processor(self, format_result_tokens):
        _lit_tokens = []
        for idx, lit_token in enumerate(format_result_tokens):
            if re.match("'", lit_token):
                if lit_token.count('"') > 1:
                    format_result_tokens.append(lit_token)
                    continue
                elif lit_token.count() == 1:
                    _lit_tokens.append(lit_token + ' ' + format_result_tokens[idx + 1])
                    format_result_tokens.pop(idx + 1)
                if lit_token.count("'") > 1:
                    format_result_tokens.append(lit_token)
                    continue
                elif lit_token.count() == 1:
                    _lit_tokens.append(lit_token + ' ' + format_result_tokens[idx + 1])
                    format_result_tokens.pop(idx + 1)
            else:
                if lit_token != '':
                    _lit_tokens.append(lit_token)

        return _lit_tokens

    def process_dec_tokens(self, js_tokens):
        _dec_token_list = []
        for idx, dec_token in enumerate(js_tokens):
            if dec_token == 'var':
                temp_tkn = dec_token + ' ' + js_tokens[idx + 1]
                js_tokens.pop(idx + 1)
                _dec_token_list.append(temp_tkn)
            else:
                if not dec_token == '':
                    _dec_token_list.append(dec_token)
        return _dec_token_list

    def arr_token_processor(self, variable_token_result):
        _arr_results = []
        for idx, arr_token in enumerate(variable_token_result):
            if "[" in arr_token:
                if "]" in arr_token:
                    pass
                else:
                    _arr_results.append(arr_token)
            else:
                if arr_token != '':
                    _arr_results.append(arr_token)

        return _arr_results

    def check_for_special_character(self, token, _char):
        _is_available = False
        for _atomic in token:
            if _atomic == _char:
                _is_available = True

        return _is_available

    def statement_token_builder(self, result_tokens):
        _build_tokens = []
        _for_header = []

        for idx, token in enumerate(result_tokens):
            if self.check_for_special_character(token, '('):
                if result_tokens[idx - 1] == "for":
                    for ind, item in enumerate(result_tokens[idx:len(result_tokens)]):
                        if not self.check_for_special_character(item, ')'):
                            _for_header.append(item)
                            # result_tokens.remove(item)
                        else:
                            _for_header.append(item)
                            _header_item = ''.join(_for_header)
                            _header_item = _header_item.replace("var", "var ")
                            _header_item = _header_item.replace(";", "; ")
                            _build_tokens.append(_header_item)
                            # result_tokens.remove(item)
                            break
                else:
                    _build_tokens.append(token)

            else:
                _build_tokens.append(token)

        for token in enumerate(_for_header):
            if token[1] in _build_tokens:
                _build_tokens.remove(token[1])

        return _build_tokens

    def trim_process_tokens(self, result_tokens):
        _return_tokens = []

        for idx, token in enumerate(result_tokens):

            if token != ',':
                token = token.replace('(', " ")
                token = token.replace(')', " ")
                token = token.strip()
                _return_tokens.append(token)

            if token == 'return':
                token = token + ' ' + result_tokens[idx + 1]
                _return_tokens.append(token)
                _return_tokens.remove('return')
                result_tokens.remove(result_tokens[idx + 1])
                break

        _processed_tokens = []

        for idx, token in enumerate(_return_tokens):
            if token in ('+', '-', '*', '/', '%'):
                tmp_tkn = _return_tokens[idx - 1] + ' ' + token + ' ' + _return_tokens[idx + 1]
                if _return_tokens[idx - 1] in _processed_tokens:
                    _processed_tokens.remove(_return_tokens[idx - 1])
                if _return_tokens[idx - 1] in _return_tokens:
                    _return_tokens.pop(idx + 1)
                _processed_tokens.append(tmp_tkn)
            else:
                if token != '':
                    _processed_tokens.append(token)

        return _processed_tokens

    def main(self):
        self.read_process_file()

    if __name__ == '__main__': main()
