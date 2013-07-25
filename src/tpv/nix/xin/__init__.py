"""xin - prototypical unified cli for nix
"""

import tpv.cli
import tpv.pkg_resources

from tpv.ordereddict import OrderedDict


@tpv.pkg_resources.children_from_entry_points(
    entry_point_group="tpv.nix.xin.commands",
)
class Xin(OrderedDict):
    """Prototypical unified nix command line.

    Come join the discussion!
    """
    verbose = tpv.cli.Flag(["v", "verbose"],
                           help="If given, I will be very talkative")

    def __call__(self, filename=None):
        if self.nested_command:
            return
        print "I will now read", filename
        if self.verbose:
            print "Yadda " * 200

    @tpv.cli.switch(['f', 'foo'], int)
    def foo(self, bar):
        """foomagic
        """
        print(bar)


app = tpv.cli.application(Xin)()
