from north_c9.controller import C9Controller

current_address = input('Current C9 Address: ')
c9 = C9Controller(address=int(current_address), verbose=True)

new_address = input('New C9 Address: ')
c9.address(int(new_address))

print(c9.info())