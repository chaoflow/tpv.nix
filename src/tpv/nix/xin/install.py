import tpv.cli

from tpv.ordereddict import OrderedDict


class Install(OrderedDict):
    """Install something

    And a longer descriptions for it.

    Stretching over multiple lines.
    """
    foo = tpv.cli.Flag(["f", "foo"],
                       help="If given, I will be very foo")

    def __call__(self, *programs):
        print("Removing %s %s" % (self.foo, programs,))

install = Install()
