from functools import partial


_compounds = dict()

def lift(obj):
    try:
        return _compounds[obj]
    except KeyError:
        _compounds[obj] = Compound(obj)
        return _compounds[obj]


def create_bridge_method(name):
    """
    Create a callable to be used as a drop-in for missing role methods.

    The callable just calls proceed().
    """
    def bridge(roles, compound, *args, **kwargs):
        return proceed(name, roles, compound, *args, **kwargs)
    return bridge


def proceed(name, roles, compound, *args, **kwargs):
    """Invoke the next method in the current dispatch context."""
    func = lookup(name, roles[1:], compound)
    return func(*args, **kwargs)


def lookup(name, roles, compound):
    """This method returns 2-ary 'handles' in every case."""
    if roles:
        func = getattr(roles[0], name, create_bridge_method(name))
        return partial(func, roles, compound)
    return getattr(compound.core, name)


class RoleType:
    pass


class Compound:
    """Wrap a core object and route method calls through its roles."""

    def __init__(self, core):
        if isinstance(core, RoleType):
            raise ValueError("roles cannot play roles")
        self.core = core
        self.roles = []

    def add_role(self, role):
        self.roles.append(role)

    def remove_role(self, role):
        self.roles.remove(role)

    def remove_all_roles(self):
        self.roles = []

    def __getattr__(self, name):
        return lookup(name, self.roles[:], self)

    def __repr__(self):
        return "Compound(%s)" % self.core
