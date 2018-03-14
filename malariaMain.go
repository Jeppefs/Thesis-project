/*
	TODO:
	- Make better tests for Immunity and Spread.
	- Print total runtime
	- Maybe try to have a reproduction rate  rate.
*/

package main

import (
	"fmt"
	"math/rand"
	"os"
	"sort"
	"strconv"
	"time"
)

func main() {
	fmt.Println("Starting")
	InitiateRunningModel()
	fmt.Println("The end. Congrats!")
}

// Malaria : .
type Malaria struct {
	// Counts
	NHosts         int // How many potential hosts there are in the system
	NInfectedHosts int // The number of infected hosts
	NAntigens      int // The number of antigens a single parasite consists of

	MaxAntigenValue int // The maximum number an antigen can have

	InfectedHosts []int // A list of hosts that are infected by one or more malaria strains

	Hosts []Host // An array which contains the host struct. Each value in the array is a single slice.
}

// Host : Contains information about a host/person
type Host struct {
	Lookout    int
	IsInfected bool

	ExpressedStrain []int8 // The strain which another person will be infected with.
	Infections      []int8 // The strains that are currently infecting a host.
	Antibodies      []bool // An array of the antigens that a host is immune to.
}

// MalariaStatistics : Contains
type MalariaStatistics struct {
}

// Parameters : Sets the parameters for a particular run. These are all set before the simulation.
type Parameters struct {
	// Parameters used when calculating rates and probabilities for next event.
	InfectionSpeed float64
	ImmunitySpeed  float64
	MutationSpeed  float64
	DeathSpeed     float64

	// Other setting that changes the behaviour of the system
	NHosts          int
	NAntigens       int
	MaxAntigenValue int
}

// ModelSettings : A structure that contains information about model settings such as
type ModelSettings struct {
	BurnIn int
	Runs   int

	Test                    bool
	AppendToCurrentDataFile bool

	CurrentDataFile string
}

// MakeModelSetting : Constructs the ModelSettings struct, which sets how the data should be saved, if a burnin should exist and so on.
func MakeModelSetting() ModelSettings {

	var setting ModelSettings

	setting.Runs = 5000000   // Usually 5000000
	setting.BurnIn = 5000000 // Usually 5000000

	setting.Test = true
	setting.AppendToCurrentDataFile = true

	setting.CurrentDataFile = "data/avgFile6.txt"

	return setting
}

// MakeParameterGrid : Creates a parameter grid to search through. Also where settings as applied.
func MakeParameterGrid() []Parameters {
	gridsize := 1

	parameterGrid := make([]Parameters, gridsize)

	for i := 0; i < gridsize; i++ {
		parameterGrid[i].InfectionSpeed = 0.97 //+ float64(i)/1000.0
		parameterGrid[i].ImmunitySpeed = 1.0
		parameterGrid[i].MutationSpeed = 0.0
		parameterGrid[i].DeathSpeed = 0.0050

		parameterGrid[i].NHosts = 10000
		parameterGrid[i].NAntigens = 3
		parameterGrid[i].MaxAntigenValue = 10
	}

	return parameterGrid
}

// InitiateRunningModel : Starts the whole simulation and sets the parameter-grid.
func InitiateRunningModel() {
	parameterGrid := MakeParameterGrid()
	setting := MakeModelSetting()
	for i := 0; i < len(parameterGrid); i++ {
		run := StartModel(parameterGrid[i], setting)
		if setting.AppendToCurrentDataFile {
			SaveToEndFile("data/test.txt", setting.CurrentDataFile, run, parameterGrid[i])
		}
	}
}

// StartModel : Starts the run of the malaria model
func StartModel(param Parameters, setting ModelSettings) int {
	modelTime := 0
	startTime := time.Now()
	m := ConstructMalariaStruct(param)

	for burnIn := 0; burnIn < setting.BurnIn; burnIn++ {
		m.EventHappens(param)
		if m.NInfectedHosts == 0 {
			fmt.Println("Malaria is dead in", burnIn, "runs. This Happened in burnin")
			break
		}
	}

	var run int
	if m.NInfectedHosts != 0 {
		if setting.Test {
			run = m.RunModelWithSaving(param, setting)
		} else {
			run = m.RunModelWithoutSaving(param, setting)
		}
	}

	endTime := time.Now()

	fmt.Println("This set of Parameters, done.", "\n It had the following parameters:", param, "\n It took intime:", modelTime, "\n It took realtime:", endTime.Sub(startTime))
	fmt.Println(m.NHosts)

	return run
}

// RunModelWithSaving :
func (m *Malaria) RunModelWithSaving(param Parameters, setting ModelSettings) int {

	filename := "test" // + strconv.Itoa(int(param.ImmunitySpeed))
	file, err := os.Create("data/" + filename + ".txt")
	defer file.Close()
	check(err)

	run := 0
	for run = 0; run < setting.Runs; run++ {
		m.EventHappens(param)
		if run%100 == 0 {
			fmt.Fprintf(file, "%v \n", m.NInfectedHosts)
			if run%1000000 == 0 {
				fmt.Println(run)
			}
		}
		if m.NInfectedHosts == 0 {
			fmt.Println("Malaria is dead in", run, "runs")
			fmt.Fprintf(file, "%v \n", m.NInfectedHosts)
			break
		}
	}

	return run
}

// RunModelWithoutSaving :
func (m *Malaria) RunModelWithoutSaving(param Parameters, setting ModelSettings) int {

	run := 0
	for run = 0; run < setting.Runs; run++ {
		m.EventHappens(param)
		if run%100 == 0 {
			if run%1000000 == 0 {
				fmt.Println(run)
			}
		}
		if m.NInfectedHosts == 0 {
			fmt.Println("Malaria is dead in", run, "runs")
			break
		}
	}

	return run
}

// ConstructMalariaStruct : Initiates a malaria struct and starts initial conditions.
func ConstructMalariaStruct(param Parameters) Malaria {
	var m Malaria

	// Sets initial values.
	m.NHosts = param.NHosts // Constant
	m.NInfectedHosts = m.NHosts / 100
	m.NAntigens = param.NAntigens
	m.MaxAntigenValue = param.MaxAntigenValue

	m.Hosts = make([]Host, m.NHosts)
	for host := 0; host < m.NHosts; host++ {
		if host < m.NInfectedHosts {
			m.Hosts[host] = MakeHost(true, m.NAntigens, m.MaxAntigenValue)
		} else {
			m.Hosts[host] = MakeHost(false, m.NAntigens, m.MaxAntigenValue)
		}
	}

	m.InfectedHosts = make([]int, m.NInfectedHosts)
	for host := 0; host < m.NInfectedHosts; host++ {
		m.InfectedHosts[host] = host
	}

	//fmt.Println(m.Antigens, "\n", m.Infections, "\n", m.Antibodies, "\n")
	return m
}

// MakeHost : Make a host in the hoststruct
func MakeHost(infected bool, NAntigens int, MaxAntigenValue int) Host {
	var h Host

	h.Lookout = 0
	h.ExpressedStrain = make([]int8, NAntigens)
	h.Antibodies = make([]bool, MaxAntigenValue)

	if infected {
		h.IsInfected = true
		h.Infections = make([]int8, NAntigens)
		for antigen := 0; antigen < NAntigens; antigen++ {
			h.ExpressedStrain[antigen] = int8(rand.Intn(MaxAntigenValue))
			h.Infections[antigen] = h.ExpressedStrain[antigen]
		}

	} else {
		h.IsInfected = false
	}

	return h
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
		host, _ := m.GetRandomInfectedHost()
		m.MutateParasite(host)
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
	r[0] = param.InfectionSpeed * float64(m.NInfectedHosts)
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
	// If the target is not currently infected put him on the infected list and add to the number of incfected
	if m.Hosts[spreadTo].IsInfected == false {
		m.NInfectedHosts++
		m.InfectedHosts = append(m.InfectedHosts, spreadTo)
		m.Hosts[spreadTo].IsInfected = true
	}

	m.Hosts[spreadTo].InfectHost(&m.Hosts[spreadFrom], m.NAntigens)

	return
}

// GetSpreadToAndSpreadFrom : Finds a host to spread to and the antigens which malaria is spread from.
func (m *Malaria) GetSpreadToAndSpreadFrom() (int, int) {
	spreadTo := rand.Intn(m.NHosts)
	spreadFrom := m.InfectedHosts[rand.Intn(m.NInfectedHosts)]
	return spreadTo, spreadFrom
}

// InfectHost :
func (h *Host) InfectHost(fromHost *Host, NAntigens int) {
	// Check if the person spreading to has any infections. If false make him sick. If true append the parasite.
	if h.IsInfected {
		for antigen := 0; antigen < NAntigens; antigen++ {
			h.Infections = append(h.Infections, fromHost.ExpressedStrain[antigen])
		}
		h.CombineParasites(NAntigens)
	} else {
		for antigen := 0; antigen < NAntigens; antigen++ {
			h.Infections = append(h.Infections, fromHost.ExpressedStrain[antigen])
			h.ExpressedStrain[antigen] = fromHost.ExpressedStrain[antigen]
		}
	}
	return
}

// CombineParasites : When a host becomes infected with another parasite (so it is inficted buy mulitple parasites), it has a combination
func (h *Host) CombineParasites(NAntigens int) {
	for antigen := 0; antigen < NAntigens; antigen++ {
		antigenOrNewParasiteChoice := rand.Float32()
		if antigenOrNewParasiteChoice > 0.5 { // Pick randomly new antigens in the infected host.
			h.ExpressedStrain[antigen] = h.Infections[rand.Intn(len(h.Infections))]
		}
	}
	return
}

// ImmunityGained : An infected person get immunity from one strain. If that one already exist, the parasite dies.
func (m *Malaria) ImmunityGained() {
	infectedHostIndex := rand.Intn(m.NInfectedHosts)
	infectedHost := m.InfectedHosts[infectedHostIndex]

	m.Hosts[infectedHost].GiveHostAntibody(m.NAntigens)

	if m.Hosts[infectedHost].IsInfected == false {
		m.NInfectedHosts--
		m.InfectedHosts = append(m.InfectedHosts[:infectedHostIndex], m.InfectedHosts[infectedHostIndex+1:]...)
	}

	return
}

// GiveHostAntibody : Gives the host an antibody for its current lookout in the antigens. Also send to RemoveParaiste method if removal should happend
func (h *Host) GiveHostAntibody(NAntigens int) {
	if h.Lookout > NAntigens-1 { //-1 because NAntigens is one larger than lookout because of 0 indexing
		h.RemoveParasite(NAntigens)
	} else if h.Antibodies[h.Infections[h.Lookout]] {
		h.RemoveParasite(NAntigens)
	} else {
		// If at end, make him healthy
		// Make immunity in the hosts antibody and set the lookout one up
		h.Antibodies[h.Infections[h.Lookout]] = true
		h.Lookout++
	}
	return
}

// RemoveParasite :  Removes a parasite from a host after immunization
func (h *Host) RemoveParasite(NAntigens int) {
	h.Infections = append(h.Infections[:0], h.Infections[NAntigens:]...)
	if len(h.Infections) == 0 { // If the last parasite of the host dies, then that host is not infected anymore.
		h.IsInfected = false
	}
	h.Lookout = 0
	return
}

// Death : Kills a host removing it from the system and adding a new one.
func (m *Malaria) Death() {
	host, hostIndex := m.GetRandomInfectedHost()

	m.Hosts[host].Die(m.NAntigens, m.MaxAntigenValue)

	//m.CheckIfAllInfectedHasInfection(1)
	//fmt.Println(hostIndex, m.InfectedHosts[hostIndex])
	m.InfectedHosts = append(m.InfectedHosts[:hostIndex], m.InfectedHosts[hostIndex+1:]...)
	m.NInfectedHosts--
	//fmt.Println(hostIndex, m.InfectedHosts[hostIndex])
	//m.CheckIfAllInfectedHasInfection(2)
	return
}

// Die : A host dies
func (h *Host) Die(NAntigens int, MaxAntigenValue int) {
	h.Infections = append(h.Infections[:0], h.Infections[len(h.Infections):]...)
	h.Lookout = 0
	h.IsInfected = false

	for antibody := 0; antibody < MaxAntigenValue; antibody++ {
		h.Antibodies[antibody] = false
	}

}

// MutateParasite : Changes a single antigen in a host to a new random one.
func (m *Malaria) MutateParasite(host int) {
	randomAntigen := rand.Intn(m.NAntigens)
	m.Hosts[host].ExpressedStrain[randomAntigen] = int8(rand.Intn(m.MaxAntigenValue))
	return
}

// GetRandomInfectedHost :
func (m *Malaria) GetRandomInfectedHost() (int, int) {
	hostIndex := rand.Intn(m.NInfectedHosts)
	host := m.InfectedHosts[hostIndex]
	return host, hostIndex
}

func (m *Malaria) CheckIfAllInfectedHasInfection(q int) {
	for _, host := range m.InfectedHosts {
		if len(m.Hosts[host].Infections) == 0 {
			fmt.Println("Warning", m.Hosts[host].Infections, host, m.Hosts[host].IsInfected, len(m.InfectedHosts), m.NInfectedHosts)
			if q == 2 {
				panic(strconv.Itoa(q))
			}
		}
	}
}

func CheckIfAllIsUnique(q []int) {
	sort.Ints(q)
	for i := 0; i <= len(q)-2; i++ {
		if q[i] == q[i+1] {
			fmt.Println(q[i])
			panic("e")
		}
	}

}
