from north_c9.controller import C9Controller

c9 = C9Controller(address=1, verbose=True)
c9.home()
c9.move_arm(0, 200, 200)