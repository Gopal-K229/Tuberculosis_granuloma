from cc3d.core.PySteppables import *
import cc3d.CompuCellSetup as CompuCellSetup
import logging
import numpy as np
import random
import pandas as pd
import os



#logging.info("Simulation started")


epithelial_coeff = input("enter the epithelial coeff: (1 for all epithelial)")
m1m2coeff = input("enter the m1/m2 coeff: (1 for all blue)")

epithelial_coeff = float(epithelial_coeff)
m1m2coeff = float(m1m2coeff)

# epithelial_coeff = 1.0
# m1m2coeff = 1.0

#epithelial=1.0
#mesenchymal=0.0

print("simulation started with epithelial coeff:", epithelial_coeff)
print("simulation started with m1/m2 coeff:", m1m2coeff)


class fielddd(SteppableBasePy):
	def __init__(self, frequency=1): #frequency from 1 to 200
		SteppableBasePy.__init__(self, frequency)
		
	def step(self, mcs):
		if mcs <= 5000:
			theField = self.field.inh
			for x, y, z in self.every_pixel(): 
				theField[x,y,z] = 0.0

class inhkilling(SteppableBasePy):
	def __init__(self, frequency=1):
		SteppableBasePy.__init__(self, frequency)
	def get_cell_center(self, cell):
		return np.array([cell.xCOM, cell.yCOM, cell.zCOM])
	def step(self, mcs):
		inh_limit = 3.0
		inh_field = self.field.inh
		for cell in self.cell_list:
			if cell.type == self.MTB:
				x, y, z = int(cell.xCOM), int(cell.yCOM), int(cell.zCOM)
				inh_concentration = inh_field[x, y, z]
				if inh_concentration > inh_limit and random.random() < 0.05:
					self.delete_cell(cell)


class mac_recruitment_Steppable(SteppableBasePy):
	def __init__(self, frequency=1):
		SteppableBasePy.__init__(self, frequency)

	def start(self):

		self.macro = self.cell_type.macro
		self.Tcell = self.cell_type.Tcell

	def step(self, mcs):
		# if mcs<10000:
		# 	epithelial_coeff = 1.0
		# else:
		# 	epithelial_coeff = 0.0

		# Random recruitment of cells based on MCS (Monte Carlo Step)
		chem_field = self.field.attr  # Make sure 'attr' is a valid field
		x = random.randint(80, 85)
		y = random.randint(13, 18)

		# logging.debug(f"Step {mcs}: Random recruitment at (x, y): ({x}, {y})")

		# Macro recruitment after MCS 250
		if 250 < mcs and random.random() < 0.1:
			cell = self.new_cell(self.macro)
			self.cell_field[x:x+3, y:y+3, 0] = cell
			# logging.info(f"Macro cell created at (x, y): ({x}, {y})")

			# Assign surface properties based on epithelial coefficient
			if mcs<10000:
				if random.random() < epithelial_coeff:
					cell.targetSurface = 15
					cell.lambdaSurface = 10.0
					# logging.debug(f"Cell surface set: targetSurface=15, lambdaSurface=10.0")
				else:
					cell.targetSurface = 18
					cell.lambdaSurface = 10.0
			else:
				cell.targetSurface = 18
				cell.lambdaSurface = 10.0
		# T-cell recruitment after MCS 1500
		if mcs > 1500 and mcs % 5 == 0 and random.random() < 0.1:
			cell = self.new_cell(self.Tcell)
			self.cell_field[x:x+3, y:y+3, 0] = cell

			
class SurfaceSteppable(SteppableBasePy):
	def __init__(self, frequency=1): #frequency from 1 to 200
		SteppableBasePy.__init__(self, frequency)
	def start(self):
		for cell in self.cell_list_by_type(self.MTB):	
			cell.targetSurface=5
			cell.lambdaSurface=50.0	
		for cell in self.cell_list_by_type(self.TCELL):	
			cell.targetSurface=12
			cell.lambdaSurface=10.0
		
	def step(self, mcs):
		if mcs>1500:
			for cell in self.cell_list_by_type(self.MTB):	
				cell.targetSurface=5
				cell.lambdaSurface=50.0	
			for cell in self.cell_list_by_type(self.TCELL):	
				cell.targetSurface=12
				cell.lambdaSurface=10.0

		if mcs>10000:
			for cell in self.cell_list:
				if cell.type == self.MACRO or cell.type == self.M2 or cell.type == self.INF_MAC:
					cell.targetSurface = 18
					cell.lambdaSurface = 10.0



#Steppeble for killing infected macrophages by T cells. 	
df4=[]
class inf_mac_killingSteppable(SteppableBasePy):
	def __init__(self, frequency=500): #frequency from 1 to 200
		SteppableBasePy.__init__(self, frequency) 
	def step(self, mcs):
		type_map = {
				1: "mtb",
				2: "macro",
				3: "inf_mac",
				4: "Tcell",
				5: "m2"
			}
		cells_to_delete = []
		for cell in self.cell_list:
			if cell.type == self.TCELL:
				for neighbor, commonSurfaceArea in self.get_cell_neighbor_data_list(cell):
					if neighbor and random.random()<0.005:
						if neighbor.type == self.INF_MAC or neighbor.type == self.M2:
							kill_data = [cell.id, cell.xCOM, cell.yCOM, neighbor.id, type_map.get(neighbor.type), neighbor.xCOM, neighbor.yCOM, mcs]
							df4.append(kill_data)
							self.delete_cell(neighbor)
		dataframe4 = pd.DataFrame(df4, columns=['tcellid', 'tcellx', 'tcelly', 'neighborid','neighbor_type', 'neighborx', 'neighbory', 'mcs'])
		output_dir = self.output_dir
		if output_dir is not None:
			output_path4 = Path(output_dir).joinpath('cell_killing' + '.csv')
			with open(output_path4, 'w') as fout:
				dataframe4.to_csv(output_path4, index=False)


		
# To 	create two types of infected cells inf_mac and m2 with a certain probability. 						
class InfectionSteppable(SteppableBasePy):
	def __init__(self, frequency=1):
		SteppableBasePy.__init__(self, frequency)
	def step(self, mcs):
		# if mcs<10000:
		# 	epithelial_coeff = 1.0
		# else:
		# 	epithelial_coeff = 0.0

		cells_to_delete = []
		for cell in self.cell_list:
			if cell.type == self.MACRO:
				for neighbor, commonSurfaceArea in self.get_cell_neighbor_data_list(cell):
					if neighbor and neighbor.type == self.MTB:
						if random.random() < m1m2coeff: # 0.75 was original
							cell.type = self.INF_MAC
							cell.dict['timer'] = 0
							cell.dict['timer_threshold'] = 1500
							if mcs<10000:
								if random.random()<epithelial_coeff:								
									cell.targetSurface=15
									cell.lambdaSurface=10.0
								else:
									cell.targetSurface=18
									cell.lambdaSurface=10.0
							else:
								cell.targetSurface=18
								cell.lambdaSurface=10.0
							self.delete_cell(neighbor)
						else:
							cell.type = self.M2
							cell.dict['timer'] = 0
							cell.dict['timer_threshold'] = 1500
							if mcs<10000:
								if random.random()<epithelial_coeff:								
									cell.targetSurface=15
									cell.lambdaSurface=10.0
								else:
									cell.targetSurface=18
									cell.lambdaSurface=10.0
							else:
								cell.targetSurface=18
								cell.lambdaSurface=10.0
							self.delete_cell(neighbor)

			
class CellTypeConverterSteppable(SteppableBasePy):
	def __init__(self, frequency=1):
		SteppableBasePy.__init__(self, frequency)
	def start(self):
		pass
	def get_cell_center(self, cell):
		return np.array([cell.xCOM, cell.yCOM, cell.zCOM])
	def step(self, mcs):
		cells_to_convert = []
		cells_to_delete = []
		for cell in self.cell_list_by_type(self.INF_MAC):
			cell.dict['timer'] = cell.dict.get('timer', 0) + 1
			if cell.dict['timer'] >= cell.dict['timer_threshold']:
				cells_to_convert.append(cell)
		for cell in cells_to_convert:
			random_iter = random.random()
			if random_iter < 0.1:
				cell.type = self.MACRO
				cell.dict['timer'] = 0
			else:
				center = self.get_cell_center(cell)
				self.delete_cell(cell)
				for bac_num in range(6):
					new_cell = self.new_cell(self.MTB)
					offset = np.random.uniform(-1, 1, 3)
					x = int(center[0] + offset[0])
					y = int(center[1] + offset[1])
					z = int(center[2] + offset[2])
					x = max(0, min(x, self.dim.x - 1))
					y = max(0, min(y, self.dim.y - 1))
					z = max(0, min(z, self.dim.z - 1))
					self.cell_field[x, y, z] = new_cell
		for cell in self.cell_list_by_type(self.M2):
			cell.dict['timer'] = cell.dict.get('timer', 0) + 1
			if cell.dict['timer'] >= cell.dict['timer_threshold']:
				cells_to_delete.append(cell)
		for cell in cells_to_delete:
			self.delete_cell(cell)


class Hypoxia_deathSteppable(SteppableBasePy):
	def __init__(self, frequency=1):
		SteppableBasePy.__init__(self, frequency)
	def get_cell_center(self, cell):
		return np.array([cell.xCOM, cell.yCOM, cell.zCOM])
	def step(self, mcs):
		oxy_limit = 25.0
		cell_to_convert = []
		chemical_field = self.field.oxy
		if mcs %10 == 0 :
			for cell in self.cell_list:
				if cell.type == self.MACRO or cell.type == self.TCELL or cell.type == self.M2:
					x, y, z = int(cell.xCOM), int(cell.yCOM), int(cell.zCOM)
					oxy_concentration = chemical_field[x, y, z]
					if oxy_concentration < oxy_limit and random.random() < 0.05:
						self.delete_cell(cell)
				elif cell.type == self.INF_MAC:
					x, y, z = int(cell.xCOM), int(cell.yCOM), int(cell.zCOM)
					oxy_concentration = chemical_field[x, y, z]
					if oxy_concentration < oxy_limit and random.random() < 0.05:
						cell_to_convert.append(cell)
			for cell in cell_to_convert:
				center = self.get_cell_center(cell)
				self.delete_cell(cell)
				for bac_num in range(2):
					new_cell = self.new_cell(self.MTB)
					offset = np.random.uniform(-1, 1, 3)
					x = int(center[0] + offset[0])
					y = int(center[1] + offset[1])
					z = int(center[2] + offset[2])
					x = max(0, min(x, self.dim.x - 1))
					y = max(0, min(y, self.dim.y - 1))
					z = max(0, min(z, self.dim.z - 1))
					self.cell_field[x, y, z] = new_cell

					
df1=[]
df2=[]
df3=[]
df5=[]
class OutputFileSteppable(SteppableBasePy):
	def __init__ (self, frequency=1):
		SteppableBasePy.__init__(self, frequency)
		
	def step(self, mcs):
		chemical_field1 = self.field.attr
		chemical_field2 = self.field.oxy
		chemical_field3 = self.field.inh
		type_map = {
				1: "mtb",
				2: "macro",
				3: "inf_mac",
				4: "Tcell",
				5: "m2"
			}
		# logging.info(f"OutputFileSteppable1 at {mcs}: {str(e)}")
		if mcs %50 ==0:
			for cell in self.cell_list:
				com = (cell.xCOM, cell.yCOM, cell.zCOM)
				attr_concentration = chemical_field1[com]
				oxy_concentration = chemical_field2[com]
				inh_concentration = chemical_field3[com]
				cell_data = [cell.id, type_map.get(cell.type, "unknown"), cell.xCOM, cell.yCOM, attr_concentration, oxy_concentration, inh_concentration, mcs]
				df1.append(cell_data)
			dataframe1 = pd.DataFrame(df1, columns=['cell_id', 'cell_type', 'cell_xcoordinate','cell_ycoordinate', 'attr_concentration', 'oxy_concentration', 'inh_concentration', 'mcs'])
		# logging.info(f"OutputFileSteppable2 at {mcs}: {str(e)}")
		if mcs %50 ==0:
			cols = 	np.arange(0.0,100.0, 5)
			oxy_con_list = []
			oxy_con_list.append(mcs)
			for i in np.arange(5.0,100.0, 5):
				oxy_con = chemical_field2[i, 15, 0]
				oxy_con_list.append(oxy_con)
			df2.append(oxy_con_list)
			dataframe2 = pd.DataFrame(df2, columns = cols)
		# logging.info(f"OutputFileSteppable3 at {mcs}: {str(e)}")
		if mcs %50 ==0:
			cols = 	np.arange(0.0,100.0, 5)
			attr_con_list = []
			attr_con_list.append(mcs)
			for i in np.arange(5.0,100.0, 5):
				attr_con = chemical_field1[i, 15, 0]
				attr_con_list.append(attr_con)
			df3.append(attr_con_list)
			dataframe3 = pd.DataFrame(df3, columns = cols)
		if mcs %50 ==0:
			cols = 	np.arange(0.0,100.0, 5)
			inh_con_list = []
			inh_con_list.append(mcs)
			for i in np.arange(5.0,100.0, 5):
				inh_con = chemical_field3[i, 15, 0]
				inh_con_list.append(inh_con)
			df5.append(inh_con_list)
			dataframe5 = pd.DataFrame(df5, columns = cols)
		
		# logging.info(f"OutputFileSteppable4 at {mcs}: {str(e)}")
		output_dir = self.output_dir
		if output_dir is not None:

			output_path1 = Path(output_dir).joinpath('CellBasedOutput' + '.csv')
			with open(output_path1, 'w') as fout:
				dataframe1.to_csv(output_path1, index=False)

			output_path2 = Path(output_dir).joinpath('OxygenConcentration' + '.csv')
			with open(output_path2, 'w') as fout:
				dataframe2.to_csv(output_path2, index=False)

			output_path3 = Path(output_dir).joinpath('AttrConcentration' + '.csv')
			with open(output_path3, 'w') as fout:
				dataframe3.to_csv(output_path3, index=False)

			output_path4 = Path(output_dir).joinpath('InhConcentration' + '.csv')
			with open(output_path4, 'w') as fout:
				dataframe5.to_csv(output_path4, index=False)

				
			
			
			
		
			
			
					
