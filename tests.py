#!/usr/bin/env python3
from io import StringIO
from unittest.mock import patch
from textwrap import dedent

from example import *


@patch("sys.stdout", new_callable=StringIO)
def assert_output_equals(func, expected, mock_stdout):
    func()
    assert mock_stdout.getvalue() == dedent(expected)


assert_output_equals(scenario1, """\
    RoleA(role_a1)::method1(test)
    RoleA(role_a2)::method1(test)
    Core(core1)::method1(test)
""")

assert_output_equals(scenario2, """\
    Core(core2)::method2()
    RoleA(role_a1)::method1(delegated from Core(core2))
    RoleB(role_b1)::method1(delegated from Core(core2))
""")

assert_output_equals(scenario3, """\
    RoleC(role_c1)::method2()
    RoleA(role_a1)::method1(delegated from RoleC(role_c1))
    RoleB(role_b1)::method1(delegated from RoleC(role_c1))
""")

assert_output_equals(scenario4, """\
    RoleC(role_c1)::method2()
    RoleA(role_a1)::method1(delegated from RoleC(role_c1))
    RoleC(role_c1)::method1(delegated from RoleC(role_c1))
    Core(core4)::method1(delegated from RoleC(role_c1))
""")

assert_output_equals(scenario5, """\
    RoleD(role_d1)::method1(test)
    RoleA(role_c1)::method1(test)
    Core(core5)::method1(test)
    RoleA(role_c1)::method1(test)
    Core(core5)::method1(test)
""")

assert_output_equals(scenario6, """\
    Core(core6)::method3(some value)
    argument: some value
""")

print("OK")
