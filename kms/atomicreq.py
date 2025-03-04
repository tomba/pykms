from __future__ import annotations

import ctypes
import fcntl
import itertools

import kms.uapi

__all__ = [ 'AtomicReq' ]

class AtomicReq:
    def __init__(self, card: kms.Card) -> None:
        self.card = card
        self.props = [] # (ob_id, prop_id, value)
        self.debug_print = False

    def commit(self, allow_modeset = False):
        flags = kms.uapi.DRM_MODE_PAGE_FLIP_EVENT | kms.uapi.DRM_MODE_ATOMIC_NONBLOCK

        if allow_modeset:
            flags |= kms.uapi.DRM_MODE_ATOMIC_ALLOW_MODESET

        self._commit(flags)

    def commit_sync(self, allow_modeset = False):
        flags = 0

        if allow_modeset:
            flags |= kms.uapi.DRM_MODE_ATOMIC_ALLOW_MODESET

        self._commit(flags)

    def _commit(self, flags):
        # Sort the list by object ID, then by property ID
        props = sorted(self.props, key=lambda tuple: (tuple[0], tuple[1]))

        if self.debug_print:
            for oid, g in itertools.groupby(props, lambda p: p[0]):
                ob = self.card.get_object(oid)
                print(ob)
                for _, pid, val in g:
                    prop_name = self.card.find_property_name(pid)

                    if prop_name in ['SRC_X', 'SRC_Y', 'SRC_W', 'SRC_H']:
                        disp_val = f'{val / 0x10000} ({val})'
                    else:
                        disp_val = str(val)

                    print(f'  {prop_name}({pid}) = {disp_val}')

        obj_prop_counts = {}
        for k, g in itertools.groupby(props, lambda p: p[0]):
            obj_prop_counts[k] = len(list(g))

        num_obs = len(obj_prop_counts)
        num_props = len(props)

        atomic = kms.uapi.struct_drm_mode_atomic()

        objs = (kms.uapi.c_uint32 * num_obs)()
        count_props = (kms.uapi.c_uint32 * num_obs)()
        prop_ids = (kms.uapi.c_uint32 * num_props)()
        prop_values = (kms.uapi.c_uint64 * num_props)()

        for idx,ob_id in enumerate(sorted(obj_prop_counts)):
            objs[idx] = ob_id
            count_props[idx] = obj_prop_counts[ob_id]

        for idx,p in enumerate(props):
            prop_id = p[1]
            prop_value = p[2]

            prop_ids[idx] = prop_id
            prop_values[idx] = prop_value

        atomic.count_objs = num_obs
        atomic.objs_ptr = ctypes.addressof(objs)
        atomic.count_props_ptr = ctypes.addressof(count_props)
        atomic.props_ptr = ctypes.addressof(prop_ids)
        atomic.prop_values_ptr = ctypes.addressof(prop_values)
        atomic.flags = flags

        pidx = 0
        for oidx, oid in enumerate(objs):
            prop_count = count_props[oidx]

            for _ in range(prop_count):
                prop_id = prop_ids[pidx]
                prop_value = prop_values[pidx]

                pidx += 1

        fcntl.ioctl(self.card.fd, kms.uapi.DRM_IOCTL_MODE_ATOMIC, atomic, True)

    def add_single(self, ob: kms.DrmPropObject | int, prop: str | int, value: int):
        if isinstance(ob, int):
            ob_id = ob
            ob = self.card.get_object(ob_id)
            assert(isinstance(ob, kms.DrmPropObject))
        elif isinstance(ob, kms.DrmPropObject):
            ob_id = ob.id
        else:
            raise RuntimeError('Bad object')

        if isinstance(prop, int):
            prop_id = prop
        elif isinstance(prop, str):
            prop_id = self.card.find_property_id(ob, prop)
        else:
            raise RuntimeError('Bad prop')

        self.props.append((ob_id, prop_id, value))

    def add_many(self, ob: kms.DrmPropObject | int, map: dict):
        for prop, value in map.items():
            self.add_single(ob, prop, value)

    def add(self, ob: kms.DrmPropObject | int, *argv):
        if len(argv) == 2:
            self.add_single(ob, *argv)
        elif len(argv) == 1:
            self.add_many(ob, *argv)
        else:
            raise RuntimeError('Bad add() call')

    def add_connector(self, connector: kms.Connector, crtc: kms.Crtc | None):
        self.add(connector.id, 'CRTC_ID', crtc.id if crtc else 0)

    def add_crtc(self, crtc: kms.Crtc, mode_blob: kms.Blob | None):
        if mode_blob:
            self.add(crtc.id, {'ACTIVE': 1, 'MODE_ID': mode_blob.id})
        else:
            self.add(crtc.id, {'ACTIVE': 0, 'MODE_ID': 0})

    def add_plane(self, plane: kms.Plane,
                  fb: kms.Framebuffer | None,
                  crtc: kms.Crtc | None,
                  src: tuple[int, int, int, int] | None=None,
                  dst: tuple[int, int, int, int] | None=None,
                  zpos: int | None=None,
                  params: dict | None=None):
        if not src and fb:
            src = (0, 0, fb.width, fb.height)

        if not dst:
            dst = src

        m = {'FB_ID': fb.id if fb else 0,
             'CRTC_ID': crtc.id if crtc else 0}

        if src is not None:
            src_x = int(round(src[0] * 0x10000))
            src_y = int(round(src[1] * 0x10000))
            src_w = int(round(src[2] * 0x10000))
            src_h = int(round(src[3] * 0x10000))

            m['SRC_X'] = src_x
            m['SRC_Y'] = src_y
            m['SRC_W'] = src_w
            m['SRC_H'] = src_h

        if dst is not None:
            crtc_x = int(round(dst[0]))
            crtc_y = int(round(dst[1]))
            crtc_w = int(round(dst[2]))
            crtc_h = int(round(dst[3]))

            m['CRTC_X'] = crtc_x
            m['CRTC_Y'] = crtc_y
            m['CRTC_W'] = crtc_w
            m['CRTC_H'] = crtc_h

        if zpos is not None:
            m['zpos'] = zpos

        if params:
            m.update(params)

        self.add(plane, m)

    @staticmethod
    def set_mode(connector: kms.Connector, crtc: kms.Crtc,
                 fb: kms.Framebuffer, mode: kms.VideoMode,
                 plane: kms.Plane | None=None):
        """Set up a pipeline with the connector and the CRTC,
        using the given mode and framebuffer. A suitable plane
        will be automatically selected, unless provided explicitly."""
        modeb = mode.to_blob(crtc.card)

        if not plane:
            plane = next(crtc.iter_planes(fb.format))

        req = kms.AtomicReq(crtc.card)

        req.add_connector(connector, crtc)
        req.add_crtc(crtc, modeb)
        req.add_plane(plane, fb, crtc, dst=(0, 0, mode.hdisplay, mode.vdisplay))

        req.commit_sync(allow_modeset = True)

    @staticmethod
    def disable_all(card: kms.Card):
        """Disable all connectors, CRTCs and planes"""
        req = kms.AtomicReq(card)

        for conn in card.connectors:
            req.add_connector(conn, None)

        for crtc in card.crtcs:
            req.add_crtc(crtc, None)

        for plane in card.planes:
            req.add_plane(plane, None, None)

        req.commit_sync(allow_modeset=True)
