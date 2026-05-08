# In-Silico Tuberculosis Granuloma Formation and Progression

This repository contains CompuCell3D (CC3D) based simulations modeling the formation and progression of tuberculosis granulomas. Specifically, these models investigate the fate of the granuloma based on the ontogenic origin of the macrophages involved in its formation.

## 📂 Repository Structure

Each main directory in this repository represents a distinct simulation case. Inside each simulation folder, you will find:
* An **XML file** defining the model properties.
* **Two Python files** (`steppables.py` and the main simulation script) setting up and controlling different biological behaviors.
* A **`runcc3d.py` script** intended to be executed via the terminal to run replicates for that specific case.

---

## 🧪 Simulation Scenarios

### `epivar_wo_mec`
**Epithelial Variation without Meclizine Treatment**  
Simulates the baseline granuloma composition variations without any drug interventions. 
* **Composition Variants:** Epithelial vs. Inflammatory proportions tested at 25%, 50%, and 75%.
* **Phenotype Variants:** Varying proportions of oxidized vs. reduced phenotypes in infected macrophages (0%, 50%, and 100% reduced, with complementary oxidized proportions). 
* **Key Variable:** Surface area of the macrophages.

### `midepi_wo_inh`
**Mid-Epithelization without Isoniazid (INH)**  
Simulates the baseline dynamics of granuloma progression based purely on structural cellular changes.
* **Parameter Tested:** Extent of macrophage epithelization adjusted via the surface parameter (15, 16.5, and 18).
* **Objective:** To observe the isolated effect of epithelization on the formation and structural progression of the granuloma.

### `midepi_w_inh`
**Mid-Epithelization with Isoniazid (INH)**  
Simulates the physical barriers to drug efficacy.
* **Parameters Tested:** Extent of macrophage epithelization (surface parameters 15, 16.5, and 18) alongside a separate diffusion field for INH.
* **Objective:** To evaluate how the degree of cellular epithelization impacts the physical penetration and distribution of the INH drug within the granuloma.

### `epivar_w_mec`
**Epithelial Variation with Meclizine & INH Treatment**  
Simulates active, combination pharmacological intervention and its effect on structural composition.
* **Treatment Mechanism:** Simulates Meclizine treatment by switching the epithelial parameter at 10,000 Monte Carlo Steps (MCS), administered alongside INH.
* **Composition Variants:** Epithelial vs. Inflammatory proportions (25%, 50%, 75%).
* **Phenotype Variants:** Oxidized vs. Reduced phenotypes in infected macrophages (0%, 50%, 100% reduced).

---

## 🚀 How to Run

To execute the simulations, navigate to the desired directory in your terminal and run the execution script. For example:

```bash
cd epivar_wo_mec
python runcc3d.py








in-silico tuberculosis Granuloma formation and progression.

CompuCell3D based simulation for formation of granuloma and its fate based on ontogenic origin of the macrophaes involved in the formation. 

Each of the following direcotory contains a simulation folder with a xml and two python files setting up and controlling different aspects of the simlation with steppebles. and runcc3d.py file to be run through terminal to run the replicates of the specific cases of the simulation as mentioned below.

epivar_wo_mec : Variation in epithelial vs inflammatory proportion of the granuloma composition for 25%, 50% and 75% and variation in the proprotion of oxidised and reduced phnoetype of the infected macrophages from 0%, 50% and 100% for reduced and complementry proportions of oxidised infected macrophages. (surface area of the macrophages) without any drug treatment

midepi_wo_inh : Simulations changing the extent of epithelisation of macrophages with changing the surface parameter (15, 16.5, 18) to see the effect on formation and progression of the granuloma dynamics.

midepi_w_inh  : Simulations changing the extent of epithelisation of macrophages with changing the surface parameter (15, 16.5, 18) with separate field of INH to see the effect of epitheliasation on the penetration of the drug

epivar_w_mec  : Epithelial parameter switching at 10,000 MCS simulating the meclizine treatment with INH and variation in epithelial vs inflammatory proportion of the granuloma composition for 25%, 50% and 75% and variation in the proprotion of oxidised and reduced phnoetype of the infected macrophages from 0%, 50% and 100% for reduced and complementry proportions of oxidised infected macrophages. (surface area of the macrophages)

