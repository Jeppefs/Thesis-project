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

	MaxAntigenValue int // The maximum number an antigen can have

	InfectedHosts []int // A list of hosts that are infected by one or more malaria strains
	Lookout       []int // This is the current antigen index which they a looking to immunize against. When the immunization method is chosen, this is the point where it checks if is immune and get immunity towards if it isnt't.

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

	m.Lookout = make([]int, m.NHosts)

	//fmt.Println(m.Antigens, "\n", m.Infections, "\n", m.Antibodies, "\n")
	return m

}

// EventHappens : ...
func (m *Malaria) EventHappens(param Parameters) {
	event := ChooseEvent(m, param)
	event = 0
	switch event {
	case 0:
		m.Spread()
	case 1:
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

	spreadTo := rand.Intn(m.NHosts)
	spreadFrom := rand.Intn(m.NInfectedHosts)
	// If spread to is equal to spread from, do not spread.
	if spreadTo == spreadFrom {
		return
	}
	m.InfectHost(spreadTo, spreadFrom)

	return
}

// InfectHost :
func (m *Malaria) InfectHost(spreadTo int, spreadFrom int) {
	// Check if the person spreading to has any infections. If true make him sick. If false append the parasite.
	if m.Infections[spreadTo][0] < 0 {
		for antigenSpot := 0; antigenSpot < m.NAntigens; antigenSpot++ {
			m.Infections[spreadTo][antigenSpot] = m.Antigens[spreadFrom][antigenSpot]
			m.Antigens[spreadTo][antigenSpot] = m.Antigens[spreadFrom][antigenSpot]
		}
	} else {
		for i := 0; i < m.NAntigens; i++ {
			m.Infections[spreadTo] = append(m.Infections[spreadTo], m.Antigens[spreadFrom][i])
		}
		m.CombineParasites(spreadTo)
	}
	return
}

// ImmunityGained : An infected person get immunity from one strain. If that one already exist, the parasite dies.
func (m *Malaria) ImmunityGained() {
	infectedHost := m.InfectedHosts[rand.Intn(m.NInfectedHosts)]
	if m.Antibodies[infectedHost][m.Lookout[infectedHost]] {

	} else {
		// If at end, make him healthy
		// Make immunity in the hosts antibody and set the lookout one up
		m.Antibodies[infectedHost][m.Antigens[infectedHost][m.Lookout[infectedHost]]] = true
		m.Lookout[infectedHost]++
		if m.Lookout[infectedHost] > 2 {
			m.RemoveParasite(infectedHost)
		}
	}
	return
}

// RemoveParasite :  Removes a parasite from a host after immunization
func (m *Malaria) RemoveParasite(host int) {
	m.Antigens[host] = append(m.Antigens[host][:0], m.Antigens[host][:m.NAntigens]...)
}

// CombineParasites : When a host becomes infected with another parasite (so it is inficted buy mulitple parasites), it has a combination
func (m *Malaria) CombineParasites(host int) {
	nParasites := len(m.Antigens[host]) / m.NAntigens
	for antigen := 0; antigen < m.NAntigens; antigen++ {
		randomNumber := rand.Intn(nParasites)
		fmt.Println(antigen+randomNumber*m.NAntigens, m.Infections[host])
		m.Antigens[host][antigen] = m.Infections[host][antigen+randomNumber*m.NAntigens]
	}
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
