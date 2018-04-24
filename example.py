#!/usr/bin/env python3
from pyroles import lift as _, proceed, Compound, RoleType


class Core:
    def __init__(self, name):
        self.name = name

    def method1(self, arg):
        print('%r::method1(%s)' % (self, arg))

    def method2(self):
        print('%r::method2()' % self)
        _(self).method1("delegated from %r" % self)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.name)


class RoleTypeBase(RoleType):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.name)


class RoleA(RoleTypeBase):
    def method1(self, roles, compound, arg):
        print("%r::method1(%s)" % (self, arg))
        proceed("method1", roles, compound, arg)


class RoleB(RoleTypeBase):
    def method1(self, roles, compound, arg):
        print("%r::method1(%s)" % (self, arg))


class RoleC(RoleA):
    def method2(self, roles, compound):
        print("%r::method2()" % self)
        compound.method1("delegated from %r" % self)


def scenario1():
    core = _(Core("core1"))
    core.add_role(RoleA("role_a1"))
    core.add_role(RoleA("role_a2"))
    core.method1("test")


def scenario2():
    core = _(Core("core2"))
    core.add_role(RoleA("role_a1"))
    core.add_role(RoleB("role_b1"))
    core.method2()


def scenario3():
    core = _(Core("core3"))
    core.add_role(RoleA("role_a1"))
    core.add_role(RoleB("role_b1"))
    core.add_role(RoleC("role_c1"))
    core.method2()


def scenario4():
    core = _(Core("core4"))
    core.add_role(RoleA("role_a1"))
    core.add_role(RoleC("role_c1"))
    core.method2()


def main():
    scenarios = [scenario1, scenario2, scenario3, scenario4]
    for scenario in scenarios:
        print("### %s" % scenario.__name__)
        scenario()


if __name__ == '__main__':
    main()
