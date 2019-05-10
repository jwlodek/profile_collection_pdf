"Define motors related to optics"
from ophyd.status import SubscriptionStatus


class Slits(Device):
    top = Cpt(EpicsMotor, 'T}Mtr')
    bottom = Cpt(EpicsMotor, 'B}Mtr')
    inboard = Cpt(EpicsMotor, 'I}Mtr')
    outboard = Cpt(EpicsMotor, 'O}Mtr')
    ''' TODO : Add later
    xc = Cpt(EpicsMotor, 'XCtr}Mtr')
    xg = Cpt(EpicsMotor, 'XGap}Mtr')
    yc = Cpt(EpicsMotor, 'YCtr}Mtr')
    yg = Cpt(EpicsMotor, 'YGap}Mtr')
    '''

ocm_slits = Slits('XF:28ID1B-OP{Slt:2-Ax:', name='ocm_slits')  # OCM Slits
bdm_slits = Slits('XF:28ID1A-OP{Slt:1-Ax:', name='bdm_slits')  # BD Slits

class SideBounceMono(Device):
    x_wedgemount = Cpt(EpicsMotor, "X}Mtr")
    y_wedgemount = Cpt(EpicsMotor, "Y}Mtr")
    yaw = Cpt(EpicsMotor, "Yaw}Mtr")
    pitch = Cpt(EpicsMotor, "Pitch}Mtr")
    roll = Cpt(EpicsMotor, "Roll}Mtr")
    bend = Cpt(EpicsMotor, "Bend}Mtr")
    twist = Cpt(EpicsMotor, "Twist}Mtr")

sbm = SideBounceMono("XF:28ID1A-OP{Mono:SBM-Ax:", name='sbm')
# Shutters:
#fs = EpicsSignal('XF:28ID1B-OP{PSh:1-Det:2}Cmd', name='fs')  # fast shutter
#temporary fast shutter
# class tempFSShutter:
#
#     def set(self, value):
#         if value == 0:
#             return fb_two_button_shutters.flt4.set('Close')
#         elif value == 1:
#             return fb_two_button_shutters.flt4.set('Open')
#
#     def read(self):
#         return fb_two_button_shutters.read()
#
#     def describe(self):
#         return fb_two_button_shutters.describe()
#
#     def stop(self, success=False):
#         return self.set('close')

# fs = tempFSShutter()

# Close the shutter on stop
# fs.stop = lambda *args, **kwargs: fs.set(0)

class PDFFastShutter(Device):
    cmd = Cpt(EpicsSignal, 'Cmd', kind='omitted')
    status = Cpt(EpicsSignal, 'Sts', kind='omitted')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.st = None
        # TODO: ask CJ to change it downstream to only accept the 'Open' or 'Close' strings (no numbers please!).
        self.setmap = {'Open': 0, 'Close': 1,
                       1: 0, 0: 1}  # MR: this is an inversed logic on the xpdacq side
        self.readmap = {0: 'Open', 1: 'Close'}

    def set(self, val):
        def check_if_done(value, old_value, **kwargs):
            if ((val in ['Open', 1] and value == 0) or
                (val in ['Close', 0] and value == 1)):
                if self.st is not None:
                    self.st._finished()
                    self.st = None
                return True
            return False
        self.cmd.set(self.setmap[val])
        status = SubscriptionStatus(self.status, check_if_done)
        return status

    def get(self):
        return self.readmap[self.cmd.get()]

    def read(self):
        d = super().read()
        d[self.name] = {'value': self.get(), 'timestamp': time.time()}
        return d

    def stop(self, success=False):
        return self.set('Close')


fs = PDFFastShutter('XF:28ID1B-OP{PSh:1-Det:2}', name='fs')


class Mirror(Device):
    y_upstream = Cpt(EpicsMotor, 'YU}Mtr')
    y_downstream_inboard = Cpt(EpicsMotor, 'YDI}Mtr')
    y_downstream_outboard = Cpt(EpicsMotor, 'YDO}Mtr')
    bend_upstream = Cpt(EpicsMotor, 'BndU}Mtr')
    bend_encoder = Cpt(EpicsSignalRO, 'BndU}Pos:Enc-I')
    bend_downstream = Cpt(EpicsMotor, 'BndD}Mtr')
    twist_encoder = Cpt(EpicsSignalRO, 'BndD}Pos:Enc-I')
    # TODO: add coordinated motions later:
    # y_upstream, y_downstream_inboard, y_downstream_outboard

Mirror_VFM = Mirror('XF:28ID1A-OP{Mir:VFM-Ax:', name='Mirror_VFM')

class OpticsTableADC(Device):
    upstream_jack_inboard = Cpt(EpicsMotor, 'YUI}Mtr')
    upstream_jack_outboard = Cpt(EpicsMotor, 'YUO}Mtr')
    downstream_jack_outboard = Cpt(EpicsMotor, 'YD}Mtr')
    X_upstream = Cpt(EpicsMotor, 'XU}Mtr')
    X_downstream = Cpt(EpicsMotor, 'XD}Mtr')
    Z = Cpt(EpicsMotor, 'Z}Mtr')

optics_table_adc = OpticsTableADC(prefix="XF:28ID1B-ES{Tbl:1-Ax:",
                                  name="optics_table_adc")

class SpinnerGoniohead(Device):
    X = Cpt(EpicsMotor, 'X}Mtr')
    Y = Cpt(EpicsMotor, 'Y}Mtr')
    Z = Cpt(EpicsMotor, 'Z}Mtr')
    Ry = Cpt(EpicsMotor, 'Ry}Mtr')

spinner_goniohead = SpinnerGoniohead(prefix="XF:28ID1B-ES{Stg:Smpl-Ax:",
                                     name="spinner_goniohead")
