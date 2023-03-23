'''
	Patterns ...
'''

class Pattern():

	def __init__(self):
		pass

	def load_patterns(self):
		NotImplemented
		# 'pattern', 'token', 'arg1', 'arg2', ... ???

class FhiPattern(Pattern):

	control = 'control.in'
	geometry_in  = 'geometry.in'
	geometry_out = geometry_in + '.next_step'
	app_out = 'FHIaims.out'

	def __init__(self):

		# files
		self.fhiaims_geometry_input  = 'geometry.in'
		self.fhiaims_geometry_ouptut = 'geometry.in.next_step'
		self.fhiaims_control         = 'control.in'

		'''
			patterns may be used for "grep"
		'''

		# possible retreiving contents
		
		self.if_success    = ("'Have a nice day.'",None)

		# energy related
		self.energy_scf     = ("'| Total energy corrected        :'",'6')			# energy after scf ... might need further consideration
		
		# geometry related
		self.geometry_cartesian = ("'atom'",None)

		# scf related
		self.scf_converged = ("'Self-consistency cycle converged.'",None)			# -B 8 to get homo-lumo info

		# property related
		self.property_dipole = ("'| Absolute dipole moment'",'6')
		self.property_dipole_x = ("'| Total dipole moment'",'7')
		self.property_dipole_y = ("'| Total dipole moment'",'8')
		self.property_dipole_z = ("'| Total dipole moment'",'9')

		self.property_electronic_homolevel  = ("'Highest occupied state'",'6')
		self.property_electronic_lumolevel  = ("'Lowest unoccupied state'",'6')
		self.property_electronic_homolumogap= ("'Overall HOMO-LUMO gap'",'4')

		# computation related
		self.computation_runtime = ("'| Total time                                 :'",'5')
		self.computation_cores   = ("'parallel tasks'",'2')
