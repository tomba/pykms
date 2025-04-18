r"""Wrapper for drm.h

Generated with:
ctypesgen --no-embed-preamble --no-macro-try-except --no-source-comments -D__volatile__= -D__signed__= -U__SIZEOF_INT128__ -I/usr/include -okms/uapi/kms.py /usr/include/drm/drm.h /usr/include/drm/drm_mode.h /usr/include/drm/drm_fourcc.h

Do not modify this file.
"""

__docformat__ = 'restructuredtext'

# Begin preamble for Python

from .ctypes_preamble import *
from .ctypes_preamble import _variadic_function

# End preamble

# No libraries

# No modules

__u8 = c_ubyte

__u16 = c_ushort

__s32 = c_int

__u32 = c_uint

__s64 = c_longlong

__u64 = c_ulonglong

__kernel_ulong_t = c_ulong

__kernel_size_t = __kernel_ulong_t

drm_handle_t = c_uint

drm_context_t = c_uint

drm_drawable_t = c_uint

drm_magic_t = c_uint


class struct_drm_clip_rect(Structure):
    pass

struct_drm_clip_rect.__slots__ = [
    'x1',
    'y1',
    'x2',
    'y2',
]
struct_drm_clip_rect._fields_ = [
    ('x1', c_ushort),
    ('y1', c_ushort),
    ('x2', c_ushort),
    ('y2', c_ushort),
]


class struct_drm_drawable_info(Structure):
    pass

struct_drm_drawable_info.__slots__ = [
    'num_rects',
    'rects',
]
struct_drm_drawable_info._fields_ = [
    ('num_rects', c_uint),
    ('rects', POINTER(struct_drm_clip_rect)),
]


class struct_drm_tex_region(Structure):
    pass

struct_drm_tex_region.__slots__ = [
    'next',
    'prev',
    'in_use',
    'padding',
    'age',
]
struct_drm_tex_region._fields_ = [
    ('next', c_ubyte),
    ('prev', c_ubyte),
    ('in_use', c_ubyte),
    ('padding', c_ubyte),
    ('age', c_uint),
]


class struct_drm_hw_lock(Structure):
    pass

struct_drm_hw_lock.__slots__ = [
    'lock',
    'padding',
]
struct_drm_hw_lock._fields_ = [
    ('lock', c_uint),
    ('padding', c_char * int(60)),
]


class struct_drm_version(Structure):
    pass

struct_drm_version.__slots__ = [
    'version_major',
    'version_minor',
    'version_patchlevel',
    'name_len',
    'name',
    'date_len',
    'date',
    'desc_len',
    'desc',
]
struct_drm_version._fields_ = [
    ('version_major', c_int),
    ('version_minor', c_int),
    ('version_patchlevel', c_int),
    ('name_len', __kernel_size_t),
    ('name', String),
    ('date_len', __kernel_size_t),
    ('date', String),
    ('desc_len', __kernel_size_t),
    ('desc', String),
]


class struct_drm_unique(Structure):
    pass

struct_drm_unique.__slots__ = [
    'unique_len',
    'unique',
]
struct_drm_unique._fields_ = [
    ('unique_len', __kernel_size_t),
    ('unique', String),
]


class struct_drm_list(Structure):
    pass

struct_drm_list.__slots__ = [
    'count',
    'version',
]
struct_drm_list._fields_ = [
    ('count', c_int),
    ('version', POINTER(struct_drm_version)),
]


class struct_drm_block(Structure):
    pass

struct_drm_block.__slots__ = [
    'unused',
]
struct_drm_block._fields_ = [
    ('unused', c_int),
]

enum_anon_3 = c_int

DRM_ADD_COMMAND = 0

DRM_RM_COMMAND = (DRM_ADD_COMMAND + 1)

DRM_INST_HANDLER = (DRM_RM_COMMAND + 1)

DRM_UNINST_HANDLER = (DRM_INST_HANDLER + 1)


class struct_drm_control(Structure):
    pass

struct_drm_control.__slots__ = [
    'func',
    'irq',
]
struct_drm_control._fields_ = [
    ('func', enum_anon_3),
    ('irq', c_int),
]

enum_drm_map_type = c_int

_DRM_FRAME_BUFFER = 0

_DRM_REGISTERS = 1

_DRM_SHM = 2

_DRM_AGP = 3

_DRM_SCATTER_GATHER = 4

_DRM_CONSISTENT = 5

enum_drm_map_flags = c_int

_DRM_RESTRICTED = 0x01

_DRM_READ_ONLY = 0x02

_DRM_LOCKED = 0x04

_DRM_KERNEL = 0x08

_DRM_WRITE_COMBINING = 0x10

_DRM_CONTAINS_LOCK = 0x20

_DRM_REMOVABLE = 0x40

_DRM_DRIVER = 0x80


class struct_drm_ctx_priv_map(Structure):
    pass

struct_drm_ctx_priv_map.__slots__ = [
    'ctx_id',
    'handle',
]
struct_drm_ctx_priv_map._fields_ = [
    ('ctx_id', c_uint),
    ('handle', POINTER(None)),
]


class struct_drm_map(Structure):
    pass

struct_drm_map.__slots__ = [
    'offset',
    'size',
    'type',
    'flags',
    'handle',
    'mtrr',
]
struct_drm_map._fields_ = [
    ('offset', c_ulong),
    ('size', c_ulong),
    ('type', enum_drm_map_type),
    ('flags', enum_drm_map_flags),
    ('handle', POINTER(None)),
    ('mtrr', c_int),
]


class struct_drm_client(Structure):
    pass

struct_drm_client.__slots__ = [
    'idx',
    'auth',
    'pid',
    'uid',
    'magic',
    'iocs',
]
struct_drm_client._fields_ = [
    ('idx', c_int),
    ('auth', c_int),
    ('pid', c_ulong),
    ('uid', c_ulong),
    ('magic', c_ulong),
    ('iocs', c_ulong),
]

enum_drm_stat_type = c_int

_DRM_STAT_LOCK = 0

_DRM_STAT_OPENS = (_DRM_STAT_LOCK + 1)

_DRM_STAT_CLOSES = (_DRM_STAT_OPENS + 1)

_DRM_STAT_IOCTLS = (_DRM_STAT_CLOSES + 1)

_DRM_STAT_LOCKS = (_DRM_STAT_IOCTLS + 1)

_DRM_STAT_UNLOCKS = (_DRM_STAT_LOCKS + 1)

_DRM_STAT_VALUE = (_DRM_STAT_UNLOCKS + 1)

_DRM_STAT_BYTE = (_DRM_STAT_VALUE + 1)

_DRM_STAT_COUNT = (_DRM_STAT_BYTE + 1)

_DRM_STAT_IRQ = (_DRM_STAT_COUNT + 1)

_DRM_STAT_PRIMARY = (_DRM_STAT_IRQ + 1)

_DRM_STAT_SECONDARY = (_DRM_STAT_PRIMARY + 1)

_DRM_STAT_DMA = (_DRM_STAT_SECONDARY + 1)

_DRM_STAT_SPECIAL = (_DRM_STAT_DMA + 1)

_DRM_STAT_MISSED = (_DRM_STAT_SPECIAL + 1)


class struct_anon_4(Structure):
    pass

struct_anon_4.__slots__ = [
    'value',
    'type',
]
struct_anon_4._fields_ = [
    ('value', c_ulong),
    ('type', enum_drm_stat_type),
]


class struct_drm_stats(Structure):
    pass

struct_drm_stats.__slots__ = [
    'count',
    'data',
]
struct_drm_stats._fields_ = [
    ('count', c_ulong),
    ('data', struct_anon_4 * int(15)),
]

enum_drm_lock_flags = c_int

_DRM_LOCK_READY = 0x01

_DRM_LOCK_QUIESCENT = 0x02

_DRM_LOCK_FLUSH = 0x04

_DRM_LOCK_FLUSH_ALL = 0x08

_DRM_HALT_ALL_QUEUES = 0x10

_DRM_HALT_CUR_QUEUES = 0x20


class struct_drm_lock(Structure):
    pass

struct_drm_lock.__slots__ = [
    'context',
    'flags',
]
struct_drm_lock._fields_ = [
    ('context', c_int),
    ('flags', enum_drm_lock_flags),
]

enum_drm_dma_flags = c_int

_DRM_DMA_BLOCK = 0x01

_DRM_DMA_WHILE_LOCKED = 0x02

_DRM_DMA_PRIORITY = 0x04

_DRM_DMA_WAIT = 0x10

_DRM_DMA_SMALLER_OK = 0x20

_DRM_DMA_LARGER_OK = 0x40

enum_anon_5 = c_int

_DRM_PAGE_ALIGN = 0x01

_DRM_AGP_BUFFER = 0x02

_DRM_SG_BUFFER = 0x04

_DRM_FB_BUFFER = 0x08

_DRM_PCI_BUFFER_RO = 0x10


class struct_drm_buf_desc(Structure):
    pass

struct_drm_buf_desc.__slots__ = [
    'count',
    'size',
    'low_mark',
    'high_mark',
    'flags',
    'agp_start',
]
struct_drm_buf_desc._fields_ = [
    ('count', c_int),
    ('size', c_int),
    ('low_mark', c_int),
    ('high_mark', c_int),
    ('flags', enum_anon_5),
    ('agp_start', c_ulong),
]


class struct_drm_buf_info(Structure):
    pass

struct_drm_buf_info.__slots__ = [
    'count',
    'list',
]
struct_drm_buf_info._fields_ = [
    ('count', c_int),
    ('list', POINTER(struct_drm_buf_desc)),
]


class struct_drm_buf_free(Structure):
    pass

struct_drm_buf_free.__slots__ = [
    'count',
    'list',
]
struct_drm_buf_free._fields_ = [
    ('count', c_int),
    ('list', POINTER(c_int)),
]


class struct_drm_buf_pub(Structure):
    pass

struct_drm_buf_pub.__slots__ = [
    'idx',
    'total',
    'used',
    'address',
]
struct_drm_buf_pub._fields_ = [
    ('idx', c_int),
    ('total', c_int),
    ('used', c_int),
    ('address', POINTER(None)),
]


class struct_drm_buf_map(Structure):
    pass

struct_drm_buf_map.__slots__ = [
    'count',
    'virtual',
    'list',
]
struct_drm_buf_map._fields_ = [
    ('count', c_int),
    ('virtual', POINTER(None)),
    ('list', POINTER(struct_drm_buf_pub)),
]


class struct_drm_dma(Structure):
    pass

struct_drm_dma.__slots__ = [
    'context',
    'send_count',
    'send_indices',
    'send_sizes',
    'flags',
    'request_count',
    'request_size',
    'request_indices',
    'request_sizes',
    'granted_count',
]
struct_drm_dma._fields_ = [
    ('context', c_int),
    ('send_count', c_int),
    ('send_indices', POINTER(c_int)),
    ('send_sizes', POINTER(c_int)),
    ('flags', enum_drm_dma_flags),
    ('request_count', c_int),
    ('request_size', c_int),
    ('request_indices', POINTER(c_int)),
    ('request_sizes', POINTER(c_int)),
    ('granted_count', c_int),
]

enum_drm_ctx_flags = c_int

_DRM_CONTEXT_PRESERVED = 0x01

_DRM_CONTEXT_2DONLY = 0x02


class struct_drm_ctx(Structure):
    pass

struct_drm_ctx.__slots__ = [
    'handle',
    'flags',
]
struct_drm_ctx._fields_ = [
    ('handle', drm_context_t),
    ('flags', enum_drm_ctx_flags),
]


class struct_drm_ctx_res(Structure):
    pass

struct_drm_ctx_res.__slots__ = [
    'count',
    'contexts',
]
struct_drm_ctx_res._fields_ = [
    ('count', c_int),
    ('contexts', POINTER(struct_drm_ctx)),
]


class struct_drm_draw(Structure):
    pass

struct_drm_draw.__slots__ = [
    'handle',
]
struct_drm_draw._fields_ = [
    ('handle', drm_drawable_t),
]

enum_anon_6 = c_int

DRM_DRAWABLE_CLIPRECTS = 0

drm_drawable_info_type_t = enum_anon_6


class struct_drm_update_draw(Structure):
    pass

struct_drm_update_draw.__slots__ = [
    'handle',
    'type',
    'num',
    'data',
]
struct_drm_update_draw._fields_ = [
    ('handle', drm_drawable_t),
    ('type', c_uint),
    ('num', c_uint),
    ('data', c_ulonglong),
]


class struct_drm_auth(Structure):
    pass

struct_drm_auth.__slots__ = [
    'magic',
]
struct_drm_auth._fields_ = [
    ('magic', drm_magic_t),
]


class struct_drm_irq_busid(Structure):
    pass

struct_drm_irq_busid.__slots__ = [
    'irq',
    'busnum',
    'devnum',
    'funcnum',
]
struct_drm_irq_busid._fields_ = [
    ('irq', c_int),
    ('busnum', c_int),
    ('devnum', c_int),
    ('funcnum', c_int),
]

enum_drm_vblank_seq_type = c_int

_DRM_VBLANK_ABSOLUTE = 0x0

_DRM_VBLANK_RELATIVE = 0x1

_DRM_VBLANK_HIGH_CRTC_MASK = 0x0000003e

_DRM_VBLANK_EVENT = 0x4000000

_DRM_VBLANK_FLIP = 0x8000000

_DRM_VBLANK_NEXTONMISS = 0x10000000

_DRM_VBLANK_SECONDARY = 0x20000000

_DRM_VBLANK_SIGNAL = 0x40000000


class struct_drm_wait_vblank_request(Structure):
    pass

struct_drm_wait_vblank_request.__slots__ = [
    'type',
    'sequence',
    'signal',
]
struct_drm_wait_vblank_request._fields_ = [
    ('type', enum_drm_vblank_seq_type),
    ('sequence', c_uint),
    ('signal', c_ulong),
]


class struct_drm_wait_vblank_reply(Structure):
    pass

struct_drm_wait_vblank_reply.__slots__ = [
    'type',
    'sequence',
    'tval_sec',
    'tval_usec',
]
struct_drm_wait_vblank_reply._fields_ = [
    ('type', enum_drm_vblank_seq_type),
    ('sequence', c_uint),
    ('tval_sec', c_long),
    ('tval_usec', c_long),
]


class union_drm_wait_vblank(Union):
    pass

union_drm_wait_vblank.__slots__ = [
    'request',
    'reply',
]
union_drm_wait_vblank._fields_ = [
    ('request', struct_drm_wait_vblank_request),
    ('reply', struct_drm_wait_vblank_reply),
]


class struct_drm_modeset_ctl(Structure):
    pass

struct_drm_modeset_ctl.__slots__ = [
    'crtc',
    'cmd',
]
struct_drm_modeset_ctl._fields_ = [
    ('crtc', __u32),
    ('cmd', __u32),
]


class struct_drm_agp_mode(Structure):
    pass

struct_drm_agp_mode.__slots__ = [
    'mode',
]
struct_drm_agp_mode._fields_ = [
    ('mode', c_ulong),
]


class struct_drm_agp_buffer(Structure):
    pass

struct_drm_agp_buffer.__slots__ = [
    'size',
    'handle',
    'type',
    'physical',
]
struct_drm_agp_buffer._fields_ = [
    ('size', c_ulong),
    ('handle', c_ulong),
    ('type', c_ulong),
    ('physical', c_ulong),
]


class struct_drm_agp_binding(Structure):
    pass

struct_drm_agp_binding.__slots__ = [
    'handle',
    'offset',
]
struct_drm_agp_binding._fields_ = [
    ('handle', c_ulong),
    ('offset', c_ulong),
]


class struct_drm_agp_info(Structure):
    pass

struct_drm_agp_info.__slots__ = [
    'agp_version_major',
    'agp_version_minor',
    'mode',
    'aperture_base',
    'aperture_size',
    'memory_allowed',
    'memory_used',
    'id_vendor',
    'id_device',
]
struct_drm_agp_info._fields_ = [
    ('agp_version_major', c_int),
    ('agp_version_minor', c_int),
    ('mode', c_ulong),
    ('aperture_base', c_ulong),
    ('aperture_size', c_ulong),
    ('memory_allowed', c_ulong),
    ('memory_used', c_ulong),
    ('id_vendor', c_ushort),
    ('id_device', c_ushort),
]


class struct_drm_scatter_gather(Structure):
    pass

struct_drm_scatter_gather.__slots__ = [
    'size',
    'handle',
]
struct_drm_scatter_gather._fields_ = [
    ('size', c_ulong),
    ('handle', c_ulong),
]


class struct_drm_set_version(Structure):
    pass

struct_drm_set_version.__slots__ = [
    'drm_di_major',
    'drm_di_minor',
    'drm_dd_major',
    'drm_dd_minor',
]
struct_drm_set_version._fields_ = [
    ('drm_di_major', c_int),
    ('drm_di_minor', c_int),
    ('drm_dd_major', c_int),
    ('drm_dd_minor', c_int),
]


class struct_drm_gem_close(Structure):
    pass

struct_drm_gem_close.__slots__ = [
    'handle',
    'pad',
]
struct_drm_gem_close._fields_ = [
    ('handle', __u32),
    ('pad', __u32),
]


class struct_drm_gem_flink(Structure):
    pass

struct_drm_gem_flink.__slots__ = [
    'handle',
    'name',
]
struct_drm_gem_flink._fields_ = [
    ('handle', __u32),
    ('name', __u32),
]


class struct_drm_gem_open(Structure):
    pass

struct_drm_gem_open.__slots__ = [
    'name',
    'handle',
    'size',
]
struct_drm_gem_open._fields_ = [
    ('name', __u32),
    ('handle', __u32),
    ('size', __u64),
]


class struct_drm_get_cap(Structure):
    pass

struct_drm_get_cap.__slots__ = [
    'capability',
    'value',
]
struct_drm_get_cap._fields_ = [
    ('capability', __u64),
    ('value', __u64),
]


class struct_drm_set_client_cap(Structure):
    pass

struct_drm_set_client_cap.__slots__ = [
    'capability',
    'value',
]
struct_drm_set_client_cap._fields_ = [
    ('capability', __u64),
    ('value', __u64),
]


class struct_drm_prime_handle(Structure):
    pass

struct_drm_prime_handle.__slots__ = [
    'handle',
    'flags',
    'fd',
]
struct_drm_prime_handle._fields_ = [
    ('handle', __u32),
    ('flags', __u32),
    ('fd', __s32),
]


class struct_drm_syncobj_create(Structure):
    pass

struct_drm_syncobj_create.__slots__ = [
    'handle',
    'flags',
]
struct_drm_syncobj_create._fields_ = [
    ('handle', __u32),
    ('flags', __u32),
]


class struct_drm_syncobj_destroy(Structure):
    pass

struct_drm_syncobj_destroy.__slots__ = [
    'handle',
    'pad',
]
struct_drm_syncobj_destroy._fields_ = [
    ('handle', __u32),
    ('pad', __u32),
]


class struct_drm_syncobj_handle(Structure):
    pass

struct_drm_syncobj_handle.__slots__ = [
    'handle',
    'flags',
    'fd',
    'pad',
]
struct_drm_syncobj_handle._fields_ = [
    ('handle', __u32),
    ('flags', __u32),
    ('fd', __s32),
    ('pad', __u32),
]


class struct_drm_syncobj_transfer(Structure):
    pass

struct_drm_syncobj_transfer.__slots__ = [
    'src_handle',
    'dst_handle',
    'src_point',
    'dst_point',
    'flags',
    'pad',
]
struct_drm_syncobj_transfer._fields_ = [
    ('src_handle', __u32),
    ('dst_handle', __u32),
    ('src_point', __u64),
    ('dst_point', __u64),
    ('flags', __u32),
    ('pad', __u32),
]


class struct_drm_syncobj_wait(Structure):
    pass

struct_drm_syncobj_wait.__slots__ = [
    'handles',
    'timeout_nsec',
    'count_handles',
    'flags',
    'first_signaled',
    'pad',
]
struct_drm_syncobj_wait._fields_ = [
    ('handles', __u64),
    ('timeout_nsec', __s64),
    ('count_handles', __u32),
    ('flags', __u32),
    ('first_signaled', __u32),
    ('pad', __u32),
]


class struct_drm_syncobj_timeline_wait(Structure):
    pass

struct_drm_syncobj_timeline_wait.__slots__ = [
    'handles',
    'points',
    'timeout_nsec',
    'count_handles',
    'flags',
    'first_signaled',
    'pad',
]
struct_drm_syncobj_timeline_wait._fields_ = [
    ('handles', __u64),
    ('points', __u64),
    ('timeout_nsec', __s64),
    ('count_handles', __u32),
    ('flags', __u32),
    ('first_signaled', __u32),
    ('pad', __u32),
]


class struct_drm_syncobj_array(Structure):
    pass

struct_drm_syncobj_array.__slots__ = [
    'handles',
    'count_handles',
    'pad',
]
struct_drm_syncobj_array._fields_ = [
    ('handles', __u64),
    ('count_handles', __u32),
    ('pad', __u32),
]


class struct_drm_syncobj_timeline_array(Structure):
    pass

struct_drm_syncobj_timeline_array.__slots__ = [
    'handles',
    'points',
    'count_handles',
    'flags',
]
struct_drm_syncobj_timeline_array._fields_ = [
    ('handles', __u64),
    ('points', __u64),
    ('count_handles', __u32),
    ('flags', __u32),
]


class struct_drm_crtc_get_sequence(Structure):
    pass

struct_drm_crtc_get_sequence.__slots__ = [
    'crtc_id',
    'active',
    'sequence',
    'sequence_ns',
]
struct_drm_crtc_get_sequence._fields_ = [
    ('crtc_id', __u32),
    ('active', __u32),
    ('sequence', __u64),
    ('sequence_ns', __s64),
]


class struct_drm_crtc_queue_sequence(Structure):
    pass

struct_drm_crtc_queue_sequence.__slots__ = [
    'crtc_id',
    'flags',
    'sequence',
    'user_data',
]
struct_drm_crtc_queue_sequence._fields_ = [
    ('crtc_id', __u32),
    ('flags', __u32),
    ('sequence', __u64),
    ('user_data', __u64),
]


class struct_drm_mode_modeinfo(Structure):
    pass

struct_drm_mode_modeinfo.__slots__ = [
    'clock',
    'hdisplay',
    'hsync_start',
    'hsync_end',
    'htotal',
    'hskew',
    'vdisplay',
    'vsync_start',
    'vsync_end',
    'vtotal',
    'vscan',
    'vrefresh',
    'flags',
    'type',
    'name',
]
struct_drm_mode_modeinfo._fields_ = [
    ('clock', __u32),
    ('hdisplay', __u16),
    ('hsync_start', __u16),
    ('hsync_end', __u16),
    ('htotal', __u16),
    ('hskew', __u16),
    ('vdisplay', __u16),
    ('vsync_start', __u16),
    ('vsync_end', __u16),
    ('vtotal', __u16),
    ('vscan', __u16),
    ('vrefresh', __u32),
    ('flags', __u32),
    ('type', __u32),
    ('name', c_char * int(32)),
]


class struct_drm_mode_card_res(Structure):
    pass

struct_drm_mode_card_res.__slots__ = [
    'fb_id_ptr',
    'crtc_id_ptr',
    'connector_id_ptr',
    'encoder_id_ptr',
    'count_fbs',
    'count_crtcs',
    'count_connectors',
    'count_encoders',
    'min_width',
    'max_width',
    'min_height',
    'max_height',
]
struct_drm_mode_card_res._fields_ = [
    ('fb_id_ptr', __u64),
    ('crtc_id_ptr', __u64),
    ('connector_id_ptr', __u64),
    ('encoder_id_ptr', __u64),
    ('count_fbs', __u32),
    ('count_crtcs', __u32),
    ('count_connectors', __u32),
    ('count_encoders', __u32),
    ('min_width', __u32),
    ('max_width', __u32),
    ('min_height', __u32),
    ('max_height', __u32),
]


class struct_drm_mode_crtc(Structure):
    pass

struct_drm_mode_crtc.__slots__ = [
    'set_connectors_ptr',
    'count_connectors',
    'crtc_id',
    'fb_id',
    'x',
    'y',
    'gamma_size',
    'mode_valid',
    'mode',
]
struct_drm_mode_crtc._fields_ = [
    ('set_connectors_ptr', __u64),
    ('count_connectors', __u32),
    ('crtc_id', __u32),
    ('fb_id', __u32),
    ('x', __u32),
    ('y', __u32),
    ('gamma_size', __u32),
    ('mode_valid', __u32),
    ('mode', struct_drm_mode_modeinfo),
]


class struct_drm_mode_set_plane(Structure):
    pass

struct_drm_mode_set_plane.__slots__ = [
    'plane_id',
    'crtc_id',
    'fb_id',
    'flags',
    'crtc_x',
    'crtc_y',
    'crtc_w',
    'crtc_h',
    'src_x',
    'src_y',
    'src_h',
    'src_w',
]
struct_drm_mode_set_plane._fields_ = [
    ('plane_id', __u32),
    ('crtc_id', __u32),
    ('fb_id', __u32),
    ('flags', __u32),
    ('crtc_x', __s32),
    ('crtc_y', __s32),
    ('crtc_w', __u32),
    ('crtc_h', __u32),
    ('src_x', __u32),
    ('src_y', __u32),
    ('src_h', __u32),
    ('src_w', __u32),
]


class struct_drm_mode_get_plane(Structure):
    pass

struct_drm_mode_get_plane.__slots__ = [
    'plane_id',
    'crtc_id',
    'fb_id',
    'possible_crtcs',
    'gamma_size',
    'count_format_types',
    'format_type_ptr',
]
struct_drm_mode_get_plane._fields_ = [
    ('plane_id', __u32),
    ('crtc_id', __u32),
    ('fb_id', __u32),
    ('possible_crtcs', __u32),
    ('gamma_size', __u32),
    ('count_format_types', __u32),
    ('format_type_ptr', __u64),
]


class struct_drm_mode_get_plane_res(Structure):
    pass

struct_drm_mode_get_plane_res.__slots__ = [
    'plane_id_ptr',
    'count_planes',
]
struct_drm_mode_get_plane_res._fields_ = [
    ('plane_id_ptr', __u64),
    ('count_planes', __u32),
]


class struct_drm_mode_get_encoder(Structure):
    pass

struct_drm_mode_get_encoder.__slots__ = [
    'encoder_id',
    'encoder_type',
    'crtc_id',
    'possible_crtcs',
    'possible_clones',
]
struct_drm_mode_get_encoder._fields_ = [
    ('encoder_id', __u32),
    ('encoder_type', __u32),
    ('crtc_id', __u32),
    ('possible_crtcs', __u32),
    ('possible_clones', __u32),
]

enum_drm_mode_subconnector = c_int

DRM_MODE_SUBCONNECTOR_Automatic = 0

DRM_MODE_SUBCONNECTOR_Unknown = 0

DRM_MODE_SUBCONNECTOR_VGA = 1

DRM_MODE_SUBCONNECTOR_DVID = 3

DRM_MODE_SUBCONNECTOR_DVIA = 4

DRM_MODE_SUBCONNECTOR_Composite = 5

DRM_MODE_SUBCONNECTOR_SVIDEO = 6

DRM_MODE_SUBCONNECTOR_Component = 8

DRM_MODE_SUBCONNECTOR_SCART = 9

DRM_MODE_SUBCONNECTOR_DisplayPort = 10

DRM_MODE_SUBCONNECTOR_HDMIA = 11

DRM_MODE_SUBCONNECTOR_Native = 15

DRM_MODE_SUBCONNECTOR_Wireless = 18


class struct_drm_mode_get_connector(Structure):
    pass

struct_drm_mode_get_connector.__slots__ = [
    'encoders_ptr',
    'modes_ptr',
    'props_ptr',
    'prop_values_ptr',
    'count_modes',
    'count_props',
    'count_encoders',
    'encoder_id',
    'connector_id',
    'connector_type',
    'connector_type_id',
    'connection',
    'mm_width',
    'mm_height',
    'subpixel',
    'pad',
]
struct_drm_mode_get_connector._fields_ = [
    ('encoders_ptr', __u64),
    ('modes_ptr', __u64),
    ('props_ptr', __u64),
    ('prop_values_ptr', __u64),
    ('count_modes', __u32),
    ('count_props', __u32),
    ('count_encoders', __u32),
    ('encoder_id', __u32),
    ('connector_id', __u32),
    ('connector_type', __u32),
    ('connector_type_id', __u32),
    ('connection', __u32),
    ('mm_width', __u32),
    ('mm_height', __u32),
    ('subpixel', __u32),
    ('pad', __u32),
]


class struct_drm_mode_property_enum(Structure):
    pass

struct_drm_mode_property_enum.__slots__ = [
    'value',
    'name',
]
struct_drm_mode_property_enum._fields_ = [
    ('value', __u64),
    ('name', c_char * int(32)),
]


class struct_drm_mode_get_property(Structure):
    pass

struct_drm_mode_get_property.__slots__ = [
    'values_ptr',
    'enum_blob_ptr',
    'prop_id',
    'flags',
    'name',
    'count_values',
    'count_enum_blobs',
]
struct_drm_mode_get_property._fields_ = [
    ('values_ptr', __u64),
    ('enum_blob_ptr', __u64),
    ('prop_id', __u32),
    ('flags', __u32),
    ('name', c_char * int(32)),
    ('count_values', __u32),
    ('count_enum_blobs', __u32),
]


class struct_drm_mode_connector_set_property(Structure):
    pass

struct_drm_mode_connector_set_property.__slots__ = [
    'value',
    'prop_id',
    'connector_id',
]
struct_drm_mode_connector_set_property._fields_ = [
    ('value', __u64),
    ('prop_id', __u32),
    ('connector_id', __u32),
]


class struct_drm_mode_obj_get_properties(Structure):
    pass

struct_drm_mode_obj_get_properties.__slots__ = [
    'props_ptr',
    'prop_values_ptr',
    'count_props',
    'obj_id',
    'obj_type',
]
struct_drm_mode_obj_get_properties._fields_ = [
    ('props_ptr', __u64),
    ('prop_values_ptr', __u64),
    ('count_props', __u32),
    ('obj_id', __u32),
    ('obj_type', __u32),
]


class struct_drm_mode_obj_set_property(Structure):
    pass

struct_drm_mode_obj_set_property.__slots__ = [
    'value',
    'prop_id',
    'obj_id',
    'obj_type',
]
struct_drm_mode_obj_set_property._fields_ = [
    ('value', __u64),
    ('prop_id', __u32),
    ('obj_id', __u32),
    ('obj_type', __u32),
]


class struct_drm_mode_get_blob(Structure):
    pass

struct_drm_mode_get_blob.__slots__ = [
    'blob_id',
    'length',
    'data',
]
struct_drm_mode_get_blob._fields_ = [
    ('blob_id', __u32),
    ('length', __u32),
    ('data', __u64),
]


class struct_drm_mode_fb_cmd(Structure):
    pass

struct_drm_mode_fb_cmd.__slots__ = [
    'fb_id',
    'width',
    'height',
    'pitch',
    'bpp',
    'depth',
    'handle',
]
struct_drm_mode_fb_cmd._fields_ = [
    ('fb_id', __u32),
    ('width', __u32),
    ('height', __u32),
    ('pitch', __u32),
    ('bpp', __u32),
    ('depth', __u32),
    ('handle', __u32),
]


class struct_drm_mode_fb_cmd2(Structure):
    pass

struct_drm_mode_fb_cmd2.__slots__ = [
    'fb_id',
    'width',
    'height',
    'pixel_format',
    'flags',
    'handles',
    'pitches',
    'offsets',
    'modifier',
]
struct_drm_mode_fb_cmd2._fields_ = [
    ('fb_id', __u32),
    ('width', __u32),
    ('height', __u32),
    ('pixel_format', __u32),
    ('flags', __u32),
    ('handles', __u32 * int(4)),
    ('pitches', __u32 * int(4)),
    ('offsets', __u32 * int(4)),
    ('modifier', __u64 * int(4)),
]


class struct_drm_mode_fb_dirty_cmd(Structure):
    pass

struct_drm_mode_fb_dirty_cmd.__slots__ = [
    'fb_id',
    'flags',
    'color',
    'num_clips',
    'clips_ptr',
]
struct_drm_mode_fb_dirty_cmd._fields_ = [
    ('fb_id', __u32),
    ('flags', __u32),
    ('color', __u32),
    ('num_clips', __u32),
    ('clips_ptr', __u64),
]


class struct_drm_mode_mode_cmd(Structure):
    pass

struct_drm_mode_mode_cmd.__slots__ = [
    'connector_id',
    'mode',
]
struct_drm_mode_mode_cmd._fields_ = [
    ('connector_id', __u32),
    ('mode', struct_drm_mode_modeinfo),
]


class struct_drm_mode_cursor(Structure):
    pass

struct_drm_mode_cursor.__slots__ = [
    'flags',
    'crtc_id',
    'x',
    'y',
    'width',
    'height',
    'handle',
]
struct_drm_mode_cursor._fields_ = [
    ('flags', __u32),
    ('crtc_id', __u32),
    ('x', __s32),
    ('y', __s32),
    ('width', __u32),
    ('height', __u32),
    ('handle', __u32),
]


class struct_drm_mode_cursor2(Structure):
    pass

struct_drm_mode_cursor2.__slots__ = [
    'flags',
    'crtc_id',
    'x',
    'y',
    'width',
    'height',
    'handle',
    'hot_x',
    'hot_y',
]
struct_drm_mode_cursor2._fields_ = [
    ('flags', __u32),
    ('crtc_id', __u32),
    ('x', __s32),
    ('y', __s32),
    ('width', __u32),
    ('height', __u32),
    ('handle', __u32),
    ('hot_x', __s32),
    ('hot_y', __s32),
]


class struct_drm_mode_crtc_lut(Structure):
    pass

struct_drm_mode_crtc_lut.__slots__ = [
    'crtc_id',
    'gamma_size',
    'red',
    'green',
    'blue',
]
struct_drm_mode_crtc_lut._fields_ = [
    ('crtc_id', __u32),
    ('gamma_size', __u32),
    ('red', __u64),
    ('green', __u64),
    ('blue', __u64),
]


class struct_drm_color_ctm(Structure):
    pass

struct_drm_color_ctm.__slots__ = [
    'matrix',
]
struct_drm_color_ctm._fields_ = [
    ('matrix', __u64 * int(9)),
]


class struct_drm_color_lut(Structure):
    pass

struct_drm_color_lut.__slots__ = [
    'red',
    'green',
    'blue',
    'reserved',
]
struct_drm_color_lut._fields_ = [
    ('red', __u16),
    ('green', __u16),
    ('blue', __u16),
    ('reserved', __u16),
]


class struct_anon_7(Structure):
    pass

struct_anon_7.__slots__ = [
    'x',
    'y',
]
struct_anon_7._fields_ = [
    ('x', __u16),
    ('y', __u16),
]


class struct_anon_8(Structure):
    pass

struct_anon_8.__slots__ = [
    'x',
    'y',
]
struct_anon_8._fields_ = [
    ('x', __u16),
    ('y', __u16),
]


class struct_hdr_metadata_infoframe(Structure):
    pass

struct_hdr_metadata_infoframe.__slots__ = [
    'eotf',
    'metadata_type',
    'display_primaries',
    'white_point',
    'max_display_mastering_luminance',
    'min_display_mastering_luminance',
    'max_cll',
    'max_fall',
]
struct_hdr_metadata_infoframe._fields_ = [
    ('eotf', __u8),
    ('metadata_type', __u8),
    ('display_primaries', struct_anon_7 * int(3)),
    ('white_point', struct_anon_8),
    ('max_display_mastering_luminance', __u16),
    ('min_display_mastering_luminance', __u16),
    ('max_cll', __u16),
    ('max_fall', __u16),
]


class union_anon_9(Union):
    pass

union_anon_9.__slots__ = [
    'hdmi_metadata_type1',
]
union_anon_9._fields_ = [
    ('hdmi_metadata_type1', struct_hdr_metadata_infoframe),
]


class struct_hdr_output_metadata(Structure):
    pass

struct_hdr_output_metadata.__slots__ = [
    'metadata_type',
    'unnamed_1',
]
struct_hdr_output_metadata._anonymous_ = [
    'unnamed_1',
]
struct_hdr_output_metadata._fields_ = [
    ('metadata_type', __u32),
    ('unnamed_1', union_anon_9),
]


class struct_drm_mode_crtc_page_flip(Structure):
    pass

struct_drm_mode_crtc_page_flip.__slots__ = [
    'crtc_id',
    'fb_id',
    'flags',
    'reserved',
    'user_data',
]
struct_drm_mode_crtc_page_flip._fields_ = [
    ('crtc_id', __u32),
    ('fb_id', __u32),
    ('flags', __u32),
    ('reserved', __u32),
    ('user_data', __u64),
]


class struct_drm_mode_crtc_page_flip_target(Structure):
    pass

struct_drm_mode_crtc_page_flip_target.__slots__ = [
    'crtc_id',
    'fb_id',
    'flags',
    'sequence',
    'user_data',
]
struct_drm_mode_crtc_page_flip_target._fields_ = [
    ('crtc_id', __u32),
    ('fb_id', __u32),
    ('flags', __u32),
    ('sequence', __u32),
    ('user_data', __u64),
]


class struct_drm_mode_create_dumb(Structure):
    pass

struct_drm_mode_create_dumb.__slots__ = [
    'height',
    'width',
    'bpp',
    'flags',
    'handle',
    'pitch',
    'size',
]
struct_drm_mode_create_dumb._fields_ = [
    ('height', __u32),
    ('width', __u32),
    ('bpp', __u32),
    ('flags', __u32),
    ('handle', __u32),
    ('pitch', __u32),
    ('size', __u64),
]


class struct_drm_mode_map_dumb(Structure):
    pass

struct_drm_mode_map_dumb.__slots__ = [
    'handle',
    'pad',
    'offset',
]
struct_drm_mode_map_dumb._fields_ = [
    ('handle', __u32),
    ('pad', __u32),
    ('offset', __u64),
]


class struct_drm_mode_destroy_dumb(Structure):
    pass

struct_drm_mode_destroy_dumb.__slots__ = [
    'handle',
]
struct_drm_mode_destroy_dumb._fields_ = [
    ('handle', __u32),
]


class struct_drm_mode_atomic(Structure):
    pass

struct_drm_mode_atomic.__slots__ = [
    'flags',
    'count_objs',
    'objs_ptr',
    'count_props_ptr',
    'props_ptr',
    'prop_values_ptr',
    'reserved',
    'user_data',
]
struct_drm_mode_atomic._fields_ = [
    ('flags', __u32),
    ('count_objs', __u32),
    ('objs_ptr', __u64),
    ('count_props_ptr', __u64),
    ('props_ptr', __u64),
    ('prop_values_ptr', __u64),
    ('reserved', __u64),
    ('user_data', __u64),
]


class struct_drm_format_modifier_blob(Structure):
    pass

struct_drm_format_modifier_blob.__slots__ = [
    'version',
    'flags',
    'count_formats',
    'formats_offset',
    'count_modifiers',
    'modifiers_offset',
]
struct_drm_format_modifier_blob._fields_ = [
    ('version', __u32),
    ('flags', __u32),
    ('count_formats', __u32),
    ('formats_offset', __u32),
    ('count_modifiers', __u32),
    ('modifiers_offset', __u32),
]


class struct_drm_format_modifier(Structure):
    pass

struct_drm_format_modifier.__slots__ = [
    'formats',
    'offset',
    'pad',
    'modifier',
]
struct_drm_format_modifier._fields_ = [
    ('formats', __u64),
    ('offset', __u32),
    ('pad', __u32),
    ('modifier', __u64),
]


class struct_drm_mode_create_blob(Structure):
    pass

struct_drm_mode_create_blob.__slots__ = [
    'data',
    'length',
    'blob_id',
]
struct_drm_mode_create_blob._fields_ = [
    ('data', __u64),
    ('length', __u32),
    ('blob_id', __u32),
]


class struct_drm_mode_destroy_blob(Structure):
    pass

struct_drm_mode_destroy_blob.__slots__ = [
    'blob_id',
]
struct_drm_mode_destroy_blob._fields_ = [
    ('blob_id', __u32),
]


class struct_drm_mode_create_lease(Structure):
    pass

struct_drm_mode_create_lease.__slots__ = [
    'object_ids',
    'object_count',
    'flags',
    'lessee_id',
    'fd',
]
struct_drm_mode_create_lease._fields_ = [
    ('object_ids', __u64),
    ('object_count', __u32),
    ('flags', __u32),
    ('lessee_id', __u32),
    ('fd', __u32),
]


class struct_drm_mode_list_lessees(Structure):
    pass

struct_drm_mode_list_lessees.__slots__ = [
    'count_lessees',
    'pad',
    'lessees_ptr',
]
struct_drm_mode_list_lessees._fields_ = [
    ('count_lessees', __u32),
    ('pad', __u32),
    ('lessees_ptr', __u64),
]


class struct_drm_mode_get_lease(Structure):
    pass

struct_drm_mode_get_lease.__slots__ = [
    'count_objects',
    'pad',
    'objects_ptr',
]
struct_drm_mode_get_lease._fields_ = [
    ('count_objects', __u32),
    ('pad', __u32),
    ('objects_ptr', __u64),
]


class struct_drm_mode_revoke_lease(Structure):
    pass

struct_drm_mode_revoke_lease.__slots__ = [
    'lessee_id',
]
struct_drm_mode_revoke_lease._fields_ = [
    ('lessee_id', __u32),
]


class struct_drm_mode_rect(Structure):
    pass

struct_drm_mode_rect.__slots__ = [
    'x1',
    'y1',
    'x2',
    'y2',
]
struct_drm_mode_rect._fields_ = [
    ('x1', __s32),
    ('y1', __s32),
    ('x2', __s32),
    ('y2', __s32),
]


class struct_drm_event(Structure):
    pass

struct_drm_event.__slots__ = [
    'type',
    'length',
]
struct_drm_event._fields_ = [
    ('type', __u32),
    ('length', __u32),
]


class struct_drm_event_vblank(Structure):
    pass

struct_drm_event_vblank.__slots__ = [
    'base',
    'user_data',
    'tv_sec',
    'tv_usec',
    'sequence',
    'crtc_id',
]
struct_drm_event_vblank._fields_ = [
    ('base', struct_drm_event),
    ('user_data', __u64),
    ('tv_sec', __u32),
    ('tv_usec', __u32),
    ('sequence', __u32),
    ('crtc_id', __u32),
]


class struct_drm_event_crtc_sequence(Structure):
    pass

struct_drm_event_crtc_sequence.__slots__ = [
    'base',
    'user_data',
    'time_ns',
    'sequence',
]
struct_drm_event_crtc_sequence._fields_ = [
    ('base', struct_drm_event),
    ('user_data', __u64),
    ('time_ns', __s64),
    ('sequence', __u64),
]

drm_clip_rect_t = struct_drm_clip_rect

drm_drawable_info_t = struct_drm_drawable_info

drm_tex_region_t = struct_drm_tex_region

drm_hw_lock_t = struct_drm_hw_lock

drm_version_t = struct_drm_version

drm_unique_t = struct_drm_unique

drm_list_t = struct_drm_list

drm_block_t = struct_drm_block

drm_control_t = struct_drm_control

drm_map_type_t = enum_drm_map_type

drm_map_flags_t = enum_drm_map_flags

drm_ctx_priv_map_t = struct_drm_ctx_priv_map

drm_map_t = struct_drm_map

drm_client_t = struct_drm_client

drm_stat_type_t = enum_drm_stat_type

drm_stats_t = struct_drm_stats

drm_lock_flags_t = enum_drm_lock_flags

drm_lock_t = struct_drm_lock

drm_dma_flags_t = enum_drm_dma_flags

drm_buf_desc_t = struct_drm_buf_desc

drm_buf_info_t = struct_drm_buf_info

drm_buf_free_t = struct_drm_buf_free

drm_buf_pub_t = struct_drm_buf_pub

drm_buf_map_t = struct_drm_buf_map

drm_dma_t = struct_drm_dma

drm_wait_vblank_t = union_drm_wait_vblank

drm_agp_mode_t = struct_drm_agp_mode

drm_ctx_flags_t = enum_drm_ctx_flags

drm_ctx_t = struct_drm_ctx

drm_ctx_res_t = struct_drm_ctx_res

drm_draw_t = struct_drm_draw

drm_update_draw_t = struct_drm_update_draw

drm_auth_t = struct_drm_auth

drm_irq_busid_t = struct_drm_irq_busid

drm_vblank_seq_type_t = enum_drm_vblank_seq_type

drm_agp_buffer_t = struct_drm_agp_buffer

drm_agp_binding_t = struct_drm_agp_binding

drm_agp_info_t = struct_drm_agp_info

drm_scatter_gather_t = struct_drm_scatter_gather

drm_set_version_t = struct_drm_set_version


_IOC_NRBITS = 8


_IOC_TYPEBITS = 8


_IOC_SIZEBITS = 14


_IOC_NRSHIFT = 0


_IOC_TYPESHIFT = (_IOC_NRSHIFT + _IOC_NRBITS)


_IOC_SIZESHIFT = (_IOC_TYPESHIFT + _IOC_TYPEBITS)


_IOC_DIRSHIFT = (_IOC_SIZESHIFT + _IOC_SIZEBITS)


_IOC_NONE = 0


_IOC_WRITE = 1


_IOC_READ = 2


def _IOC(dir, type, nr, size):
    return ((((dir << _IOC_DIRSHIFT) | (ord(type) << _IOC_TYPESHIFT)) | (nr << _IOC_NRSHIFT)) | (size << _IOC_SIZESHIFT))


def _IOC_TYPECHECK(t):
    return sizeof(t)


def _IO(type, nr):
    return (_IOC (_IOC_NONE, type, nr, 0))


def _IOR(type, nr, size):
    return (_IOC (_IOC_READ, type, nr, (_IOC_TYPECHECK (size))))


def _IOW(type, nr, size):
    return (_IOC (_IOC_WRITE, type, nr, (_IOC_TYPECHECK (size))))


def _IOWR(type, nr, size):
    return (_IOC ((_IOC_READ | _IOC_WRITE), type, nr, (_IOC_TYPECHECK (size))))


DRM_NAME = 'drm'


DRM_MIN_ORDER = 5


DRM_MAX_ORDER = 22


DRM_RAM_PERCENT = 10


_DRM_LOCK_HELD = 0x80000000


_DRM_LOCK_CONT = 0x40000000


def _DRM_LOCK_IS_HELD(lock):
    return (lock & _DRM_LOCK_HELD)


def _DRM_LOCK_IS_CONT(lock):
    return (lock & _DRM_LOCK_CONT)


def _DRM_LOCKING_CONTEXT(lock):
    return (lock & (~(_DRM_LOCK_HELD | _DRM_LOCK_CONT)))


_DRM_VBLANK_HIGH_CRTC_SHIFT = 1


_DRM_VBLANK_TYPES_MASK = (_DRM_VBLANK_ABSOLUTE | _DRM_VBLANK_RELATIVE)


_DRM_VBLANK_FLAGS_MASK = (((_DRM_VBLANK_EVENT | _DRM_VBLANK_SIGNAL) | _DRM_VBLANK_SECONDARY) | _DRM_VBLANK_NEXTONMISS)


_DRM_PRE_MODESET = 1


_DRM_POST_MODESET = 2


DRM_CAP_DUMB_BUFFER = 0x1


DRM_CAP_VBLANK_HIGH_CRTC = 0x2


DRM_CAP_DUMB_PREFERRED_DEPTH = 0x3


DRM_CAP_DUMB_PREFER_SHADOW = 0x4


DRM_CAP_PRIME = 0x5


DRM_PRIME_CAP_IMPORT = 0x1


DRM_PRIME_CAP_EXPORT = 0x2


DRM_CAP_TIMESTAMP_MONOTONIC = 0x6


DRM_CAP_ASYNC_PAGE_FLIP = 0x7


DRM_CAP_CURSOR_WIDTH = 0x8


DRM_CAP_CURSOR_HEIGHT = 0x9


DRM_CAP_ADDFB2_MODIFIERS = 0x10


DRM_CAP_PAGE_FLIP_TARGET = 0x11


DRM_CAP_CRTC_IN_VBLANK_EVENT = 0x12


DRM_CAP_SYNCOBJ = 0x13


DRM_CAP_SYNCOBJ_TIMELINE = 0x14


DRM_CLIENT_CAP_STEREO_3D = 1


DRM_CLIENT_CAP_UNIVERSAL_PLANES = 2


DRM_CLIENT_CAP_ATOMIC = 3


DRM_CLIENT_CAP_ASPECT_RATIO = 4


DRM_CLIENT_CAP_WRITEBACK_CONNECTORS = 5


DRM_SYNCOBJ_CREATE_SIGNALED = (1 << 0)


DRM_SYNCOBJ_FD_TO_HANDLE_FLAGS_IMPORT_SYNC_FILE = (1 << 0)


DRM_SYNCOBJ_HANDLE_TO_FD_FLAGS_EXPORT_SYNC_FILE = (1 << 0)


DRM_SYNCOBJ_WAIT_FLAGS_WAIT_ALL = (1 << 0)


DRM_SYNCOBJ_WAIT_FLAGS_WAIT_FOR_SUBMIT = (1 << 1)


DRM_SYNCOBJ_WAIT_FLAGS_WAIT_AVAILABLE = (1 << 2)


DRM_SYNCOBJ_QUERY_FLAGS_LAST_SUBMITTED = (1 << 0)


DRM_CRTC_SEQUENCE_RELATIVE = 0x00000001


DRM_CRTC_SEQUENCE_NEXT_ON_MISS = 0x00000002


DRM_CONNECTOR_NAME_LEN = 32


DRM_DISPLAY_MODE_LEN = 32


DRM_PROP_NAME_LEN = 32


DRM_MODE_TYPE_BUILTIN = (1 << 0)


DRM_MODE_TYPE_CLOCK_C = ((1 << 1) | DRM_MODE_TYPE_BUILTIN)


DRM_MODE_TYPE_CRTC_C = ((1 << 2) | DRM_MODE_TYPE_BUILTIN)


DRM_MODE_TYPE_PREFERRED = (1 << 3)


DRM_MODE_TYPE_DEFAULT = (1 << 4)


DRM_MODE_TYPE_USERDEF = (1 << 5)


DRM_MODE_TYPE_DRIVER = (1 << 6)


DRM_MODE_TYPE_ALL = ((DRM_MODE_TYPE_PREFERRED | DRM_MODE_TYPE_USERDEF) | DRM_MODE_TYPE_DRIVER)


DRM_MODE_FLAG_PHSYNC = (1 << 0)


DRM_MODE_FLAG_NHSYNC = (1 << 1)


DRM_MODE_FLAG_PVSYNC = (1 << 2)


DRM_MODE_FLAG_NVSYNC = (1 << 3)


DRM_MODE_FLAG_INTERLACE = (1 << 4)


DRM_MODE_FLAG_DBLSCAN = (1 << 5)


DRM_MODE_FLAG_CSYNC = (1 << 6)


DRM_MODE_FLAG_PCSYNC = (1 << 7)


DRM_MODE_FLAG_NCSYNC = (1 << 8)


DRM_MODE_FLAG_HSKEW = (1 << 9)


DRM_MODE_FLAG_BCAST = (1 << 10)


DRM_MODE_FLAG_PIXMUX = (1 << 11)


DRM_MODE_FLAG_DBLCLK = (1 << 12)


DRM_MODE_FLAG_CLKDIV2 = (1 << 13)


DRM_MODE_FLAG_3D_MASK = (0x1f << 14)


DRM_MODE_FLAG_3D_NONE = (0 << 14)


DRM_MODE_FLAG_3D_FRAME_PACKING = (1 << 14)


DRM_MODE_FLAG_3D_FIELD_ALTERNATIVE = (2 << 14)


DRM_MODE_FLAG_3D_LINE_ALTERNATIVE = (3 << 14)


DRM_MODE_FLAG_3D_SIDE_BY_SIDE_FULL = (4 << 14)


DRM_MODE_FLAG_3D_L_DEPTH = (5 << 14)


DRM_MODE_FLAG_3D_L_DEPTH_GFX_GFX_DEPTH = (6 << 14)


DRM_MODE_FLAG_3D_TOP_AND_BOTTOM = (7 << 14)


DRM_MODE_FLAG_3D_SIDE_BY_SIDE_HALF = (8 << 14)


DRM_MODE_PICTURE_ASPECT_NONE = 0


DRM_MODE_PICTURE_ASPECT_4_3 = 1


DRM_MODE_PICTURE_ASPECT_16_9 = 2


DRM_MODE_PICTURE_ASPECT_64_27 = 3


DRM_MODE_PICTURE_ASPECT_256_135 = 4


DRM_MODE_CONTENT_TYPE_NO_DATA = 0


DRM_MODE_CONTENT_TYPE_GRAPHICS = 1


DRM_MODE_CONTENT_TYPE_PHOTO = 2


DRM_MODE_CONTENT_TYPE_CINEMA = 3


DRM_MODE_CONTENT_TYPE_GAME = 4


DRM_MODE_FLAG_PIC_AR_MASK = (0x0F << 19)


DRM_MODE_FLAG_PIC_AR_NONE = (DRM_MODE_PICTURE_ASPECT_NONE << 19)


DRM_MODE_FLAG_PIC_AR_4_3 = (DRM_MODE_PICTURE_ASPECT_4_3 << 19)


DRM_MODE_FLAG_PIC_AR_16_9 = (DRM_MODE_PICTURE_ASPECT_16_9 << 19)


DRM_MODE_FLAG_PIC_AR_64_27 = (DRM_MODE_PICTURE_ASPECT_64_27 << 19)


DRM_MODE_FLAG_PIC_AR_256_135 = (DRM_MODE_PICTURE_ASPECT_256_135 << 19)


DRM_MODE_FLAG_ALL = ((((((((((((DRM_MODE_FLAG_PHSYNC | DRM_MODE_FLAG_NHSYNC) | DRM_MODE_FLAG_PVSYNC) | DRM_MODE_FLAG_NVSYNC) | DRM_MODE_FLAG_INTERLACE) | DRM_MODE_FLAG_DBLSCAN) | DRM_MODE_FLAG_CSYNC) | DRM_MODE_FLAG_PCSYNC) | DRM_MODE_FLAG_NCSYNC) | DRM_MODE_FLAG_HSKEW) | DRM_MODE_FLAG_DBLCLK) | DRM_MODE_FLAG_CLKDIV2) | DRM_MODE_FLAG_3D_MASK)


DRM_MODE_DPMS_ON = 0


DRM_MODE_DPMS_STANDBY = 1


DRM_MODE_DPMS_SUSPEND = 2


DRM_MODE_DPMS_OFF = 3


DRM_MODE_SCALE_NONE = 0


DRM_MODE_SCALE_FULLSCREEN = 1


DRM_MODE_SCALE_CENTER = 2


DRM_MODE_SCALE_ASPECT = 3


DRM_MODE_DITHERING_OFF = 0


DRM_MODE_DITHERING_ON = 1


DRM_MODE_DITHERING_AUTO = 2


DRM_MODE_DIRTY_OFF = 0


DRM_MODE_DIRTY_ON = 1


DRM_MODE_DIRTY_ANNOTATE = 2


DRM_MODE_LINK_STATUS_GOOD = 0


DRM_MODE_LINK_STATUS_BAD = 1


DRM_MODE_ROTATE_0 = (1 << 0)


DRM_MODE_ROTATE_90 = (1 << 1)


DRM_MODE_ROTATE_180 = (1 << 2)


DRM_MODE_ROTATE_270 = (1 << 3)


DRM_MODE_ROTATE_MASK = (((DRM_MODE_ROTATE_0 | DRM_MODE_ROTATE_90) | DRM_MODE_ROTATE_180) | DRM_MODE_ROTATE_270)


DRM_MODE_REFLECT_X = (1 << 4)


DRM_MODE_REFLECT_Y = (1 << 5)


DRM_MODE_REFLECT_MASK = (DRM_MODE_REFLECT_X | DRM_MODE_REFLECT_Y)


DRM_MODE_CONTENT_PROTECTION_UNDESIRED = 0


DRM_MODE_CONTENT_PROTECTION_DESIRED = 1


DRM_MODE_CONTENT_PROTECTION_ENABLED = 2


DRM_MODE_PRESENT_TOP_FIELD = (1 << 0)


DRM_MODE_PRESENT_BOTTOM_FIELD = (1 << 1)


DRM_MODE_ENCODER_NONE = 0


DRM_MODE_ENCODER_DAC = 1


DRM_MODE_ENCODER_TMDS = 2


DRM_MODE_ENCODER_LVDS = 3


DRM_MODE_ENCODER_TVDAC = 4


DRM_MODE_ENCODER_VIRTUAL = 5


DRM_MODE_ENCODER_DSI = 6


DRM_MODE_ENCODER_DPMST = 7


DRM_MODE_ENCODER_DPI = 8


DRM_MODE_CONNECTOR_Unknown = 0


DRM_MODE_CONNECTOR_VGA = 1


DRM_MODE_CONNECTOR_DVII = 2


DRM_MODE_CONNECTOR_DVID = 3


DRM_MODE_CONNECTOR_DVIA = 4


DRM_MODE_CONNECTOR_Composite = 5


DRM_MODE_CONNECTOR_SVIDEO = 6


DRM_MODE_CONNECTOR_LVDS = 7


DRM_MODE_CONNECTOR_Component = 8


DRM_MODE_CONNECTOR_9PinDIN = 9


DRM_MODE_CONNECTOR_DisplayPort = 10


DRM_MODE_CONNECTOR_HDMIA = 11


DRM_MODE_CONNECTOR_HDMIB = 12


DRM_MODE_CONNECTOR_TV = 13


DRM_MODE_CONNECTOR_eDP = 14


DRM_MODE_CONNECTOR_VIRTUAL = 15


DRM_MODE_CONNECTOR_DSI = 16


DRM_MODE_CONNECTOR_DPI = 17


DRM_MODE_CONNECTOR_WRITEBACK = 18


DRM_MODE_CONNECTOR_SPI = 19


DRM_MODE_CONNECTOR_USB = 20


DRM_MODE_PROP_PENDING = (1 << 0)


DRM_MODE_PROP_RANGE = (1 << 1)


DRM_MODE_PROP_IMMUTABLE = (1 << 2)


DRM_MODE_PROP_ENUM = (1 << 3)


DRM_MODE_PROP_BLOB = (1 << 4)


DRM_MODE_PROP_BITMASK = (1 << 5)


DRM_MODE_PROP_LEGACY_TYPE = (((DRM_MODE_PROP_RANGE | DRM_MODE_PROP_ENUM) | DRM_MODE_PROP_BLOB) | DRM_MODE_PROP_BITMASK)


DRM_MODE_PROP_EXTENDED_TYPE = 0x0000ffc0


def DRM_MODE_PROP_TYPE(n):
    return (n << 6)


DRM_MODE_PROP_OBJECT = (DRM_MODE_PROP_TYPE (1))


DRM_MODE_PROP_SIGNED_RANGE = (DRM_MODE_PROP_TYPE (2))


DRM_MODE_PROP_ATOMIC = 0x80000000


DRM_MODE_OBJECT_CRTC = 0xcccccccc


DRM_MODE_OBJECT_CONNECTOR = 0xc0c0c0c0


DRM_MODE_OBJECT_ENCODER = 0xe0e0e0e0


DRM_MODE_OBJECT_MODE = 0xdededede


DRM_MODE_OBJECT_PROPERTY = 0xb0b0b0b0


DRM_MODE_OBJECT_FB = 0xfbfbfbfb


DRM_MODE_OBJECT_BLOB = 0xbbbbbbbb


DRM_MODE_OBJECT_PLANE = 0xeeeeeeee


DRM_MODE_OBJECT_ANY = 0


DRM_MODE_FB_INTERLACED = (1 << 0)


DRM_MODE_FB_MODIFIERS = (1 << 1)


DRM_MODE_FB_DIRTY_ANNOTATE_COPY = 0x01


DRM_MODE_FB_DIRTY_ANNOTATE_FILL = 0x02


DRM_MODE_FB_DIRTY_FLAGS = 0x03


DRM_MODE_FB_DIRTY_MAX_CLIPS = 256


DRM_MODE_CURSOR_BO = 0x01


DRM_MODE_CURSOR_MOVE = 0x02


DRM_MODE_CURSOR_FLAGS = 0x03


DRM_MODE_PAGE_FLIP_EVENT = 0x01


DRM_MODE_PAGE_FLIP_ASYNC = 0x02


DRM_MODE_PAGE_FLIP_TARGET_ABSOLUTE = 0x4


DRM_MODE_PAGE_FLIP_TARGET_RELATIVE = 0x8


DRM_MODE_PAGE_FLIP_TARGET = (DRM_MODE_PAGE_FLIP_TARGET_ABSOLUTE | DRM_MODE_PAGE_FLIP_TARGET_RELATIVE)


DRM_MODE_PAGE_FLIP_FLAGS = ((DRM_MODE_PAGE_FLIP_EVENT | DRM_MODE_PAGE_FLIP_ASYNC) | DRM_MODE_PAGE_FLIP_TARGET)


DRM_MODE_ATOMIC_TEST_ONLY = 0x0100


DRM_MODE_ATOMIC_NONBLOCK = 0x0200


DRM_MODE_ATOMIC_ALLOW_MODESET = 0x0400


DRM_MODE_ATOMIC_FLAGS = ((((DRM_MODE_PAGE_FLIP_EVENT | DRM_MODE_PAGE_FLIP_ASYNC) | DRM_MODE_ATOMIC_TEST_ONLY) | DRM_MODE_ATOMIC_NONBLOCK) | DRM_MODE_ATOMIC_ALLOW_MODESET)


FORMAT_BLOB_CURRENT = 1


DRM_IOCTL_BASE = 'd'


def DRM_IO(nr):
    return (_IO (DRM_IOCTL_BASE, nr))


def DRM_IOR(nr, type):
    return (_IOR (DRM_IOCTL_BASE, nr, type))


def DRM_IOW(nr, type):
    return (_IOW (DRM_IOCTL_BASE, nr, type))


def DRM_IOWR(nr, type):
    return (_IOWR (DRM_IOCTL_BASE, nr, type))


DRM_IOCTL_VERSION = (DRM_IOWR (0x00, struct_drm_version))


DRM_IOCTL_GET_UNIQUE = (DRM_IOWR (0x01, struct_drm_unique))


DRM_IOCTL_GET_MAGIC = (DRM_IOR (0x02, struct_drm_auth))


DRM_IOCTL_IRQ_BUSID = (DRM_IOWR (0x03, struct_drm_irq_busid))


DRM_IOCTL_GET_MAP = (DRM_IOWR (0x04, struct_drm_map))


DRM_IOCTL_GET_CLIENT = (DRM_IOWR (0x05, struct_drm_client))


DRM_IOCTL_GET_STATS = (DRM_IOR (0x06, struct_drm_stats))


DRM_IOCTL_SET_VERSION = (DRM_IOWR (0x07, struct_drm_set_version))


DRM_IOCTL_MODESET_CTL = (DRM_IOW (0x08, struct_drm_modeset_ctl))


DRM_IOCTL_GEM_CLOSE = (DRM_IOW (0x09, struct_drm_gem_close))


DRM_IOCTL_GEM_FLINK = (DRM_IOWR (0x0a, struct_drm_gem_flink))


DRM_IOCTL_GEM_OPEN = (DRM_IOWR (0x0b, struct_drm_gem_open))


DRM_IOCTL_GET_CAP = (DRM_IOWR (0x0c, struct_drm_get_cap))


DRM_IOCTL_SET_CLIENT_CAP = (DRM_IOW (0x0d, struct_drm_set_client_cap))


DRM_IOCTL_SET_UNIQUE = (DRM_IOW (0x10, struct_drm_unique))


DRM_IOCTL_AUTH_MAGIC = (DRM_IOW (0x11, struct_drm_auth))


DRM_IOCTL_BLOCK = (DRM_IOWR (0x12, struct_drm_block))


DRM_IOCTL_UNBLOCK = (DRM_IOWR (0x13, struct_drm_block))


DRM_IOCTL_CONTROL = (DRM_IOW (0x14, struct_drm_control))


DRM_IOCTL_ADD_MAP = (DRM_IOWR (0x15, struct_drm_map))


DRM_IOCTL_ADD_BUFS = (DRM_IOWR (0x16, struct_drm_buf_desc))


DRM_IOCTL_MARK_BUFS = (DRM_IOW (0x17, struct_drm_buf_desc))


DRM_IOCTL_INFO_BUFS = (DRM_IOWR (0x18, struct_drm_buf_info))


DRM_IOCTL_MAP_BUFS = (DRM_IOWR (0x19, struct_drm_buf_map))


DRM_IOCTL_FREE_BUFS = (DRM_IOW (0x1a, struct_drm_buf_free))


DRM_IOCTL_RM_MAP = (DRM_IOW (0x1b, struct_drm_map))


DRM_IOCTL_SET_SAREA_CTX = (DRM_IOW (0x1c, struct_drm_ctx_priv_map))


DRM_IOCTL_GET_SAREA_CTX = (DRM_IOWR (0x1d, struct_drm_ctx_priv_map))


DRM_IOCTL_SET_MASTER = (DRM_IO (0x1e))


DRM_IOCTL_DROP_MASTER = (DRM_IO (0x1f))


DRM_IOCTL_ADD_CTX = (DRM_IOWR (0x20, struct_drm_ctx))


DRM_IOCTL_RM_CTX = (DRM_IOWR (0x21, struct_drm_ctx))


DRM_IOCTL_MOD_CTX = (DRM_IOW (0x22, struct_drm_ctx))


DRM_IOCTL_GET_CTX = (DRM_IOWR (0x23, struct_drm_ctx))


DRM_IOCTL_SWITCH_CTX = (DRM_IOW (0x24, struct_drm_ctx))


DRM_IOCTL_NEW_CTX = (DRM_IOW (0x25, struct_drm_ctx))


DRM_IOCTL_RES_CTX = (DRM_IOWR (0x26, struct_drm_ctx_res))


DRM_IOCTL_ADD_DRAW = (DRM_IOWR (0x27, struct_drm_draw))


DRM_IOCTL_RM_DRAW = (DRM_IOWR (0x28, struct_drm_draw))


DRM_IOCTL_DMA = (DRM_IOWR (0x29, struct_drm_dma))


DRM_IOCTL_LOCK = (DRM_IOW (0x2a, struct_drm_lock))


DRM_IOCTL_UNLOCK = (DRM_IOW (0x2b, struct_drm_lock))


DRM_IOCTL_FINISH = (DRM_IOW (0x2c, struct_drm_lock))


DRM_IOCTL_PRIME_HANDLE_TO_FD = (DRM_IOWR (0x2d, struct_drm_prime_handle))


DRM_IOCTL_PRIME_FD_TO_HANDLE = (DRM_IOWR (0x2e, struct_drm_prime_handle))


DRM_IOCTL_AGP_ACQUIRE = (DRM_IO (0x30))


DRM_IOCTL_AGP_RELEASE = (DRM_IO (0x31))


DRM_IOCTL_AGP_ENABLE = (DRM_IOW (0x32, struct_drm_agp_mode))


DRM_IOCTL_AGP_INFO = (DRM_IOR (0x33, struct_drm_agp_info))


DRM_IOCTL_AGP_ALLOC = (DRM_IOWR (0x34, struct_drm_agp_buffer))


DRM_IOCTL_AGP_FREE = (DRM_IOW (0x35, struct_drm_agp_buffer))


DRM_IOCTL_AGP_BIND = (DRM_IOW (0x36, struct_drm_agp_binding))


DRM_IOCTL_AGP_UNBIND = (DRM_IOW (0x37, struct_drm_agp_binding))


DRM_IOCTL_SG_ALLOC = (DRM_IOWR (0x38, struct_drm_scatter_gather))


DRM_IOCTL_SG_FREE = (DRM_IOW (0x39, struct_drm_scatter_gather))


DRM_IOCTL_WAIT_VBLANK = (DRM_IOWR (0x3a, union_drm_wait_vblank))


DRM_IOCTL_CRTC_GET_SEQUENCE = (DRM_IOWR (0x3b, struct_drm_crtc_get_sequence))


DRM_IOCTL_CRTC_QUEUE_SEQUENCE = (DRM_IOWR (0x3c, struct_drm_crtc_queue_sequence))


DRM_IOCTL_UPDATE_DRAW = (DRM_IOW (0x3f, struct_drm_update_draw))


DRM_IOCTL_MODE_GETRESOURCES = (DRM_IOWR (0xA0, struct_drm_mode_card_res))


DRM_IOCTL_MODE_GETCRTC = (DRM_IOWR (0xA1, struct_drm_mode_crtc))


DRM_IOCTL_MODE_SETCRTC = (DRM_IOWR (0xA2, struct_drm_mode_crtc))


DRM_IOCTL_MODE_CURSOR = (DRM_IOWR (0xA3, struct_drm_mode_cursor))


DRM_IOCTL_MODE_GETGAMMA = (DRM_IOWR (0xA4, struct_drm_mode_crtc_lut))


DRM_IOCTL_MODE_SETGAMMA = (DRM_IOWR (0xA5, struct_drm_mode_crtc_lut))


DRM_IOCTL_MODE_GETENCODER = (DRM_IOWR (0xA6, struct_drm_mode_get_encoder))


DRM_IOCTL_MODE_GETCONNECTOR = (DRM_IOWR (0xA7, struct_drm_mode_get_connector))


DRM_IOCTL_MODE_ATTACHMODE = (DRM_IOWR (0xA8, struct_drm_mode_mode_cmd))


DRM_IOCTL_MODE_DETACHMODE = (DRM_IOWR (0xA9, struct_drm_mode_mode_cmd))


DRM_IOCTL_MODE_GETPROPERTY = (DRM_IOWR (0xAA, struct_drm_mode_get_property))


DRM_IOCTL_MODE_SETPROPERTY = (DRM_IOWR (0xAB, struct_drm_mode_connector_set_property))


DRM_IOCTL_MODE_GETPROPBLOB = (DRM_IOWR (0xAC, struct_drm_mode_get_blob))


DRM_IOCTL_MODE_GETFB = (DRM_IOWR (0xAD, struct_drm_mode_fb_cmd))


DRM_IOCTL_MODE_ADDFB = (DRM_IOWR (0xAE, struct_drm_mode_fb_cmd))


DRM_IOCTL_MODE_RMFB = (DRM_IOWR (0xAF, c_uint))


DRM_IOCTL_MODE_PAGE_FLIP = (DRM_IOWR (0xB0, struct_drm_mode_crtc_page_flip))


DRM_IOCTL_MODE_DIRTYFB = (DRM_IOWR (0xB1, struct_drm_mode_fb_dirty_cmd))


DRM_IOCTL_MODE_CREATE_DUMB = (DRM_IOWR (0xB2, struct_drm_mode_create_dumb))


DRM_IOCTL_MODE_MAP_DUMB = (DRM_IOWR (0xB3, struct_drm_mode_map_dumb))


DRM_IOCTL_MODE_DESTROY_DUMB = (DRM_IOWR (0xB4, struct_drm_mode_destroy_dumb))


DRM_IOCTL_MODE_GETPLANERESOURCES = (DRM_IOWR (0xB5, struct_drm_mode_get_plane_res))


DRM_IOCTL_MODE_GETPLANE = (DRM_IOWR (0xB6, struct_drm_mode_get_plane))


DRM_IOCTL_MODE_SETPLANE = (DRM_IOWR (0xB7, struct_drm_mode_set_plane))


DRM_IOCTL_MODE_ADDFB2 = (DRM_IOWR (0xB8, struct_drm_mode_fb_cmd2))


DRM_IOCTL_MODE_OBJ_GETPROPERTIES = (DRM_IOWR (0xB9, struct_drm_mode_obj_get_properties))


DRM_IOCTL_MODE_OBJ_SETPROPERTY = (DRM_IOWR (0xBA, struct_drm_mode_obj_set_property))


DRM_IOCTL_MODE_CURSOR2 = (DRM_IOWR (0xBB, struct_drm_mode_cursor2))


DRM_IOCTL_MODE_ATOMIC = (DRM_IOWR (0xBC, struct_drm_mode_atomic))


DRM_IOCTL_MODE_CREATEPROPBLOB = (DRM_IOWR (0xBD, struct_drm_mode_create_blob))


DRM_IOCTL_MODE_DESTROYPROPBLOB = (DRM_IOWR (0xBE, struct_drm_mode_destroy_blob))


DRM_IOCTL_SYNCOBJ_CREATE = (DRM_IOWR (0xBF, struct_drm_syncobj_create))


DRM_IOCTL_SYNCOBJ_DESTROY = (DRM_IOWR (0xC0, struct_drm_syncobj_destroy))


DRM_IOCTL_SYNCOBJ_HANDLE_TO_FD = (DRM_IOWR (0xC1, struct_drm_syncobj_handle))


DRM_IOCTL_SYNCOBJ_FD_TO_HANDLE = (DRM_IOWR (0xC2, struct_drm_syncobj_handle))


DRM_IOCTL_SYNCOBJ_WAIT = (DRM_IOWR (0xC3, struct_drm_syncobj_wait))


DRM_IOCTL_SYNCOBJ_RESET = (DRM_IOWR (0xC4, struct_drm_syncobj_array))


DRM_IOCTL_SYNCOBJ_SIGNAL = (DRM_IOWR (0xC5, struct_drm_syncobj_array))


DRM_IOCTL_MODE_CREATE_LEASE = (DRM_IOWR (0xC6, struct_drm_mode_create_lease))


DRM_IOCTL_MODE_LIST_LESSEES = (DRM_IOWR (0xC7, struct_drm_mode_list_lessees))


DRM_IOCTL_MODE_GET_LEASE = (DRM_IOWR (0xC8, struct_drm_mode_get_lease))


DRM_IOCTL_MODE_REVOKE_LEASE = (DRM_IOWR (0xC9, struct_drm_mode_revoke_lease))


DRM_IOCTL_SYNCOBJ_TIMELINE_WAIT = (DRM_IOWR (0xCA, struct_drm_syncobj_timeline_wait))


DRM_IOCTL_SYNCOBJ_QUERY = (DRM_IOWR (0xCB, struct_drm_syncobj_timeline_array))


DRM_IOCTL_SYNCOBJ_TRANSFER = (DRM_IOWR (0xCC, struct_drm_syncobj_transfer))


DRM_IOCTL_SYNCOBJ_TIMELINE_SIGNAL = (DRM_IOWR (0xCD, struct_drm_syncobj_timeline_array))


DRM_IOCTL_MODE_GETFB2 = (DRM_IOWR (0xCE, struct_drm_mode_fb_cmd2))


DRM_COMMAND_BASE = 0x40


DRM_COMMAND_END = 0xA0


DRM_EVENT_VBLANK = 0x01


DRM_EVENT_FLIP_COMPLETE = 0x02


DRM_EVENT_CRTC_SEQUENCE = 0x03


def fourcc_code(a, b, c, d):
    return ((((__u32 (ord_if_char(a))).value | ((__u32 (ord_if_char(b))).value << 8)) | ((__u32 (ord_if_char(c))).value << 16)) | ((__u32 (ord_if_char(d))).value << 24))


DRM_FORMAT_BIG_ENDIAN = (1 << 31)


DRM_FORMAT_INVALID = 0


DRM_FORMAT_C8 = (fourcc_code ('C', '8', ' ', ' '))


DRM_FORMAT_R8 = (fourcc_code ('R', '8', ' ', ' '))


DRM_FORMAT_R16 = (fourcc_code ('R', '1', '6', ' '))


DRM_FORMAT_RG88 = (fourcc_code ('R', 'G', '8', '8'))


DRM_FORMAT_GR88 = (fourcc_code ('G', 'R', '8', '8'))


DRM_FORMAT_RG1616 = (fourcc_code ('R', 'G', '3', '2'))


DRM_FORMAT_GR1616 = (fourcc_code ('G', 'R', '3', '2'))


DRM_FORMAT_RGB332 = (fourcc_code ('R', 'G', 'B', '8'))


DRM_FORMAT_BGR233 = (fourcc_code ('B', 'G', 'R', '8'))


DRM_FORMAT_XRGB4444 = (fourcc_code ('X', 'R', '1', '2'))


DRM_FORMAT_XBGR4444 = (fourcc_code ('X', 'B', '1', '2'))


DRM_FORMAT_RGBX4444 = (fourcc_code ('R', 'X', '1', '2'))


DRM_FORMAT_BGRX4444 = (fourcc_code ('B', 'X', '1', '2'))


DRM_FORMAT_ARGB4444 = (fourcc_code ('A', 'R', '1', '2'))


DRM_FORMAT_ABGR4444 = (fourcc_code ('A', 'B', '1', '2'))


DRM_FORMAT_RGBA4444 = (fourcc_code ('R', 'A', '1', '2'))


DRM_FORMAT_BGRA4444 = (fourcc_code ('B', 'A', '1', '2'))


DRM_FORMAT_XRGB1555 = (fourcc_code ('X', 'R', '1', '5'))


DRM_FORMAT_XBGR1555 = (fourcc_code ('X', 'B', '1', '5'))


DRM_FORMAT_RGBX5551 = (fourcc_code ('R', 'X', '1', '5'))


DRM_FORMAT_BGRX5551 = (fourcc_code ('B', 'X', '1', '5'))


DRM_FORMAT_ARGB1555 = (fourcc_code ('A', 'R', '1', '5'))


DRM_FORMAT_ABGR1555 = (fourcc_code ('A', 'B', '1', '5'))


DRM_FORMAT_RGBA5551 = (fourcc_code ('R', 'A', '1', '5'))


DRM_FORMAT_BGRA5551 = (fourcc_code ('B', 'A', '1', '5'))


DRM_FORMAT_RGB565 = (fourcc_code ('R', 'G', '1', '6'))


DRM_FORMAT_BGR565 = (fourcc_code ('B', 'G', '1', '6'))


DRM_FORMAT_RGB888 = (fourcc_code ('R', 'G', '2', '4'))


DRM_FORMAT_BGR888 = (fourcc_code ('B', 'G', '2', '4'))


DRM_FORMAT_XRGB8888 = (fourcc_code ('X', 'R', '2', '4'))


DRM_FORMAT_XBGR8888 = (fourcc_code ('X', 'B', '2', '4'))


DRM_FORMAT_RGBX8888 = (fourcc_code ('R', 'X', '2', '4'))


DRM_FORMAT_BGRX8888 = (fourcc_code ('B', 'X', '2', '4'))


DRM_FORMAT_ARGB8888 = (fourcc_code ('A', 'R', '2', '4'))


DRM_FORMAT_ABGR8888 = (fourcc_code ('A', 'B', '2', '4'))


DRM_FORMAT_RGBA8888 = (fourcc_code ('R', 'A', '2', '4'))


DRM_FORMAT_BGRA8888 = (fourcc_code ('B', 'A', '2', '4'))


DRM_FORMAT_XRGB2101010 = (fourcc_code ('X', 'R', '3', '0'))


DRM_FORMAT_XBGR2101010 = (fourcc_code ('X', 'B', '3', '0'))


DRM_FORMAT_RGBX1010102 = (fourcc_code ('R', 'X', '3', '0'))


DRM_FORMAT_BGRX1010102 = (fourcc_code ('B', 'X', '3', '0'))


DRM_FORMAT_ARGB2101010 = (fourcc_code ('A', 'R', '3', '0'))


DRM_FORMAT_ABGR2101010 = (fourcc_code ('A', 'B', '3', '0'))


DRM_FORMAT_RGBA1010102 = (fourcc_code ('R', 'A', '3', '0'))


DRM_FORMAT_BGRA1010102 = (fourcc_code ('B', 'A', '3', '0'))


DRM_FORMAT_XRGB16161616 = (fourcc_code ('X', 'R', '4', '8'))


DRM_FORMAT_XBGR16161616 = (fourcc_code ('X', 'B', '4', '8'))


DRM_FORMAT_ARGB16161616 = (fourcc_code ('A', 'R', '4', '8'))


DRM_FORMAT_ABGR16161616 = (fourcc_code ('A', 'B', '4', '8'))


DRM_FORMAT_XRGB16161616F = (fourcc_code ('X', 'R', '4', 'H'))


DRM_FORMAT_XBGR16161616F = (fourcc_code ('X', 'B', '4', 'H'))


DRM_FORMAT_ARGB16161616F = (fourcc_code ('A', 'R', '4', 'H'))


DRM_FORMAT_ABGR16161616F = (fourcc_code ('A', 'B', '4', 'H'))


DRM_FORMAT_AXBXGXRX106106106106 = (fourcc_code ('A', 'B', '1', '0'))


DRM_FORMAT_YUYV = (fourcc_code ('Y', 'U', 'Y', 'V'))


DRM_FORMAT_YVYU = (fourcc_code ('Y', 'V', 'Y', 'U'))


DRM_FORMAT_UYVY = (fourcc_code ('U', 'Y', 'V', 'Y'))


DRM_FORMAT_VYUY = (fourcc_code ('V', 'Y', 'U', 'Y'))


DRM_FORMAT_AYUV = (fourcc_code ('A', 'Y', 'U', 'V'))


DRM_FORMAT_XYUV8888 = (fourcc_code ('X', 'Y', 'U', 'V'))


DRM_FORMAT_VUY888 = (fourcc_code ('V', 'U', '2', '4'))


DRM_FORMAT_VUY101010 = (fourcc_code ('V', 'U', '3', '0'))


DRM_FORMAT_Y210 = (fourcc_code ('Y', '2', '1', '0'))


DRM_FORMAT_Y212 = (fourcc_code ('Y', '2', '1', '2'))


DRM_FORMAT_Y216 = (fourcc_code ('Y', '2', '1', '6'))


DRM_FORMAT_Y410 = (fourcc_code ('Y', '4', '1', '0'))


DRM_FORMAT_Y412 = (fourcc_code ('Y', '4', '1', '2'))


DRM_FORMAT_Y416 = (fourcc_code ('Y', '4', '1', '6'))


DRM_FORMAT_XVYU2101010 = (fourcc_code ('X', 'V', '3', '0'))


DRM_FORMAT_XVYU12_16161616 = (fourcc_code ('X', 'V', '3', '6'))


DRM_FORMAT_XVYU16161616 = (fourcc_code ('X', 'V', '4', '8'))


DRM_FORMAT_Y0L0 = (fourcc_code ('Y', '0', 'L', '0'))


DRM_FORMAT_X0L0 = (fourcc_code ('X', '0', 'L', '0'))


DRM_FORMAT_Y0L2 = (fourcc_code ('Y', '0', 'L', '2'))


DRM_FORMAT_X0L2 = (fourcc_code ('X', '0', 'L', '2'))


DRM_FORMAT_YUV420_8BIT = (fourcc_code ('Y', 'U', '0', '8'))


DRM_FORMAT_YUV420_10BIT = (fourcc_code ('Y', 'U', '1', '0'))


DRM_FORMAT_XRGB8888_A8 = (fourcc_code ('X', 'R', 'A', '8'))


DRM_FORMAT_XBGR8888_A8 = (fourcc_code ('X', 'B', 'A', '8'))


DRM_FORMAT_RGBX8888_A8 = (fourcc_code ('R', 'X', 'A', '8'))


DRM_FORMAT_BGRX8888_A8 = (fourcc_code ('B', 'X', 'A', '8'))


DRM_FORMAT_RGB888_A8 = (fourcc_code ('R', '8', 'A', '8'))


DRM_FORMAT_BGR888_A8 = (fourcc_code ('B', '8', 'A', '8'))


DRM_FORMAT_RGB565_A8 = (fourcc_code ('R', '5', 'A', '8'))


DRM_FORMAT_BGR565_A8 = (fourcc_code ('B', '5', 'A', '8'))


DRM_FORMAT_NV12 = (fourcc_code ('N', 'V', '1', '2'))


DRM_FORMAT_NV21 = (fourcc_code ('N', 'V', '2', '1'))


DRM_FORMAT_NV16 = (fourcc_code ('N', 'V', '1', '6'))


DRM_FORMAT_NV61 = (fourcc_code ('N', 'V', '6', '1'))


DRM_FORMAT_NV24 = (fourcc_code ('N', 'V', '2', '4'))


DRM_FORMAT_NV42 = (fourcc_code ('N', 'V', '4', '2'))


DRM_FORMAT_NV15 = (fourcc_code ('N', 'V', '1', '5'))


DRM_FORMAT_P210 = (fourcc_code ('P', '2', '1', '0'))


DRM_FORMAT_P010 = (fourcc_code ('P', '0', '1', '0'))


DRM_FORMAT_P012 = (fourcc_code ('P', '0', '1', '2'))


DRM_FORMAT_P016 = (fourcc_code ('P', '0', '1', '6'))


DRM_FORMAT_P030 = (fourcc_code ('P', '0', '3', '0'))


DRM_FORMAT_Q410 = (fourcc_code ('Q', '4', '1', '0'))


DRM_FORMAT_Q401 = (fourcc_code ('Q', '4', '0', '1'))


DRM_FORMAT_YUV410 = (fourcc_code ('Y', 'U', 'V', '9'))


DRM_FORMAT_YVU410 = (fourcc_code ('Y', 'V', 'U', '9'))


DRM_FORMAT_YUV411 = (fourcc_code ('Y', 'U', '1', '1'))


DRM_FORMAT_YVU411 = (fourcc_code ('Y', 'V', '1', '1'))


DRM_FORMAT_YUV420 = (fourcc_code ('Y', 'U', '1', '2'))


DRM_FORMAT_YVU420 = (fourcc_code ('Y', 'V', '1', '2'))


DRM_FORMAT_YUV422 = (fourcc_code ('Y', 'U', '1', '6'))


DRM_FORMAT_YVU422 = (fourcc_code ('Y', 'V', '1', '6'))


DRM_FORMAT_YUV444 = (fourcc_code ('Y', 'U', '2', '4'))


DRM_FORMAT_YVU444 = (fourcc_code ('Y', 'V', '2', '4'))


DRM_FORMAT_MOD_VENDOR_NONE = 0


DRM_FORMAT_MOD_VENDOR_INTEL = 0x01


DRM_FORMAT_MOD_VENDOR_AMD = 0x02


DRM_FORMAT_MOD_VENDOR_NVIDIA = 0x03


DRM_FORMAT_MOD_VENDOR_SAMSUNG = 0x04


DRM_FORMAT_MOD_VENDOR_QCOM = 0x05


DRM_FORMAT_MOD_VENDOR_VIVANTE = 0x06


DRM_FORMAT_MOD_VENDOR_BROADCOM = 0x07


DRM_FORMAT_MOD_VENDOR_ARM = 0x08


DRM_FORMAT_MOD_VENDOR_ALLWINNER = 0x09


DRM_FORMAT_MOD_VENDOR_AMLOGIC = 0x0a


DRM_FORMAT_RESERVED = ((1 << 56) - 1)


DRM_FORMAT_MOD_NONE = 0


__fourcc_mod_broadcom_param_shift = 8


__fourcc_mod_broadcom_param_bits = 48


def fourcc_mod_broadcom_param(m):
    return (c_int (ord_if_char(((m >> __fourcc_mod_broadcom_param_shift) & ((1 << __fourcc_mod_broadcom_param_bits) - 1))))).value


def fourcc_mod_broadcom_mod(m):
    return (m & (~(((1 << __fourcc_mod_broadcom_param_bits) - 1) << __fourcc_mod_broadcom_param_shift)))


DRM_FORMAT_MOD_ARM_TYPE_AFBC = 0x00


DRM_FORMAT_MOD_ARM_TYPE_MISC = 0x01


AFBC_FORMAT_MOD_BLOCK_SIZE_MASK = 0xf


AFBC_FORMAT_MOD_BLOCK_SIZE_16x16 = 1


AFBC_FORMAT_MOD_BLOCK_SIZE_32x8 = 2


AFBC_FORMAT_MOD_BLOCK_SIZE_64x4 = 3


AFBC_FORMAT_MOD_BLOCK_SIZE_32x8_64x4 = 4


AFBC_FORMAT_MOD_YTR = (1 << 4)


AFBC_FORMAT_MOD_SPLIT = (1 << 5)


AFBC_FORMAT_MOD_SPARSE = (1 << 6)


AFBC_FORMAT_MOD_CBR = (1 << 7)


AFBC_FORMAT_MOD_TILED = (1 << 8)


AFBC_FORMAT_MOD_SC = (1 << 9)


AFBC_FORMAT_MOD_DB = (1 << 10)


AFBC_FORMAT_MOD_BCH = (1 << 11)


AFBC_FORMAT_MOD_USM = (1 << 12)


DRM_FORMAT_MOD_ARM_TYPE_AFRC = 0x02


AFRC_FORMAT_MOD_CU_SIZE_MASK = 0xf


AFRC_FORMAT_MOD_CU_SIZE_16 = 1


AFRC_FORMAT_MOD_CU_SIZE_24 = 2


AFRC_FORMAT_MOD_CU_SIZE_32 = 3


def AFRC_FORMAT_MOD_CU_SIZE_P0(__afrc_cu_size):
    return __afrc_cu_size


def AFRC_FORMAT_MOD_CU_SIZE_P12(__afrc_cu_size):
    return (__afrc_cu_size << 4)


AFRC_FORMAT_MOD_LAYOUT_SCAN = (1 << 8)


__fourcc_mod_amlogic_layout_mask = 0xff


__fourcc_mod_amlogic_options_shift = 8


__fourcc_mod_amlogic_options_mask = 0xff


AMLOGIC_FBC_LAYOUT_BASIC = 1


AMLOGIC_FBC_LAYOUT_SCATTER = 2


AMLOGIC_FBC_OPTION_MEM_SAVING = (1 << 0)


def IS_AMD_FMT_MOD(val):
    return ((val >> 56) == DRM_FORMAT_MOD_VENDOR_AMD)


AMD_FMT_MOD_TILE_VER_GFX9 = 1


AMD_FMT_MOD_TILE_VER_GFX10 = 2


AMD_FMT_MOD_TILE_VER_GFX10_RBPLUS = 3


AMD_FMT_MOD_TILE_GFX9_64K_S = 9


AMD_FMT_MOD_TILE_GFX9_64K_D = 10


AMD_FMT_MOD_TILE_GFX9_64K_S_X = 25


AMD_FMT_MOD_TILE_GFX9_64K_D_X = 26


AMD_FMT_MOD_TILE_GFX9_64K_R_X = 27


AMD_FMT_MOD_DCC_BLOCK_64B = 0


AMD_FMT_MOD_DCC_BLOCK_128B = 1


AMD_FMT_MOD_DCC_BLOCK_256B = 2


AMD_FMT_MOD_TILE_VERSION_SHIFT = 0


AMD_FMT_MOD_TILE_VERSION_MASK = 0xFF


AMD_FMT_MOD_TILE_SHIFT = 8


AMD_FMT_MOD_TILE_MASK = 0x1F


AMD_FMT_MOD_DCC_SHIFT = 13


AMD_FMT_MOD_DCC_MASK = 0x1


AMD_FMT_MOD_DCC_RETILE_SHIFT = 14


AMD_FMT_MOD_DCC_RETILE_MASK = 0x1


AMD_FMT_MOD_DCC_PIPE_ALIGN_SHIFT = 15


AMD_FMT_MOD_DCC_PIPE_ALIGN_MASK = 0x1


AMD_FMT_MOD_DCC_INDEPENDENT_64B_SHIFT = 16


AMD_FMT_MOD_DCC_INDEPENDENT_64B_MASK = 0x1


AMD_FMT_MOD_DCC_INDEPENDENT_128B_SHIFT = 17


AMD_FMT_MOD_DCC_INDEPENDENT_128B_MASK = 0x1


AMD_FMT_MOD_DCC_MAX_COMPRESSED_BLOCK_SHIFT = 18


AMD_FMT_MOD_DCC_MAX_COMPRESSED_BLOCK_MASK = 0x3


AMD_FMT_MOD_DCC_CONSTANT_ENCODE_SHIFT = 20


AMD_FMT_MOD_DCC_CONSTANT_ENCODE_MASK = 0x1


AMD_FMT_MOD_PIPE_XOR_BITS_SHIFT = 21


AMD_FMT_MOD_PIPE_XOR_BITS_MASK = 0x7


AMD_FMT_MOD_BANK_XOR_BITS_SHIFT = 24


AMD_FMT_MOD_BANK_XOR_BITS_MASK = 0x7


AMD_FMT_MOD_PACKERS_SHIFT = 27


AMD_FMT_MOD_PACKERS_MASK = 0x7


AMD_FMT_MOD_RB_SHIFT = 30


AMD_FMT_MOD_RB_MASK = 0x7


AMD_FMT_MOD_PIPE_SHIFT = 33


AMD_FMT_MOD_PIPE_MASK = 0x7

drm_clip_rect = struct_drm_clip_rect

drm_drawable_info = struct_drm_drawable_info

drm_tex_region = struct_drm_tex_region

drm_hw_lock = struct_drm_hw_lock

drm_version = struct_drm_version

drm_unique = struct_drm_unique

drm_list = struct_drm_list

drm_block = struct_drm_block

drm_control = struct_drm_control

drm_ctx_priv_map = struct_drm_ctx_priv_map

drm_map = struct_drm_map

drm_client = struct_drm_client

drm_stats = struct_drm_stats

drm_lock = struct_drm_lock

drm_buf_desc = struct_drm_buf_desc

drm_buf_info = struct_drm_buf_info

drm_buf_free = struct_drm_buf_free

drm_buf_pub = struct_drm_buf_pub

drm_buf_map = struct_drm_buf_map

drm_dma = struct_drm_dma

drm_ctx = struct_drm_ctx

drm_ctx_res = struct_drm_ctx_res

drm_draw = struct_drm_draw

drm_update_draw = struct_drm_update_draw

drm_auth = struct_drm_auth

drm_irq_busid = struct_drm_irq_busid

drm_wait_vblank_request = struct_drm_wait_vblank_request

drm_wait_vblank_reply = struct_drm_wait_vblank_reply

drm_wait_vblank = union_drm_wait_vblank

drm_modeset_ctl = struct_drm_modeset_ctl

drm_agp_mode = struct_drm_agp_mode

drm_agp_buffer = struct_drm_agp_buffer

drm_agp_binding = struct_drm_agp_binding

drm_agp_info = struct_drm_agp_info

drm_scatter_gather = struct_drm_scatter_gather

drm_set_version = struct_drm_set_version

drm_gem_close = struct_drm_gem_close

drm_gem_flink = struct_drm_gem_flink

drm_gem_open = struct_drm_gem_open

drm_get_cap = struct_drm_get_cap

drm_set_client_cap = struct_drm_set_client_cap

drm_prime_handle = struct_drm_prime_handle

drm_syncobj_create = struct_drm_syncobj_create

drm_syncobj_destroy = struct_drm_syncobj_destroy

drm_syncobj_handle = struct_drm_syncobj_handle

drm_syncobj_transfer = struct_drm_syncobj_transfer

drm_syncobj_wait = struct_drm_syncobj_wait

drm_syncobj_timeline_wait = struct_drm_syncobj_timeline_wait

drm_syncobj_array = struct_drm_syncobj_array

drm_syncobj_timeline_array = struct_drm_syncobj_timeline_array

drm_crtc_get_sequence = struct_drm_crtc_get_sequence

drm_crtc_queue_sequence = struct_drm_crtc_queue_sequence

drm_mode_modeinfo = struct_drm_mode_modeinfo

drm_mode_card_res = struct_drm_mode_card_res

drm_mode_crtc = struct_drm_mode_crtc

drm_mode_set_plane = struct_drm_mode_set_plane

drm_mode_get_plane = struct_drm_mode_get_plane

drm_mode_get_plane_res = struct_drm_mode_get_plane_res

drm_mode_get_encoder = struct_drm_mode_get_encoder

drm_mode_get_connector = struct_drm_mode_get_connector

drm_mode_property_enum = struct_drm_mode_property_enum

drm_mode_get_property = struct_drm_mode_get_property

drm_mode_connector_set_property = struct_drm_mode_connector_set_property

drm_mode_obj_get_properties = struct_drm_mode_obj_get_properties

drm_mode_obj_set_property = struct_drm_mode_obj_set_property

drm_mode_get_blob = struct_drm_mode_get_blob

drm_mode_fb_cmd = struct_drm_mode_fb_cmd

drm_mode_fb_cmd2 = struct_drm_mode_fb_cmd2

drm_mode_fb_dirty_cmd = struct_drm_mode_fb_dirty_cmd

drm_mode_mode_cmd = struct_drm_mode_mode_cmd

drm_mode_cursor = struct_drm_mode_cursor

drm_mode_cursor2 = struct_drm_mode_cursor2

drm_mode_crtc_lut = struct_drm_mode_crtc_lut

drm_color_ctm = struct_drm_color_ctm

drm_color_lut = struct_drm_color_lut

hdr_metadata_infoframe = struct_hdr_metadata_infoframe

hdr_output_metadata = struct_hdr_output_metadata

drm_mode_crtc_page_flip = struct_drm_mode_crtc_page_flip

drm_mode_crtc_page_flip_target = struct_drm_mode_crtc_page_flip_target

drm_mode_create_dumb = struct_drm_mode_create_dumb

drm_mode_map_dumb = struct_drm_mode_map_dumb

drm_mode_destroy_dumb = struct_drm_mode_destroy_dumb

drm_mode_atomic = struct_drm_mode_atomic

drm_format_modifier_blob = struct_drm_format_modifier_blob

drm_format_modifier = struct_drm_format_modifier

drm_mode_create_blob = struct_drm_mode_create_blob

drm_mode_destroy_blob = struct_drm_mode_destroy_blob

drm_mode_create_lease = struct_drm_mode_create_lease

drm_mode_list_lessees = struct_drm_mode_list_lessees

drm_mode_get_lease = struct_drm_mode_get_lease

drm_mode_revoke_lease = struct_drm_mode_revoke_lease

drm_mode_rect = struct_drm_mode_rect

drm_event = struct_drm_event

drm_event_vblank = struct_drm_event_vblank

drm_event_crtc_sequence = struct_drm_event_crtc_sequence

# No inserted files

# No prefix-stripping

