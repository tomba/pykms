#!/usr/bin/env python3

import argparse
import urwid
import kms

parser = argparse.ArgumentParser()
parser.add_argument('-C', '--card', type=int)
parser.add_argument('-c', '--connector', default='')
args = parser.parse_args()


def div_or_zero(n, d):
    return 0 if d == 0 else n / d


def khz_to_ps(khz):
    return 0 if khz == 0 else 1.0 / khz * 1000 * 1000 * 1000


def khz_to_us(khz):
    return 0 if khz == 0 else 1.0 / khz * 1000


def mode_to_str(mode):
    return f'{mode.name}@{mode.vrefresh}{"i" if mode.interlace else ""}'


def polarity_to_tristate(flags, pos_flag, neg_flag):
    if flags & pos_flag:
        return True
    if flags & neg_flag:
        return False
    return 'mixed'


def tristate_to_flag(state, pos_flag, neg_flag):
    if state is True:
        return pos_flag
    if state is False:
        return neg_flag
    return kms.ModeFlag(0)


class IntEditPlus(urwid.IntEdit):
    """IntEdit with +/- shortcuts and a value_changed signal.

    set_int() is a no-op when the displayed value already equals val,
    which preserves cursor position during model-driven re-renders.
    """

    signals = list(urwid.IntEdit.signals) + ['value_changed']

    def __init__(self, caption=''):
        super().__init__(caption, 0)
        self._suppress = False
        self._last_int = 0
        urwid.connect_signal(self, 'change', self._on_change)

    def _on_change(self, _widget, new_text):
        # Treat empty edit text as transient — don't propagate while the
        # user has cleared the field mid-edit.
        if new_text == '':
            return
        new_int = int(new_text)
        if new_int == self._last_int:
            return
        self._last_int = new_int
        if not self._suppress:
            urwid.emit_signal(self, 'value_changed', self, new_int)

    def set_int(self, val):
        val = int(val)
        cur = self.edit_text
        if cur != '' and int(cur) == val:
            return
        self._suppress = True
        pos = self.edit_pos
        new_text = str(val)
        self.set_edit_text(new_text)
        self.edit_pos = min(pos, len(new_text))
        self._suppress = False

    def get_int(self):
        return self._last_int

    def keypress(self, size, key):
        if key == '+':
            self.set_edit_text(str(self._last_int + 1))
            return None
        if key == '-':
            self.set_edit_text(str(self._last_int - 1))
            return None
        return super().keypress(size, key)


class PclkPanel:
    def __init__(self, mode, on_changed):
        self._mode = mode
        self._on_changed = on_changed
        self.w_khz = IntEditPlus('pclk (kHz) ')
        self.w_ps = urwid.Text('')
        urwid.connect_signal(self.w_khz, 'value_changed', self._on_value_changed)
        self.box = urwid.LineBox(
            urwid.Columns([self.w_khz, self.w_ps]),
            title='Pixel clock',
        )

    def _on_value_changed(self, widget, val):
        self._mode.clock = val * 1000
        self._on_changed(source=widget)

    def render(self, source=None):
        khz = self._mode.clock // 1000
        if self.w_khz is not source:
            self.w_khz.set_int(khz)
        self.w_ps.set_text(f'pclk {khz_to_ps(khz):.2f} ps')


class TimingPanel:
    """Two-column view of (disp, fp, sw, bp): deltas and absolute positions."""

    _ROLES = ('disp', 'fp', 'sw', 'bp', 'disp2', 'ss', 'se', 'tot')

    def __init__(self, prefix, title, mode, on_changed):
        self._prefix = prefix
        self._mode = mode
        self._on_changed = on_changed

        labels = {
            'disp':  f'{prefix}disp ',
            'fp':    f'{prefix}fp   ',
            'sw':    f'{prefix}sw   ',
            'bp':    f'{prefix}bp   ',
            'disp2': f'{prefix}disp ',
            'ss':    f'{prefix}ss   ',
            'se':    f'{prefix}se   ',
            'tot':   f'{prefix}tot  ',
        }
        self.widgets = {role: IntEditPlus(labels[role]) for role in self._ROLES}
        for role, w in self.widgets.items():
            urwid.connect_signal(
                w, 'value_changed', self._on_value_changed, user_args=[role]
            )

        col1 = [self.widgets[r] for r in ('disp', 'fp', 'sw', 'bp')]
        col2 = [self.widgets[r] for r in ('disp2', 'ss', 'se', 'tot')]
        self.box = urwid.LineBox(
            urwid.Columns([(15, urwid.Pile(col1)), (15, urwid.Pile(col2))]),
            title=title,
        )

    def _get(self):
        p = self._prefix
        return (
            getattr(self._mode, f'{p}display'),
            getattr(self._mode, f'{p}fp'),
            getattr(self._mode, f'{p}sw'),
            getattr(self._mode, f'{p}bp'),
        )

    def _set(self, disp, fp, sw, bp):
        p = self._prefix
        setattr(self._mode, f'{p}display', disp)
        setattr(self._mode, f'{p}fp', fp)
        setattr(self._mode, f'{p}sw', sw)
        setattr(self._mode, f'{p}bp', bp)

    def _on_value_changed(self, role, widget, val):
        disp, fp, sw, bp = self._get()
        if role in ('disp', 'disp2'):
            disp = val
        elif role == 'fp':
            fp = val
        elif role == 'sw':
            sw = val
        elif role == 'bp':
            bp = val
        elif role == 'ss':
            fp = val - disp
        elif role == 'se':
            sw = val - disp - fp
        elif role == 'tot':
            bp = val - disp - fp - sw
        self._set(disp, fp, sw, bp)
        self._on_changed(source=widget)

    def render(self, source=None):
        disp, fp, sw, bp = self._get()
        values = {
            'disp':  disp,
            'fp':    fp,
            'sw':    sw,
            'bp':    bp,
            'disp2': disp,
            'ss':    disp + fp,
            'se':    disp + fp + sw,
            'tot':   disp + fp + sw + bp,
        }
        for role, w in self.widgets.items():
            if w is not source:
                w.set_int(values[role])


class FlagsPanel:
    _MANAGED = (
        kms.ModeFlag.INTERLACE | kms.ModeFlag.DBLCLK |
        kms.ModeFlag.HSYNC_POS | kms.ModeFlag.HSYNC_NEG |
        kms.ModeFlag.VSYNC_POS | kms.ModeFlag.VSYNC_NEG
    )

    def __init__(self, mode, on_changed):
        self._mode = mode
        self._on_changed = on_changed
        self.w_ilace = urwid.CheckBox('interlace')
        self.w_hsync = urwid.CheckBox('hsync positive', has_mixed=True)
        self.w_vsync = urwid.CheckBox('vsync positive', has_mixed=True)
        self.w_dblclk = urwid.CheckBox('double clock')
        for w in (self.w_ilace, self.w_hsync, self.w_vsync, self.w_dblclk):
            urwid.connect_signal(w, 'change', self._on_state_changed, user_args=[w])
        self.box = urwid.LineBox(
            urwid.Pile([self.w_ilace, self.w_hsync, self.w_vsync, self.w_dblclk]),
            title='Flags',
        )

    def _on_state_changed(self, widget, _emitter, new_state):
        # urwid emits 'change' with the incoming state before applying it,
        # so use new_state for the source and current .state for the others.
        states = {
            self.w_ilace:  self.w_ilace.state,
            self.w_hsync:  self.w_hsync.state,
            self.w_vsync:  self.w_vsync.state,
            self.w_dblclk: self.w_dblclk.state,
        }
        states[widget] = new_state
        f = kms.ModeFlag(int(self._mode.flags) & ~int(self._MANAGED))
        if states[self.w_ilace]:
            f |= kms.ModeFlag.INTERLACE
        if states[self.w_dblclk]:
            f |= kms.ModeFlag.DBLCLK
        f |= tristate_to_flag(
            states[self.w_hsync], kms.ModeFlag.HSYNC_POS, kms.ModeFlag.HSYNC_NEG
        )
        f |= tristate_to_flag(
            states[self.w_vsync], kms.ModeFlag.VSYNC_POS, kms.ModeFlag.VSYNC_NEG
        )
        self._mode.flags = f
        self._on_changed(source=widget)

    def render(self, source=None):
        del source  # set_state(do_callback=False) is enough to avoid re-entry.
        f = self._mode.flags
        self.w_ilace.set_state(bool(f & kms.ModeFlag.INTERLACE), do_callback=False)
        self.w_dblclk.set_state(bool(f & kms.ModeFlag.DBLCLK), do_callback=False)
        self.w_hsync.set_state(
            polarity_to_tristate(f, kms.ModeFlag.HSYNC_POS, kms.ModeFlag.HSYNC_NEG),
            do_callback=False,
        )
        self.w_vsync.set_state(
            polarity_to_tristate(f, kms.ModeFlag.VSYNC_POS, kms.ModeFlag.VSYNC_NEG),
            do_callback=False,
        )


class InfoPanel:
    def __init__(self, mode):
        self._mode = mode
        self.w_line_us = urwid.Text('')
        self.w_line_khz = urwid.Text('')
        self.w_frame_tot = urwid.Text('')
        self.w_frame_us = urwid.Text('')
        self.w_frame_khz = urwid.Text('')
        self.box = urwid.LineBox(
            urwid.Pile([
                self.w_line_us,
                self.w_line_khz,
                urwid.Divider(),
                self.w_frame_tot,
                self.w_frame_us,
                self.w_frame_khz,
            ]),
            title='Info',
        )

    def render(self):
        khz = self._mode.clock // 1000
        htot = self._mode.htotal
        vtot = self._mode.vtotal
        line_us = khz_to_us(khz) * htot
        self.w_line_us.set_text(f'line {line_us:.2f} us')
        self.w_line_khz.set_text(f'line {div_or_zero(khz, htot):.2f} kHz')
        self.w_frame_tot.set_text(f'tot {htot * vtot} pix')
        self.w_frame_us.set_text(f'frame {line_us * vtot / 1000:.2f} ms')
        self.w_frame_khz.set_text(
            f'frame {div_or_zero(khz * 1000, htot * vtot):.2f} Hz'
        )


class KmsModeView:
    def __init__(self):
        self._fb = None
        self._loop = None
        self._rendering = False

        card_path = f'/dev/dri/card{args.card}' if args.card is not None else None
        self._card = kms.Card(card_path)
        res = kms.ResourceManager(self._card)
        self._conn = res.reserve_connector(args.connector)
        self._crtc = res.reserve_crtc(self._conn)

        self._mode = kms.VideoMode()

        self._pclk = PclkPanel(self._mode, self._on_changed)
        self._h = TimingPanel('h', 'Horizontal', self._mode, self._on_changed)
        self._v = TimingPanel('v', 'Vertical', self._mode, self._on_changed)
        self._info = InfoPanel(self._mode)
        self._flags = FlagsPanel(self._mode, self._on_changed)

        mode_buttons = [
            urwid.Button(mode_to_str(m), on_press=self._on_mode_press, user_data=m)
            for m in self._conn.modes
        ]
        modes_box = urwid.LineBox(urwid.Pile(mode_buttons), title='Video modes')

        apply_box = urwid.LineBox(
            urwid.Padding(urwid.Button('apply', on_press=self._on_apply_press))
        )

        main_pile = urwid.Pile([
            modes_box,
            self._pclk.box,
            urwid.Columns([self._h.box, self._v.box]),
            self._info.box,
            self._flags.box,
            apply_box,
        ])

        self._top = urwid.Filler(main_pile, valign='top')

        if self._conn.modes:
            self._load_mode(self._conn.modes[0])

    def _on_changed(self, source=None):
        if self._rendering:
            return
        self._rendering = True
        try:
            self._pclk.render(source=source)
            self._h.render(source=source)
            self._v.render(source=source)
            self._info.render()
            self._flags.render(source=source)
        finally:
            self._rendering = False

    def _load_mode(self, source):
        self._mode.__dict__.update(source.__dict__)
        self._on_changed()

    def _apply_mode(self):
        self._fb = kms.DumbFramebuffer(
            self._card, self._mode.hdisplay, self._mode.vdisplay,
            kms.PixelFormats.XRGB8888,
        )
        kms.draw_test_pattern(self._fb)
        kms.AtomicReq.set_mode(self._conn, self._crtc, self._fb, self._mode)

    def _on_mode_press(self, _widget, mode):
        self._load_mode(mode)

    def _on_apply_press(self, _widget):
        self._apply_mode()

    def _on_unhandled_input(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        if key == 'a':
            self._apply_mode()

    def run(self):
        self._loop = urwid.MainLoop(
            self._top,
            unhandled_input=self._on_unhandled_input,
            handle_mouse=False,
        )
        self._loop.run()
        self._fb = None


def main():
    KmsModeView().run()


if __name__ == '__main__':
    main()
