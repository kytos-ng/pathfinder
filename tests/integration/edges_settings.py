"""Module to overwrite all the needed methods."""

# Core modules to import
from kytos.core.link import Link

# pylint: disable=E0401
from tests.integration.test_paths import TestPaths


class EdgesSettings(TestPaths):
    """Class to setups all the settings related to topology."""

    @staticmethod
    def generate_topology():
        """Generate a predetermined topology."""
        switches, interfaces, links = {}, {}, {}

        TestPaths.create_switch("S1", switches)
        TestPaths.add_interfaces(2, switches["S1"], interfaces)

        TestPaths.create_switch("S2", switches)
        TestPaths.add_interfaces(2, switches["S2"], interfaces)

        TestPaths.create_switch("S3", switches)
        TestPaths.add_interfaces(6, switches["S3"], interfaces)

        TestPaths.create_switch("S4", switches)
        TestPaths.add_interfaces(2, switches["S4"], interfaces)

        TestPaths.create_switch("S5", switches)
        TestPaths.add_interfaces(6, switches["S5"], interfaces)

        TestPaths.create_switch("S6", switches)
        TestPaths.add_interfaces(5, switches["S6"], interfaces)

        TestPaths.create_switch("S7", switches)
        TestPaths.add_interfaces(2, switches["S7"], interfaces)

        TestPaths.create_switch("S8", switches)
        TestPaths.add_interfaces(8, switches["S8"], interfaces)

        TestPaths.create_switch("S9", switches)
        TestPaths.add_interfaces(4, switches["S9"], interfaces)

        TestPaths.create_switch("S10", switches)
        TestPaths.add_interfaces(3, switches["S10"], interfaces)

        TestPaths.create_switch("S11", switches)
        TestPaths.add_interfaces(3, switches["S11"], interfaces)

        TestPaths.create_switch("User1", switches)
        TestPaths.add_interfaces(4, switches["User1"], interfaces)

        TestPaths.create_switch("User2", switches)
        TestPaths.add_interfaces(2, switches["User2"], interfaces)

        TestPaths.create_switch("User3", switches)
        TestPaths.add_interfaces(2, switches["User3"], interfaces)

        TestPaths.create_switch("User4", switches)
        TestPaths.add_interfaces(3, switches["User4"], interfaces)

        EdgesSettings._fill_links(links, interfaces)

        EdgesSettings._add_metadata_to_links(links)

        return switches, links

    @staticmethod
    def _add_metadata_to_links(links):
        links["S1:1<->S2:1"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 105}
        )

        links["S1:2<->User1:1"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 1}
        )

        links["S2:2<->User4:1"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 10}
        )

        links["S3:1<->S5:1"].extend_metadata(
            {"reliability": 5, "bandwidth": 10, "delay": 112}
        )

        links["S3:2<->S7:1"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 1}
        )

        links["S3:3<->S8:1"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 1}
        )

        links["S3:4<->S11:1"].extend_metadata(
            {"reliability": 3, "bandwidth": 100, "delay": 6}
        )

        links["S3:5<->User3:1"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 1}
        )

        links["S3:6<->User4:2"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 10}
        )

        links["S4:1<->S5:2"].extend_metadata(
            {
                "reliability": 1,
                "bandwidth": 100,
                "delay": 30,
                "ownership": {"A": {}},
            }
        )

        links["S4:2<->User1:2"].extend_metadata(
            {
                "reliability": 3,
                "bandwidth": 100,
                "delay": 110,
                "ownership": {"A": {}},
            }
        )

        links["S5:3<->S6:1"].extend_metadata(
            {"reliability": 1, "bandwidth": 100, "delay": 40}
        )

        links["S5:4<->S6:2"].extend_metadata(
            {
                "reliability": 3,
                "bandwidth": 100,
                "delay": 40,
                "ownership": {"A": {}},
            }
        )

        links["S5:5<->S8:2"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 112}
        )

        links["S5:6<->User1:3"].extend_metadata(
            {"reliability": 3, "bandwidth": 100, "delay": 60}
        )

        links["S6:3<->S9:1"].extend_metadata(
            {"reliability": 3, "bandwidth": 100, "delay": 60}
        )

        links["S6:4<->S9:2"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 62}
        )

        links["S6:5<->S10:1"].extend_metadata(
            {"bandwidth": 100, "delay": 108, "ownership": {"A": {}}}
        )

        links["S7:2<->S8:3"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 1}
        )

        links["S8:4<->S9:3"].extend_metadata(
            {"reliability": 3, "bandwidth": 100, "delay": 32}
        )

        links["S8:5<->S9:4"].extend_metadata(
            {"reliability": 3, "bandwidth": 100, "delay": 110}
        )

        links["S8:6<->S10:2"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "ownership": {"A": {}}}
        )

        links["S8:7<->S11:2"].extend_metadata(
            {"reliability": 3, "bandwidth": 100, "delay": 7}
        )

        links["S8:8<->User3:2"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 1}
        )

        links["S10:3<->User2:1"].extend_metadata(
            {
                "reliability": 3,
                "bandwidth": 100,
                "delay": 10,
                "ownership": {"A": {}},
            }
        )

        links["S11:3<->User2:2"].extend_metadata(
            {"reliability": 3, "bandwidth": 100, "delay": 6}
        )

        links["User1:4<->User4:3"].extend_metadata(
            {"reliability": 5, "bandwidth": 10, "delay": 105}
        )

    @staticmethod
    def _fill_links(links, interfaces):
        links["S1:1<->S2:1"] = Link(interfaces["S1:1"], interfaces["S2:1"])

        links["S1:2<->User1:1"] = Link(
            interfaces["S1:2"], interfaces["User1:1"]
        )

        links["S2:2<->User4:1"] = Link(
            interfaces["S2:2"], interfaces["User4:1"]
        )

        links["S3:1<->S5:1"] = Link(interfaces["S3:1"], interfaces["S5:1"])

        links["S3:2<->S7:1"] = Link(interfaces["S3:2"], interfaces["S7:1"])

        links["S3:3<->S8:1"] = Link(interfaces["S3:3"], interfaces["S8:1"])

        links["S3:4<->S11:1"] = Link(interfaces["S3:4"], interfaces["S11:1"])

        links["S3:5<->User3:1"] = Link(
            interfaces["S3:5"], interfaces["User3:1"]
        )

        links["S3:6<->User4:2"] = Link(
            interfaces["S3:6"], interfaces["User4:2"]
        )

        links["S4:1<->S5:2"] = Link(interfaces["S4:1"], interfaces["S5:2"])

        links["S4:2<->User1:2"] = Link(
            interfaces["S4:2"], interfaces["User1:2"]
        )

        links["S5:3<->S6:1"] = Link(interfaces["S5:3"], interfaces["S6:1"])

        links["S5:4<->S6:2"] = Link(interfaces["S5:4"], interfaces["S6:2"])

        links["S5:5<->S8:2"] = Link(interfaces["S5:5"], interfaces["S8:2"])

        links["S5:6<->User1:3"] = Link(
            interfaces["S5:6"], interfaces["User1:3"]
        )

        links["S6:3<->S9:1"] = Link(interfaces["S6:3"], interfaces["S9:1"])

        links["S6:4<->S9:2"] = Link(interfaces["S6:4"], interfaces["S9:2"])

        links["S6:5<->S10:1"] = Link(interfaces["S6:5"], interfaces["S10:1"])

        links["S7:2<->S8:3"] = Link(interfaces["S7:2"], interfaces["S8:3"])

        links["S8:4<->S9:3"] = Link(interfaces["S8:4"], interfaces["S9:3"])

        links["S8:5<->S9:4"] = Link(interfaces["S8:5"], interfaces["S9:4"])

        links["S8:6<->S10:2"] = Link(interfaces["S8:6"], interfaces["S10:2"])

        links["S8:7<->S11:2"] = Link(interfaces["S8:7"], interfaces["S11:2"])

        links["S8:8<->User3:2"] = Link(
            interfaces["S8:8"], interfaces["User3:2"]
        )

        links["S10:3<->User2:1"] = Link(
            interfaces["S10:3"], interfaces["User2:1"]
        )

        links["S11:3<->User2:2"] = Link(
            interfaces["S11:3"], interfaces["User2:2"]
        )

        links["User1:4<->User4:3"] = Link(
            interfaces["User1:4"], interfaces["User4:3"]
        )

        for link in links.values():
            link.enable()
            link.activate()
