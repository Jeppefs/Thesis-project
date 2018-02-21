package main

import (
	"fmt"
	"math/rand"
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

	InfectedHosts []int

	Antigens   [][]int8 // This is the antigens that person would spread to another person.
	Infections [][]int8 // This is all the strains that infects a particular host.
	Antibodies [][]bool // The immunities for the antigens in each host.
}

// Parameters : Sets the parameters for a particular run.
type Parameters struct {
	ImmunitySpeed  float64
	InfectionSpeed float64
	MutationSpeed  float64

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
	parameterGrid[0].InfectionSpeed = 1
	parameterGrid[0].ImmunitySpeed = 20
	parameterGrid[0].Runs = 1
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
				m.Antigens[host][antigen] = int8(rand.Intn(m.MaxAntigenValue))
			} else {
				m.Antigens[host][antigen]--
			}
		}
	}

	// Make initial infections
	m.Infections = make([][]int8, m.NHosts)
	for host := 0; host < m.NHosts; host++ {
		m.Infections[host] = make([]int8, m.NAntigens)
		for antigen := 0; antigen < m.NAntigens; antigen++ {
			if host < m.NInfectedHosts {
				m.Infections[host][antigen] = m.Antigens[host][antigen]
			} else {
				m.Infections[host][antigen]--
			}
		}
	}
	// Make initial immunities
	m.Antibodies = make([][]bool, m.NHosts)
	for host := 0; host < m.NHosts; host++ {
		m.Antibodies[host] = make([]bool, m.MaxAntigenValue)
	}

	m.InfectedHosts = make([]int, m.NInfectedHosts)
	for host := 0; host < m.NInfectedHosts; host++ {
		m.InfectedHosts[host] = host
	}

	fmt.Println(m.Antigens, "\n", m.Infections, "\n", m.Antibodies, "\n")
	return m

}

// EventHappens : ...
func (m *Malaria) EventHappens(param Parameters) {
	event := ChooseEvent(m, param)
	event = 0
	switch event {
	case 1:
		m.Spread()
	case 2:
		m.ImmunityGained()
	}
	fmt.Println(event)
	return
}

// ChooseEvent : Choose which event should happen with probability proportional to the rates.
func ChooseEvent(m *Malaria, param Parameters) int {

	rates := CalcRates(m, param)
	ratesTotal := SumSlice(rates)

	choice := rand.Float64()
	rProb := 0.0
	var event int
	for i := 0; i < 2; i++ {
		rProb += rates[i] / ratesTotal
		if choice < rProb {
			event = i
			break
		}
	}

	return event
}

// CalcRates : Calculates all the rates.
func CalcRates(m *Malaria, param Parameters) []float64 {
	r := make([]float64, 3)
	r[0] = param.InfectionSpeed * float64(m.NInfectedHosts) * (float64(m.NHosts))
	r[1] = param.ImmunitySpeed * float64(m.NInfectedHosts)
	//r[2] = param.MutationSpeed * float64(m.NInfectedHosts)
	return r
}

// Spread : Another person gets infected.
func (m *Malaria) Spread() {
	SpreadTo := rand.Intn(r.NHosts)
	SpreadFrom := rand.Intn(r.NInfectedHosts)
	// If spread to is equal to spread from, do not spread.
	if SpreadTo == SpreadFrom {
		return
	}

	return
}

// ImmunityGained : An infected person get immunity from one strain. If that one already exist, the parasite dies.
func (m *Malaria) ImmunityGained() {
	return
}

// CombineParasites : When a host becomes infected with another parasite (so it is inficted buy mulitple parasites), it has a combination
func (m *Malaria) CombineParasites() {
	return
}

// SumSlice : Returns the sum a float64 slice.
func SumSlice(X []float64) float64 {
	sum := 0.0
	for _, x := range X {
		sum += x
	}
	return sum
}
