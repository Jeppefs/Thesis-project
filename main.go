/*
	TODO:
	- Make a delete function
	- Write test for death method
	- Write test for muation method
*/

package main

import (
	"fmt"
	"math/rand"
	"os"
	"strconv"
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
	DeathSpeed     float64

	Runs int
}

// MakeParameterGrid : Creates a parameter grid to search through. Also where settings a applied.
func MakeParameterGrid() []Parameters {
	gridsize := 5

	parameterGrid := make([]Parameters, gridsize)

	for i := 0; i < gridsize; i++ {
		parameterGrid[i].InfectionSpeed = 1.0
		parameterGrid[i].ImmunitySpeed = 10000.0 + 1000.0*float64(i)
		parameterGrid[i].MutationSpeed = 0.0
		parameterGrid[i].DeathSpeed = 1

		parameterGrid[i].Runs = 5000000
	}

	return parameterGrid
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

// RunMalariaModel : Starts the run of the malaria model
func RunMalariaModel(param Parameters) {
	modelTime := 0
	startTime := time.Now()

	filename := "text" + strconv.Itoa(int(param.ImmunitySpeed))
	file, err := os.Create("data/" + filename + ".txt")
	check(err)

	m := ConstructMalariaStruct()
	for run := 0; run < param.Runs; run++ {
		m.EventHappens(param)
		if run%10 == 0 {
			fmt.Fprintf(file, "%v \n", m.NInfectedHosts)
			if run%100000 == 0 {
				fmt.Println(run)
			}
		}
		if m.NInfectedHosts == 0 {
			fmt.Println("Malaria is dead in", run, "runs")
			fmt.Fprintf(file, "%v \n", m.NInfectedHosts)
			break
		}
	}
	endTime := time.Now()

	file.Close()

	fmt.Println("This set of Parameters, done.", "\n It had the following parameters:", param, "\n It took intime:", modelTime, "\n It took:", endTime.Sub(startTime))
	fmt.Println(m.NHosts)

	return
}

// ConstructMalariaStruct : Initiates a malaria struct and starts initial conditions.
func ConstructMalariaStruct() Malaria {
	var m Malaria

	// Sets initial values.
	m.NHosts = 10000 // Constant
	m.NInfectedHosts = m.NHosts / 100
	m.NAntigens = 3
	m.NStrains = 1

	m.MaxAntigenValue = 10

	// Make initial antigens

	m.Antigens = make([][]int8, m.NHosts)
	for host := 0; host < m.NHosts; host++ {
		m.Antigens[host] = make([]int8, m.NAntigens)
		for antigen := 0; antigen < m.NAntigens; antigen++ {
			m.Antigens[host][antigen] = int8(rand.Intn(m.MaxAntigenValue))
		}
	}

	// Make initial infections
	m.Infections = make([][]int8, m.NHosts)
	for host := 0; host < m.NInfectedHosts; host++ {
		m.Infections[host] = make([]int8, m.NAntigens)
		for antigen := 0; antigen < m.NAntigens; antigen++ {
			m.Infections[host][antigen] = m.Antigens[host][antigen]
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
	switch event {
	case 0:
		m.Spread()
	case 1:
		m.ImmunityGained()
	case 2:
		m.MutateParasite(m.GetRandomInfectedHost())
	case 3:
		m.Death()
	}
	return
}

// ChooseEvent : Choose which event should happen with probability proportional to the rates.
func ChooseEvent(m *Malaria, param Parameters) int {

	rates := CalcRates(m, param)
	ratesTotal := SumSlice(rates)

	choice := rand.Float64()
	rProb := 0.0
	var event int
	for i := 0; i < 4; i++ {
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
	r := make([]float64, 4)
	r[0] = param.InfectionSpeed * float64(m.NInfectedHosts) * (float64(m.NHosts))
	r[1] = param.ImmunitySpeed * float64(m.NInfectedHosts)
	r[2] = param.MutationSpeed * float64(m.NInfectedHosts)
	r[3] = param.DeathSpeed * float64(m.NInfectedHosts)
	return r
}

// Spread : Another person gets infected.
func (m *Malaria) Spread() {

	spreadTo, spreadFrom := m.GetSpreadToAndSpreadFrom()

	// If spread to is equal to spread from, do not spread.
	if spreadTo == spreadFrom {
		return
	}
	m.InfectHost(spreadTo, spreadFrom)

	return
}

// GetSpreadToAndSpreadFrom : Finds a host to spread to and the antigens which malaria is spread from.
func (m *Malaria) GetSpreadToAndSpreadFrom() (int, int) {
	spreadTo := rand.Intn(m.NHosts)
	spreadFrom := m.InfectedHosts[rand.Intn(m.NInfectedHosts)]
	return spreadTo, spreadFrom
}

// InfectHost :
func (m *Malaria) InfectHost(spreadTo int, spreadFrom int) {
	// Check if the person spreading to has any infections. If true make him sick. If false append the parasite.
	if len(m.Infections[spreadTo]) == 0 {
		for antigenSpot := 0; antigenSpot < m.NAntigens; antigenSpot++ {
			m.Infections[spreadTo] = append(m.Infections[spreadTo], m.Antigens[spreadFrom][antigenSpot])
			m.Antigens[spreadTo] = append(m.Antigens[spreadTo], m.Antigens[spreadFrom][antigenSpot])
		}
		m.NInfectedHosts++
		m.InfectedHosts = append(m.InfectedHosts, spreadTo)
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
	infectedHostIndex := rand.Intn(m.NInfectedHosts)
	infectedHost := m.InfectedHosts[infectedHostIndex]
	if m.Antibodies[infectedHost][m.Lookout[infectedHost]] { // If immune remove parasite.
		m.RemoveParasite(infectedHost, infectedHostIndex)
	} else {
		// If at end, make him healthy
		// Make immunity in the hosts antibody and set the lookout one up
		m.Antibodies[infectedHost][m.Antigens[infectedHost][m.Lookout[infectedHost]]] = true
		m.Lookout[infectedHost]++
		if m.Lookout[infectedHost] > 2 {
			m.RemoveParasite(infectedHost, infectedHostIndex)
		}
	}
	return
}

// RemoveParasite :  Removes a parasite from a host after immunization
func (m *Malaria) RemoveParasite(host int, infectedHostIndex int) {
	m.Infections[host] = append(m.Infections[host][:0], m.Infections[host][m.NAntigens:]...) // Delete the parasite eg. the three first antigens in the infected host.
	if len(m.Infections[host]) == 0 {                                                        // If the last parasite of the host dies, then that host is not infectious anymore.
		m.Antigens[host] = append(m.Antigens[host][:0], m.Antigens[host][m.NAntigens:]...)
		m.NInfectedHosts--
		m.InfectedHosts = append(m.InfectedHosts[:infectedHostIndex], m.InfectedHosts[infectedHostIndex+1:]...)
	}
	m.Lookout[host] = 0
	return
}

// CombineParasites : When a host becomes infected with another parasite (so it is inficted buy mulitple parasites), it has a combination
func (m *Malaria) CombineParasites(host int) {
	nParasites := len(m.Antigens[host])
	for antigen := 0; antigen < m.NAntigens; antigen++ {
		antigenOrNewParasiteChoice := rand.Float64()
		if antigenOrNewParasiteChoice > 0.5 {
			m.Antigens[host][antigen] = m.Infections[host][nParasites-m.NAntigens+rand.Intn(m.NAntigens)]
		}
	}
	return
}

// MutateParasite : Changes a single antigen in a host to a new random one.
func (m *Malaria) MutateParasite(host int) {
	randomAntigen := rand.Intn(m.NAntigens)
	m.Antigens[host][randomAntigen] = int8(rand.Intn(m.MaxAntigenValue))
	return
}

// Death : Kills a host removing it's
func (m *Malaria) Death() {
	hostIndex := rand.Intn(m.NInfectedHosts)
	host := m.InfectedHosts[hostIndex]

	m.Antigens[host] = append(m.Antigens[host][:0], m.Antigens[host][m.NAntigens:]...)
	m.Infections[host] = append(m.Infections[host][:0], m.Infections[host][len(m.Infections[host]):]...)
	m.InfectedHosts = append(m.InfectedHosts[:hostIndex], m.InfectedHosts[hostIndex+1:]...)

	for antibody := 0; antibody < m.MaxAntigenValue; antibody++ {
		m.Antibodies[host][antibody] = false
	}
	m.NInfectedHosts--
	return
}

// GetRandomInfectedHost :
func (m *Malaria) GetRandomInfectedHost() int {
	return m.InfectedHosts[rand.Intn(m.NInfectedHosts)]
}

// SumSlice : Returns the sum a float64 slice.
func SumSlice(X []float64) float64 {
	sum := 0.0
	for _, x := range X {
		sum += x
	}
	return sum
}

func check(e error) {
	if e != nil {
		panic(e)
	}
}

// Death : A person dies
/*
func (m *Malaria) Death() {
	infectedOrHealthy := rand.Float64()
	if infectedOrHealthy > 0.1 { // there is ~ ten times greater likelihood that an infected person dies than a completely random person dies.
		host := m.InfectedHosts[rand.Intn(m.NInfectedHosts)]
		m.Antigens[host] = append(m.Antigens[host][:0], m.Antigens[host][m.NAntigens+1:]...)

		m.NInfectedHosts--
	} else {
		//host := rand.Intn(m.NHosts)

	}

}
*/
