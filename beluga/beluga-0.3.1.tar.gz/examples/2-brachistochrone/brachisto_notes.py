"""
Working Version
"""
"""
beluga.py:111: states: ['x', 'y', 'v', 'lamX', 'lamY', 'lamV']
beluga.py:111: states_units: ['m', 'm', 'm/s', 's/m', 's/m', 's**2/m']
beluga.py:111: deriv_list: ['tf*v*cos(theta)', 'tf*v*sin(theta)', 'g*tf*sin(theta)', '0', '0', 'tf*(-lamX*cos(theta) - lamY*sin(theta))']
beluga.py:111: dynamical_parameters: ['tf']
beluga.py:111: dynamical_parameters_units: ['s']
beluga.py:111: nondynamical_parameters: ['lagrange_initial_1', 'lagrange_initial_2', 'lagrange_initial_3', 'lagrange_terminal_1', 'lagrange_terminal_2']
beluga.py:111: nondynamical_parameters_units: ['s/m', 's/m', 's**2/m', 's/m', 's/m']
beluga.py:111: control_list: ['theta']
beluga.py:111: controls: ['theta']
beluga.py:111: hamiltonian: g*lamV*sin(theta) + lamX*v*cos(theta) + lamY*v*sin(theta) + 1
beluga.py:111: hamiltonian_units: s
beluga.py:111: num_states: 6
beluga.py:111: dHdu: [g*lamV*cos(theta) - lamX*v*sin(theta) + lamY*v*cos(theta)]
beluga.py:111: bc_initial: ['x', 'y', 'v', 'lagrange_initial_1 + lamX', 'lagrange_initial_2 + lamY', 'lagrange_initial_3 + lamV']
beluga.py:111: bc_terminal: ['x - x_f', 'y - y_f', '-lagrange_terminal_1 + lamX', '-lagrange_terminal_2 + lamY', 'lamV', 'g*lamV*sin(theta) + lamX*v*cos(theta) + lamY*v*sin(theta) + 1']
beluga.py:111: control_options: [{'theta': '-2*atan(lamX*v/(g*lamV + lamY*v) - sqrt(g**2*lamV**2 + 2*g*lamV*lamY*v + lamX**2*v**2 + lamY**2*v**2)/(g*lamV + lamY*v))'}, {'theta': '-2*atan(lamX*v/(g*lamV + lamY*v) + sqrt(g**2*lamV**2 + 2*g*lamV*lamY*v + lamX**2*v**2 + lamY**2*v**2)/(g*lamV + lamY*v))'}]
beluga.py:111: num_controls: 1
"""
"""
Not Working Version
"""
"""
beluga.py:111: states: ['x', 'y', 'v', 't', 'lamX', 'lamY', 'lamV', 'lamT']
beluga.py:111: states_rates: ['t*v*cos(theta)', 't*v*sin(theta)', 'g*t*sin(theta)', '0', '0', '0', 't*(-lamX*cos(theta) - lamY*sin(theta))', '0']
beluga.py:111: states_units: ['m', 'm', 'm/s', 's', 's/m', 's/m', 's**2/m', '1']
beluga.py:111: dynamical_parameters: []
beluga.py:111: dynamical_parameters_units: []
beluga.py:111: nondynamical_parameters: ['lagrange_initial_1', 'lagrange_initial_2', 'lagrange_initial_3', 'lagrange_terminal_1', 'lagrange_terminal_2']
beluga.py:111: nondynamical_parameters_units: ['s/m', 's/m', 's**2/m', 's/m', 's/m']
beluga.py:111: control_list: ['theta']
beluga.py:111: controls: ['theta']
beluga.py:111: hamiltonian: g*lamV*sin(theta) + lamX*v*cos(theta) + lamY*v*sin(theta) + 1
beluga.py:111: hamiltonian_units: s
beluga.py:111: num_states: 8
beluga.py:111: dHdu: [g*lamV*cos(theta) - lamX*v*sin(theta) + lamY*v*cos(theta)]
beluga.py:111: bc_initial: ['x', 'y', 'v', 'lagrange_initial_1 + lamX', 'lagrange_initial_2 + lamY', 'lagrange_initial_3 + lamV', 'lamT']
beluga.py:111: bc_terminal: ['x - x_f', 'y - y_f', '-lagrange_terminal_1 + lamX', '-lagrange_terminal_2 + lamY', 'lamV', 'lamT']
beluga.py:111: control_options: [{'theta': '-2*atan(lamX*v/(g*lamV + lamY*v) - sqrt(g**2*lamV**2 + 2*g*lamV*lamY*v + lamX**2*v**2 + lamY**2*v**2)/(g*lamV + lamY*v))'}, {'theta': '-2*atan(lamX*v/(g*lamV + lamY*v) + sqrt(g**2*lamV**2 + 2*g*lamV*lamY*v + lamX**2*v**2 + lamY**2*v**2)/(g*lamV + lamY*v))'}]
beluga.py:111: num_controls: 1
"""
