package main

import (
	"fmt"
)

// Malaria : .
type Malaria struct {
	// Counts
	NHosts         int
	NInfectedHosts int
	NAntigens      int
	NStrains       int

	Antigens [][]int   // This is the antigens that person would spread to another person.
	Hosts    [][][]int // This is all the strains that infects a particular host.
}

// Parameters : Sets the parameters for a particular run.
type Parameters struct {
	ImmunitySpeed  float64
	InfectionSpeed float64

	Runs int
}

func main() {
	InitiateRunningModel()
	fmt.Println("The end. Congrats!")
}

// InitiateRunningModel : Starts the whole simulation and sets the parameter-grid.
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
	fmt.Println("This set of Parameters, done.", "\n It had the following parameters:", param, "\n It took intime:", time, "\n It took")
}

// ConstructMalariaStruct : Initiates a malaria struct and starts initial conditions.
func ConstructMalariaStruct() {
	var m Malaria

	// Sets initial values.
	m.NHosts = 1000 // Constant
	m.NInfectedHosts = 10
	m.NAntigens = 3
	m.NStrains = 1

	// Make initial antigens
	m.Antigens = make([][]int, m.NHosts)

	for host := 0; host < m.NHosts; host++ {

	}

	// Make initial hosts
	m.Hosts = make([][][]int, m.NHosts)

}

// ChooseEvent : Choose which event should happen with probability proportional to the rates.
func ChooseEvent() {

}

// CalcRates : Calculates all the rates.
func CalcRates(m Malaria, param Parameters) (float64, float64) {
	InfectionRate := param.InfectionSpeed * m.NHosts * (m.NHosts - 1)
	ImmunityRate := param.ImmunitySpeed * m.NInfectedHosts

	return InfectionRate, ImmunityRate
}
