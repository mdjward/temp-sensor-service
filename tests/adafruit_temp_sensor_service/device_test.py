from unittest import TestCase
from Adafruit_DHT import platform_detect as platform
from unittest_data_provider import data_provider
from adafruit_temp_sensor_service.device import *
from typing import Callable

class DeviceTest(TestCase):

    provideRaspberryPiExamples = lambda: (
        [lambda: platform.RASPBERRY_PI, lambda: 1, lambda: 1],
        [lambda: platform.RASPBERRY_PI, lambda: 1, lambda: 2],
        [lambda: platform.RASPBERRY_PI, lambda: 1, lambda: 3],
        [lambda: platform.RASPBERRY_PI, lambda: 1, lambda: 1],
        [lambda: platform.RASPBERRY_PI, lambda: 2, lambda: 2],
        [lambda: platform.RASPBERRY_PI, lambda: 2, lambda: 3],
    )

    @data_provider(provideRaspberryPiExamples)
    def test_it_will_accept_a_reported_raspberry_pi(self, platform_detector:Callable, revision_detector:Callable, version_detector:Callable):
        expected_revision = revision_detector()
        expected_version = version_detector()

        device = Device.detect(platform_detector=platform_detector, revision_detector=revision_detector, version_detector=version_detector)
        self.assertTrue(isinstance(device, RaspberryPiDevice))
        self.assertEqual(expected_revision, device.getRevision())
        self.assertEqual(expected_version, device.getVersion())
    
    def test_it_will_accept_a_reported_beaglebone_black(self):
        self.assertTrue(isinstance(Device.detect(platform_detector=lambda: platform.BEAGLEBONE_BLACK), BeagleboneBlackDevice))

    def test_it_will_raise_an_undetectable_device_error(self):
        self.assertRaises(UnknownDeviceException, Device.detect, platform_detector=lambda: platform.UNKNOWN)



class DeviceFullIntegrationTest(TestCase):

    def test_it_will_detect_a_raspberry_pi(self):
        if platform.platform_detect() != platform.RASPBERRY_PI:
            self.skipTest("Raspberry Pi detection can only be tested on a Raspberry Pi device");

        expected_revision = platform.pi_revision()
        expected_version = platform.pi_version()

        device = Device.detect()
        self.assertTrue(isinstance(device, RaspberryPiDevice))
        self.assertEqual(expected_revision, device.getRevision())
        self.assertEqual(expected_version, device.getVersion())

    def test_it_will_detect_a_beaglebone_black(self):
        if platform.platform_detect() != platform.BEAGLEBONE_BLACK:
            self.skipTest("Beaglebone Black detection can only be tested on a Beaglebone Black device");

    def test_it_will_raise_an_exception_for_unknown(self):
        if platform.platform_detect() == platform.RASPBERRY_PI:
            self.skipTest("Unknown device detection cannot be tested on a Raspberry Pi device");
        if platform.platform_detect() == platform.BEAGLEBONE_BLACK:
            self.skipTest("Unknown device detection cannot be tested on a Beaglebone Black device");

        self.assertRaises(UnknownDeviceException, Device.detect)



class RaspberryPiDeviceTest(TestCase):

    invalidRevisions = lambda: [ [-1], [0], [3]]
    invalidVersions = lambda: [ [-1], [0], [4]]

    def test_it_will_return_correct_platform_identifier(self):
        self.assertEqual(platform.RASPBERRY_PI, RaspberryPiDevice(2, 3).getIdentifier())

    def test_it_will_return_device_info(self):
        deviceInfo = RaspberryPiDevice(2, 3).getDeviceInfo()

        self.assertEqual("Raspberry Pi", deviceInfo["name"])
        self.assertEqual(2, deviceInfo["revision"])
        self.assertEqual(3, deviceInfo["version"])

    @data_provider(invalidRevisions)
    def test_it_will_raise_a_value_error_for_invalid_revision(self, revision):
        with self.assertRaises(ValueError):
            RaspberryPiDevice(revision, 3)

    @data_provider(invalidVersions)
    def test_it_will_raise_a_value_error_for_invalid_version(self, version):
        with self.assertRaises(ValueError):
            RaspberryPiDevice(2, version)



class BeagleboneBlackDeviceTest(TestCase):

    def test_it_will_return_correct_platform_identifier(self):
        self.assertEqual(platform.BEAGLEBONE_BLACK, BeagleboneBlackDevice().getIdentifier())

    def test_it_will_return_device_info(self):
        self.assertEqual("Beaglebone Black", BeagleboneBlackDevice().getDeviceInfo()["name"])
