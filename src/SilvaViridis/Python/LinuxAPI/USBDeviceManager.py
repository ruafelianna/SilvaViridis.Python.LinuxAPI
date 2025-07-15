from __future__ import annotations

from dataclasses import dataclass, field
from pyudev import Context, DeviceNotFoundAtPathError, Device, Devices

@dataclass
class DeviceBase:
    data : Device

@dataclass
class USBHostController(DeviceBase):
    pass

@dataclass
class USBHub(DeviceBase):
    pass

@dataclass
class USBPort(DeviceBase):
    index : int

@dataclass
class USBDevice(DeviceBase):
    pass

@dataclass
class USBNode:
    parent : USBNode | None
    device : USBHostController | USBHub | USBPort | USBDevice
    children : list[USBNode] = field(default_factory = list["USBNode"])

def build_usb_tree(
) -> list[USBNode]:
    usb_tree : list[USBNode] = []

    context = Context()

    usb_devs = [
        dev
        for dev in context.list_devices(subsystem = "usb")
        if dev.device_type is not None and dev.device_type == "usb_device"
    ]

    def enumerate_children(parent : USBNode):
        if not isinstance(parent.device, USBHub):
            return

        children = list(parent.device.data.children)

        parent_interface = next(
            (child for child in children if child.device_type == "usb_interface"),
            None,
        )

        if parent_interface is None:
            return

        ports_num = parent.device.data.attributes.get("maxchild")
        ports_num = 0 if ports_num is None or not isinstance(ports_num, str | bytes) else int(ports_num)

        for i in range(ports_num):
            port_path = f"{parent_interface.sys_path}/{parent.device.data.sys_name}-port{i + 1}"
            port_device = Devices.from_path(context, port_path)

            port_node = USBNode(
                parent = parent,
                device = USBPort(
                    data = port_device,
                    index = i + 1,
                )
            )

            try:
                conn_device = Devices.from_path(context, f"{port_path}/device")
            except DeviceNotFoundAtPathError:
                conn_device = None

            if conn_device is not None:
                dev_class = conn_device.attributes.get("bDeviceClass", b"-")

                is_hub = dev_class == b"09"

                if is_hub:
                    device = USBHub(
                        data = conn_device,
                    )
                else:
                    device = USBDevice(
                        data = conn_device,
                    )

                device_node = USBNode(
                    parent = port_node,
                    device = device,
                )

                if is_hub:
                    enumerate_children(device_node)

                port_node.children.append(device_node)

            parent.children.append(port_node)

    for dev in usb_devs:
        usb_parent = dev.find_parent("usb")

        if usb_parent is None:
            pci_parent = dev.find_parent("pci")

            if pci_parent is not None:
                hc_node = USBNode(
                    parent = None,
                    device = USBHostController(
                        data = pci_parent,
                    )
                )

                hub_node = USBNode(
                    parent = hc_node,
                    device = USBHub(
                        data = dev,
                    ),
                )

                enumerate_children(hub_node)
                hc_node.children.append(hub_node)
                usb_tree.append(hc_node)

    return usb_tree

def print_usb_tree(usb_tree : list[USBNode], level : int = 0):
    for node in usb_tree:
        manufacturer = node.device.data.attributes.get("manufacturer")
        product = node.device.data.attributes.get("product")

        join = "" if manufacturer is None or product is None else ", "
        open = "" if manufacturer is None and product is None else " ("
        close = "" if manufacturer is None and product is None else ")"

        manufacturer = "" if manufacturer is None or not isinstance(manufacturer, bytes) else manufacturer.decode()
        product = "" if product is None or not isinstance(product, bytes) else product.decode()

        print(f"{"  " * level}[{type(node.device).__name__}] {node.device.data.sys_name}{open}{product}{join}{manufacturer}{close}")
        print_usb_tree(node.children, level + 1)
