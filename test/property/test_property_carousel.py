from unittest import TestCase
from unittest.mock import Mock
from owrx.property import PropertyCarousel, PropertyLayer, PropertyDeleted


class PropertyCarouselTest(TestCase):
    def testInitiallyEmpty(self):
        pc = PropertyCarousel()
        with self.assertRaises(KeyError):
            x = pc["testkey"]

    def testPropertyAccess(self):
        pc = PropertyCarousel()
        pl = PropertyLayer(testkey="testvalue")
        pc.addLayer("test", pl)
        pc.switch("test")
        self.assertEqual(pc["testkey"], "testvalue")

    def testWriteAccess(self):
        pc = PropertyCarousel()
        pl = PropertyLayer(testkey="old_value")
        pc.addLayer("test", pl)
        pc.switch("test")
        pc["testkey"] = "new_value"
        self.assertEqual(pc["testkey"], "new_value")
        self.assertEqual(pl["testkey"], "new_value")

    def testForwardsEvents(self):
        pc = PropertyCarousel()
        pl = PropertyLayer(testkey="old_value")
        pc.addLayer("test", pl)
        pc.switch("test")
        mock = Mock()
        pc.wire(mock.method)
        pc["testkey"] = "new_value"
        mock.method.assert_called_once_with({"testkey": "new_value"})

    def testStopsForwardingAfterSwitch(self):
        pc = PropertyCarousel()
        pl_x = PropertyLayer(testkey="old_value")
        pc.addLayer("x", pl_x)
        pl_y = PropertyLayer(testkey="new_value")
        pc.addLayer("y", pl_y)
        pc.switch("x")
        pc.switch("y")
        mock = Mock()
        pc.wire(mock.method)
        pl_x["testkey"] = "new_value"
        mock.method.assert_not_called()

    def testEventsOnSwitch(self):
        pc = PropertyCarousel()
        pl_x = PropertyLayer(old_key="old_value")
        pc.addLayer("x", pl_x)
        pl_y = PropertyLayer(new_key="new_value")
        pc.addLayer("y", pl_y)
        pc.switch("x")
        mock = Mock()
        pc.wire(mock.method)
        pc.switch("y")
        mock.method.assert_called_once_with({"old_key": PropertyDeleted, "new_key": "new_value"})

    def testNoEventsIfKeysDontChange(self):
        pc = PropertyCarousel()
        pl_x = PropertyLayer(testkey="same_value")
        pc.addLayer("x", pl_x)
        pl_y = PropertyLayer(testkey="same_value")
        pc.addLayer("y", pl_y)
        pc.switch("x")
        mock = Mock()
        pc.wire(mock.method)
        pc.switch("y")
        mock.method.assert_not_called()

    def testKeyErrorOnInvalidSwitch(self):
        pc = PropertyCarousel()
        with self.assertRaises(KeyError):
            pc.switch("doesntmatter")