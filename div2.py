import os
from Patterns import FhiPatterns
from ShellCommand import ShellCmd

root = os.getcwd()
tarfile_output = 'FHIaims.out'
tarfile_geometry_in  = 'geometry.in'
tarfile_geometry_out = 'geometry.in.next_step'
tar = os.path.join(root,tarfile_output)

sc = ShellCmd(tar)
#pt = Patterns()
pt = FhiPatterns()
#print(pt.if_success)

# FHIaims.out
if sc.filecheck == True:
	print('Check Initial Energy .....................................')
	# initial energy
	res = sc.execute(sc.pipe(sc.grep(pt.energy_scf[0],headtail='head'),sc.awk(pt.energy_scf[1])))
	print('initialE: {}'.format(res))
	# final energy
	print('Check Final Energy .....................................')
	res = sc.execute(sc.pipe(sc.grep(pt.energy_scf[0],headtail='tail'),sc.awk(pt.energy_scf[1])))
	print('finalE  : {}'.format(res))


	print('Check Success ..............................................')
	cmd = sc.grep(pt.if_success[0])
	success_flag = False
	if sc.execute(cmd) != None:
		success_flag = True
		print('If Success: {} / Cmd: {}'.format(success_flag,cmd))
	print('............................................................')

	print('SCF Energy Check ... based "SCF Converged"')
	# Get Energy ...
	cmd = sc.pipe(sc.pipe(sc.grep(pt.scf_converged[0],'-A 40'),sc.grep(pt.energy_scf[0],file=False)),sc.awk(pt.energy_scf[1]))
	print(cmd)
	print(sc.execute(cmd))
	print('..........................................')

	print('HOMO LUMO Check ... same base')
	base = sc.grep(pt.scf_converged[0],'-B 8','-A 40')

	print('SCF HOMO:')
	all_homo = sc.pipe(sc.pipe(base,sc.grep(pt.property_electronic_homolevel[0],file=False)),sc.awk(pt.property_electronic_homolevel[1]))
	print(sc.execute(all_homo))
	print('')
	init_homo = sc.pipe(sc.pipe(base,sc.grep(pt.property_electronic_homolevel[0],headtail='head',file=False)),sc.awk(pt.property_electronic_homolevel[1]))
	print('Initial HOMO: {}'.format(sc.execute(init_homo)))
	fina_homo = sc.pipe(sc.pipe(base,sc.grep(pt.property_electronic_homolevel[0],headtail='tail',file=False)),sc.awk(pt.property_electronic_homolevel[1]))
	print('Final HOMO: {}'.format(sc.execute(fina_homo)))
	print('.......................................END')


	print('Dipole Check ... same base')
	base = sc.grep(pt.scf_converged[0],'-B 8','-A 40')

	all_dipole = sc.pipe(base,sc.grep(pt.property_dipole[0],file=False))
	print(sc.execute(all_dipole))

	init_dipole = sc.pipe(sc.pipe(base,sc.grep(pt.property_dipole[0],headtail='head',file=False)),sc.awk(pt.property_dipole[1]))
	print('Init Dipole: {}'.format(sc.execute(init_dipole)))
	fina_dipole = sc.pipe(sc.pipe(base,sc.grep(pt.property_dipole[0],headtail='tail',file=False)),sc.awk(pt.property_dipole[1]))
	print('FinalDipole: {}'.format(sc.execute(fina_dipole)))
	print('.......................................END')

	print('Time / Task Check')
	time = sc.pipe(sc.grep(pt.computation_runtime[0]),sc.awk(pt.computation_runtime[1]))
	task = sc.pipe(sc.grep(pt.computation_cores[0]),sc.awk(pt.computation_cores[1]))
	print('Wtime / Tasks : {} / {}'.format(sc.execute(time),sc.execute(task)))
	print('.......................................END')

tarfile_general_out = 'FHIaims.out'
tarfile_geometry_in = 'geometry.in'
tarfile_geometry_out = 'geometry.in.next_step'

file_checklist = [tarfile_general_out,tarfile_geometry_in,tarfile_geometry_out]
success_checklist = []
root = os.getcwd()

for offset, item in enumerate(file_checklist):
	file_checklist[offset] = os.path.join(root,item)

	if os.path.exists(file_checklist[offset]):
		success_checklist.append(True)

print(success_checklist)


print('check geometry ...')
print('initial ...')
sc.set_tarfile(file_checklist[1])
#print(sc.check_tarfile(),sc.get_tarfile_path())

cmd = sc.grep(pt.geometry_cartesian[0])
res = sc.execute(cmd).split('\n')

ini_config = []
fin_config = []
for line in res:
	ini_config.append(line.split())
print(ini_config,len(ini_config))

sc.set_tarfile(file_checklist[2])
cmd = sc.grep(pt.geometry_cartesian[0])
res = sc.execute(cmd).split()

for line in res:
	fin_config.append(line.split())
print(fin_config,len(fin_config))




