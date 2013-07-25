import tpv.cli

from tpv.ordereddict import OrderedDict


class Remove(OrderedDict):
    """Remove something
    """
    foo = tpv.cli.Flag(["f", "foo"],
                       help="If given, I will be very foo")

    def __call__(self, *programs):
        print("Removing %s %s" % (self.foo, programs,))

remove = Remove()
