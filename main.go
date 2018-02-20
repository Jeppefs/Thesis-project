package main

import (
	"fmt"
)

type Malaria struct {
	Antigens []int
	Hosts    [][][]int

	NHosts         float64
	NInfectedHosts float64
}

type Parameters struct {
	ImmunitySpeed  float64
	InfectionSpeed float64

	Runs int
}

func main() {

	fmt.Println("The end. Congrats!")
}

// RunMalariaModel : Starts the whole simulation. Also sets parameters and calls the saving function.
func InitiateRunningModel() {
	parameterGrid := MakeParameterGrid()
	for i := 0; i < len(parameterGrid); i++ {
		RunMalariaModel(parameterGrid[i])
	}
}

// MakeParameterGrid : Creates a parameter grid to search through. Also where settings a applied.
func MakeParameterGrid() []Parameters {
	parameterGrid := make([]Parameters, 1)
	parameterGrid[0].ImmunitySpeed = 1
	parameterGrid[0].InfectionSpeed = 1
	parameterGrid[0].Runs = 1000
	return parameterGrid
}

// RunMalariaModel : Starts the run of the malaria model
func RunMalariaModel(param Parameters) {
	time := 0
	runTime := 0
	for run := 0; run < param.Runs; run++ {

	}
	fmt.Println("This set of Parameters, done. \n It had the following parameters:", parameterGrid[i], "\n It took intime:", time, "\n It took" "\n")
}

func ConstructMalariaStruct() {

}

func ChooseEvent() {

}

// CalcRates : Calculates all the rates.
func CalcRates(m Malaria, param Parameters) (float64, float64) {
	InfectionRate := param.InfectionSpeed * m.NHosts * (m.NHosts - 1)
	ImmunityRate := param.ImmunitySpeed * m.NInfectedHosts

	return InfectionRate, ImmunityRate
}
