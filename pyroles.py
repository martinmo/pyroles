"""A high-level, purely educational illustration of the RoleVM role dispatch."""

from functools import partial

# public API:
__all__ = ["lift", "proceed", "RoleType", "Compound"]

_compounds = dict()

def lift(obj):
    """Return the global compound object for the given object."""
    try:
        return _compounds[obj]
    except KeyError:
        _compounds[obj] = Compound(obj)
        return _compounds[obj]


def proceed(name, roles, compound, *args, **kwargs):
    """Invoke the next method in the current dispatch context."""
    func = _lookup(name, roles[1:], compound)
    return func(*args, **kwargs)


def _lookup(name, roles, compound):
    """Return a callable representing the next role or core method with the given name."""
    if roles:
        # bridge missing method in the role, if necessary
        func = getattr(roles[0], name, _create_missing_method(name))
        # role methods have a different calling convention, and expect
        # the dispatch context and the compound object as arguments:
        return partial(func, roles, compound)
    return getattr(compound.core, name)


def _create_missing_method(name):
    """Create a drop-in callable for a missing role method with the given name."""
    def bridge(roles, compound, *args, **kwargs):
        return proceed(name, roles, compound, *args, **kwargs)
    return bridge


class RoleType:
    """Empty marker class to distinguish natural and role types."""


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
        """Lookup attributes in roles (if any), or in the core object."""
        return _lookup(name, self.roles[:], self)

    def __repr__(self):
        return "Compound(%r)" % self.core
