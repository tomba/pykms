from __future__ import annotations

import kms.uapi

__all__ = ['ResourceManager']


class ResourceManager:
    def __init__(self, card: kms.Card) -> None:
        self.card = card
        self.reserved_connectors = set()
        self.reserved_crtcs = set()
        self.reserved_planes = set()

    def find_connector(self):
        for c in self.card.connectors:
            if not c.connected:
                continue

            if c in self.reserved_connectors:
                continue

            return c

        raise RuntimeError('Available connector not found')

    def resolve_connector(self, name: str):
        if name.startswith('@'):
            id = int(name[1:])
            conn = self.card.get_connector(id)

            if conn in self.reserved_connectors:
                raise RuntimeError('Connector already reserved')

            return conn

        try:
            idx = int(name)
        except ValueError:
            pass
        else:
            if idx >= len(self.card.connectors):
                raise RuntimeError('Connector idx too high')

            conn = self.card.connectors[idx]

            if conn in self.reserved_connectors:
                raise RuntimeError('Connector already reserved')

            return conn

        name = name.lower()

        for c in self.card.connectors:
            if name not in c.fullname.lower():
                continue

            if c in self.reserved_connectors:
                raise RuntimeError('Connector already reserved')

            return c

        raise RuntimeError(f"Connector '{name}' not found")

    def reserve_connector(self, name=''):
        if not name:
            conn = self.find_connector()
        else:
            conn = self.resolve_connector(name)

        self.reserved_connectors.add(conn)

        return conn

    def reserve_crtc(self, connector: kms.Connector):
        crtc = connector.current_crtc

        if crtc and crtc not in self.reserved_crtcs:
            self.reserved_crtcs.add(crtc)
            return crtc

        for crtc in connector.possible_crtcs:
            if crtc not in self.reserved_crtcs:
                self.reserved_crtcs.add(crtc)
                return crtc

        raise RuntimeError('Crtc not found')

    def reserve_plane(self, crtc: kms.Crtc, format: kms.PixelFormat | None = None, plane_type=None):
        for plane in crtc.iter_planes(format, plane_type):
            if plane in self.reserved_planes:
                continue

            self.reserved_planes.add(plane)

            return plane

        raise RuntimeError('Plane not found')

    # Deprecated
    def reserve_generic_plane(self, crtc: kms.Crtc, format: kms.PixelFormat | None = None):
        return self.reserve_plane(crtc, format)

    # Deprecated
    def reserve_primary_plane(self, crtc: kms.Crtc, format: kms.PixelFormat | None = None):
        return self.reserve_plane(crtc, format, kms.PlaneType.PRIMARY)

    # Deprecated
    def reserve_overlay_plane(self, crtc: kms.Crtc, format: kms.PixelFormat | None = None):
        return self.reserve_plane(crtc, format, kms.PlaneType.OVERLAY)
