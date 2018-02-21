package main

import (
	"fmt"
	"time"
)

// Malaria : .
type Malaria struct {
	// Counts
	NHosts         int
	NInfectedHosts int
	NAntigens      int
	NStrains       int

	MaxAntigenValue int

	Antigens   [][]int8 // This is the antigens that person would spread to another person.
	Infections [][]int8 // This is all the strains that infects a particular host.
	Antibodies [][]bool // The immunities for the antigens in each host.
}

// Parameters : Sets the parameters for a particular run.
type Parameters struct {
	ImmunitySpeed  float64
	InfectionSpeed float64

	Runs int
}

type EventTypes struct {
	Spread        int
	Infect        int
	ChangeAntigen int
}

func main() {
	fmt.Println("Starting")
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
	modelTime := 0
	startTime := time.Now()
	m := ConstructMalariaStruct()
	for run := 0; run < param.Runs; run++ {
		m.EventHappens(param)
	}
	endTime := time.Now()
	fmt.Println("This set of Parameters, done.", "\n It had the following parameters:", param, "\n It took intime:", modelTime, "\n It took:", endTime.Sub(startTime))
	fmt.Println(m.NHosts)
	return
}

// ConstructMalariaStruct : Initiates a malaria struct and starts initial conditions.
func ConstructMalariaStruct() Malaria {
	var m Malaria

	// Sets initial values.
	m.NHosts = 20 // Constant
	m.NInfectedHosts = 10
	m.NAntigens = 3
	m.NStrains = 1

	m.MaxAntigenValue = 10

	// Make initial antigens

	m.Antigens = make([][]int8, m.NHosts)
	for host := 0; host < m.NHosts; host++ {
		m.Antigens[host] = make([]int8, m.NAntigens)
		for antigen := 0; antigen < m.NAntigens; antigen++ {
			if host < m.NInfectedHosts {
				m.Antigens[host][antigen] = int8(antigen + 1)
			}
		}
	}

	// Make initial infections
	m.Infections = make([][]int8, m.NHosts)
	for host := 0; host < m.NHosts; host++ {
		m.Infections[host] = make([]int8, m.NAntigens)
		for antigen := 0; antigen < m.NAntigens; antigen++ {
			if host < m.NInfectedHosts {
				m.Infections[host][antigen] = int8(antigen + 1)
			}
		}
	}
	// Make initial immunities
	m.Antibodies = make([][]bool, m.NHosts)
	for host := 0; host < m.NHosts; host++ {
		m.Antibodies[host] = make([]bool, m.MaxAntigenValue)
	}

	return m

}

func (m *Malaria) EventHappens(param *Parameters) {

	return
}

// ChooseEvent : Choose which event should happen with probability proportional to the rates.
func ChooseEvent() {

	rates := CalcRates(m, param)
	ratesTotal := SumSlice(r)

	return
}

// CalcRates : Calculates all the rates.
func CalcRates(m *Malaria, param *Parameters) []float64 {
	r = make([]float64, 3)
	r[0] = param.InfectionSpeed * float64(m.NHosts) * (float64(m.NHosts) - 1)
	r[1] = param.ImmunitySpeed * float64(m.NInfectedHosts)
	r[2] = param.MutationSepped * m.NInfectedHosts

	return r
}

// SumSlice : Returns the sum a float64 slice.
func SumSlice(X []float64) float64 {
	sum := 0.0
	for _, x := range X {
		sum += x
	}
	return sum
}
