from SilvaViridis.Python.LinuxAPI import USBDeviceManager

usb_tree = USBDeviceManager.build_usb_tree()

USBDeviceManager.print_usb_tree(usb_tree)
