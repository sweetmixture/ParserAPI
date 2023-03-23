import os,sys,csv
import numpy as np

import Pattern #import FhiPattern
from ShellCommand import Shell

pt = Pattern.FhiPattern()

# Target Files
tarfile_list = [pt.geometry_in,pt.geometry_out,pt.app_out]
dirs = [ d for d in os.listdir('./') if 'run_' in d ]
dirs = sorted(dirs,key=lambda x: int(x.split('_')[1]))

root = os.getcwd()
for offset, item in enumerate(dirs):
	dirs[offset] = os.path.join(root,item)


# Files & Success Check
success_checklist = []
sc = Shell()
scg = Shell()

data = []


###### VARIABLES ...
OE  = -2034.812985907
PbE = -589993.362026741
onsiteE = OE + PbE

#Sampling ...
#O1 = [0.03364181,     -0.00000000,     -0.00000000]
#Pb1= [1.96635819,     -0.00000000,     -0.00000000]
sample_config = np.array([0.03364181,-0.00000000,-0.00000000,1.96635819,-0.00000000,-0.00000000])
##################

for item in dirs:

	print('\rRT processing: {}'.format(item),end="")

	checklist = []
	checklist.append(item)

	# file check
	checklist.append(os.path.exists(os.path.join(item,tarfile_list[0])))	# geo in
	checklist.append(os.path.exists(os.path.join(item,tarfile_list[1])))	# geo next
	checklist.append(os.path.exists(os.path.join(item,tarfile_list[2])))	# fhi.ou

	# calculation check
	check = sc.set_tarfile(os.path.join(item,tarfile_list[2]))
	if check == True:	# or sc.check_tarfile()
		cmd =  sc.grep(pt.if_success[0])
		if sc.execute(cmd) != None:
			checklist.append(True)
		else:
			checklist.append(False)

	'''
	if False not in checklist[1:]:
		print('succeed')
	print(checklist)
	sys.exit(1)
	'''

	success_checklist.append(checklist)

	if False not in checklist[1:]:			# Case passes all inspection

		app_out = os.path.join(item,pt.app_out)
		geo_in  = os.path.join(item,pt.geometry_in)
		geo_out = os.path.join(item,pt.geometry_out)

		data_elem = []

		### using app_out

		sc.set_tarfile(app_out)

		### Get Initial/Final E
		initE = sc.execute(sc.pipe(sc.grep(pt.energy_scf[0],headtail='head'),sc.awk(pt.energy_scf[1])))
		finaE = sc.execute(sc.pipe(sc.grep(pt.energy_scf[0],headtail='tail'),sc.awk(pt.energy_scf[1])))
		initdE = float(initE) - onsiteE
		finadE = float(finaE) - onsiteE

		# update
		data_elem.append(initdE)
		data_elem.append(finadE)

		### Get Initial/Final HOMO,LUMO,Eg(HOMO-LUMO GAP)
		base = sc.grep(pt.scf_converged[0],'-B 8','-A 40')

		init_hE = sc.execute(sc.pipe(sc.pipe(base,sc.grep(pt.property_electronic_homolevel[0],headtail='head',file=False)), \
				sc.awk(pt.property_electronic_homolevel[1])))
		init_lE = sc.execute(sc.pipe(sc.pipe(base,sc.grep(pt.property_electronic_lumolevel[0],headtail='head',file=False)), \
				sc.awk(pt.property_electronic_lumolevel[1])))
		init_lu = sc.execute(sc.pipe(sc.pipe(base,sc.grep(pt.property_electronic_homolumogap[0],headtail='head',file=False)), \
				sc.awk(pt.property_electronic_homolumogap[1])))


		fina_hE = sc.execute(sc.pipe(sc.pipe(base,sc.grep(pt.property_electronic_homolevel[0],headtail='tail',file=False)), \
				sc.awk(pt.property_electronic_homolevel[1])))
		fina_lE = sc.execute(sc.pipe(sc.pipe(base,sc.grep(pt.property_electronic_lumolevel[0],headtail='tail',file=False)), \
				sc.awk(pt.property_electronic_lumolevel[1])))
		fina_lu = sc.execute(sc.pipe(sc.pipe(base,sc.grep(pt.property_electronic_homolumogap[0],headtail='tail',file=False)), \
				sc.awk(pt.property_electronic_homolumogap[1])))

		hl = [init_hE,init_lE,init_lu,fina_hE,fina_lE,fina_lu]

		# update
		data_elem.extend(hl)

		### Get Initial/Final Dipole
		#base = sc.grep(pt.scf_converged[0],'-B 8','-A 40')

		init_p = sc.execute(sc.pipe(sc.pipe(base,sc.grep(pt.property_dipole[0],headtail='head',file=False)),sc.awk(pt.property_dipole[1])))
		fina_p = sc.execute(sc.pipe(sc.pipe(base,sc.grep(pt.property_dipole[0],headtail='tail',file=False)),sc.awk(pt.property_dipole[1])))

		p = [init_p,fina_p]

		# update
		data_elem.extend(p)

		########## using 'app_out' ends

		# Geometry - RMSD Measure, (SamplingCentre - SamplePoint)^2/Nvariables
		init_config = []
		scg.set_tarfile(geo_in)
		lines = scg.execute(scg.grep(pt.geometry_cartesian[0])).split('\n')

		for line in lines:
			init_config.extend(line.split()[1:-1])

		delta_config = sample_config - np.array(list(map(lambda x: float(x), init_config)))
		#rmsd = np.linalg.norm(delta_config)/len(init_config)
		rmsd_config = np.linalg.norm(delta_config)/(float(len(init_config))-1.)

		rmsd = [rmsd_config]

		# update
		data_elem.extend(rmsd)

		### using 'app_out', wtime / ptasks
		cmd = sc.grep(pt.computation_runtime[0],headtail='tail')
		wtime = sc.execute(sc.pipe(cmd,sc.awk(pt.computation_runtime[1])))

		cmd = sc.grep(pt.computation_cores[0],headtail='head')
		ptasks = sc.execute(sc.pipe(cmd,sc.awk(pt.computation_cores[1])))
		
		# update
		data_elem.extend(ptasks)
		data_elem.extend(wtime)

		### finalise
		data_elem.append(item)	# logging the path
		data.append(data_elem)	# logging full data

# writing
print('')

fields = ['initE','finaE','inith','initl','inithl','finah','final','finahl','initp','finap','rmsd','ptasks','wtime','src']

with open('res.csv','w') as w:

	cw = csv.writer(w)
	cw.writerow(fields)

	for row in data:

		cw.writerow(row)

