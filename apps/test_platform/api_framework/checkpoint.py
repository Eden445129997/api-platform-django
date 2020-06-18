#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging, re, json, jsonpath

from apps.test_platform.enumeration import CheckMethod

# 日志
runner_log = logging.getLogger('runner_log')


class CheckpointBuilder(object):
    """
    校验点建造者
    """

    log = runner_log

    def __init__(self):
        self.result = {
            'error_list': []
        }
        # 方法字典
        self._funcs_dict = {
            CheckMethod.ASSERT_EQUAL.value: "_assertEqual",
            CheckMethod.ASSERT_NOT_EQUAL.value: '_assertNotEqual',
            CheckMethod.ASSERT_IN.value: '_assertIn',
            CheckMethod.ASSERT_NOT_IN.value: '_assertNotIn'
        }

    def _error_record(self, *error_info):
        """
        异常流
        :param report_id:
        :param error_info:
        :return:
        """
        self.log.error('error_info：%s' % str(error_info))
        self.result.get('error_list', []).extend(error_info)

    def build(self, checkpoint_list, response):
        # 处理response数据
        if isinstance(response, dict):
            try:
                response = json.dumps(response, ensure_ascii=False)
            except Exception as e:
                self._error_record('json序列化失败:\n响应参：{}\n错误：{}'.format(response, e))
                return self.result

        # 循环校验
        for check_info in checkpoint_list:
            jsonpath_expression = check_info.get('check_object')
            check_method = check_info.get('check_method')
            check_value = check_info.get('check_value')

            # todo：jsonpath_expression/check_method/check_value获取不到数据的

            catch_list = jsonpath.jsonpath(response, jsonpath_expression)
            # list为空则添加error
            if not catch_list:
                self._error_record('jsonpath表达式捕捉为空:\n表达式：{}\n捕捉结果：{}'.format(jsonpath_expression, catch_list))
            else:
                # 校验
                check_result = self._to_check(check_method, catch_list[0], check_value)
                # print(check_result)
                # 校验失败进入判断
                if not check_result:
                    self._error_record(
                        {'check_object': catch_list[0], 'check_method': check_method, 'check_value': check_value}
                    )
        return self.result

    def _to_check(self, func, first, second):
        # 根据设置的枚举选择并获取方法
        assertion_func = self._getAssertFunc(func)
        # 校验的对象都转成字符串
        first, second = str(first).replace(' ', ''), str(second).replace(' ', '')
        # 返回true或者false
        return assertion_func(first, second)

    def _getAssertFunc(self, func):
        """根据字典获取对应的方法"""
        asserter = self._funcs_dict.get(func)
        if asserter is not None:
            if isinstance(asserter, str):
                asserter = getattr(self, asserter)
            return asserter
        # 不是统一数据类型返回默认验证方法
        return self._baseAssertEqual

    def _baseAssertEqual(self, first, second):
        """默认校验方法"""
        if not first == second:
            self.result.get('error_list', []).append(self._baseAssertEqual)

    def _assertEqual(self, first, second):
        """判断值相等"""
        return first == second

    def _assertNotEqual(self, first, second):
        """判断值不想等"""
        return first != second

    def _assertIn(self, first, second):
        """判断包含"""
        return second in first

    def _assertNotIn(self, first, second):
        """判断不包含"""
        return second not in first

# if __name__ == '__main__':
# check = CheckpointBuilder()
