/*
	TODO:
	- Make better tests for Immunity and Spread.
	- Maybe try to have a reproduction method.
	- NoCombineParasites
		- Talk to Kim about this
		- What does it really do?
*/

package main

import (
	"fmt"
	"io"
	"math/rand"
	"os"
	"time"
)

func main() {
	fmt.Println("Starting")
	startTime := time.Now()
	InitiateRunningModel()
	endTime := time.Now()
	fmt.Println("The end. Congrats! The whole run took:", endTime.Sub(startTime), "d")
}

// Malaria : .
type Malaria struct {
	// Counts
	NHosts          int // How many potential hosts there are in the system
	NInfectedHosts  int // The number of infected hosts
	NAntigens       int // The number of antigens a single parasite consists of
	MaxAntigenValue int // The maximum number an antigen can have

	NDifferentAntigens int // The current amount of different antigens in the system.

	InfectedHosts []int // A list of hosts that are infected by one or more malaria strains

	Hosts []Host // An array which contains the host struct. Each index in the array is a single host.
}

// Host : Contains information about a host/person
type Host struct {
	IsAlive    bool
	IsInfected bool
	Lookout    int // The antigen spot which the host currently looks at.

	ExpressedStrain []int8 // The strain which another person will be infected with.
	Infections      []int8 // The strains that are currently infecting a host.
	Antibodies      []bool // An array of the antigens that a host is immune to.
}

// InitiateRunningModel : Starts the whole simulation and sets the parameter-grid.
func InitiateRunningModel() {

	fileName := "MaxAntigenLen3"
	settings := InsertSettings("parameters/" + fileName + "_set.csv")
	CreateAvgDataFile("data/" + fileName + "_data.csv")

	GetParametersAndStartTheThing(fileName, settings)

	return
}

// GetParametersAndStartTheThing : Gets the parameters given in the file, and start the model using the parameters gotten.
func GetParametersAndStartTheThing(fileName string, settings ModelSettings) {
	r := LoadCSVFile("parameters/" + fileName + "_param.csv")

	var run int
	var header []string

	i := 0

	for {

		records, err := r.Read()

		// Error Checking
		if err == io.EOF {
			break
		}
		check(err)

		if i == 0 {
			for j := 0; j < len(records); j++ {
				header = append(header, records[j])
			}
		} else {
			param := InsertParameters(header, records)
			run = StartModel(param, settings)
			if settings.AppendToCurrentDataFile {
				SaveToEndFile("data/temp.txt", settings.CurrentDataFile, run)
			}
		}
		i++
	}
}

// StartModel : Starts the run of the malaria model
func StartModel(param Parameters, settings ModelSettings) int {
	modelTime := 0
	startTime := time.Now()
	m := ConstructMalariaStruct(param)

	m.RunBurnIn(param, settings.BurnIn)

	var run int
	if m.NInfectedHosts != 0 {
		run = m.RunModel(param, settings)
	}

	endTime := time.Now()

	fmt.Println("This set of Parameters, done.", "\n It had the following parameters:", param, "\n It took intime:", modelTime, "\n It took realtime:", endTime.Sub(startTime))

	return run
}

// RunBurnIn : Runs the model N times given by the burnin settings. None of the data will be saved.
func (m *Malaria) RunBurnIn(param Parameters, burnIn int) {
	for run := 0; run < burnIn; run++ {
		m.EventHappens(param)
		if m.NInfectedHosts == 0 {
			fmt.Println("Malaria is dead in", burnIn, "runs. This Happened in burnin")
			return
		}
	}
	return
}

// RunModel :
func (m *Malaria) RunModel(param Parameters, setting ModelSettings) int {

	fileName := "temp"
	file, err := os.Create("data/" + fileName + ".txt")
	check(err)
	defer file.Close()

	run := 0
	for run = 0; run < setting.Runs; run++ {
		m.EventHappens(param)
		if run%100 == 0 {
			//m.CountNumberOfUniqueAntigens()
			fmt.Fprintf(file, "%v \n", m.NInfectedHosts)
			if run%1000000 == 0 {
				//fmt.Println(m.NDifferentAntigens)
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

// CountNumberOfUniqueAntigens : Counts the number of unique antigens an all hosts. s
func (m *Malaria) CountNumberOfUniqueAntigens() {
	AntigenExistence := make([]bool, m.MaxAntigenValue)
	for _, host := range m.Hosts {
		for _, antigen := range host.ExpressedStrain {
			AntigenExistence[antigen] = true
		}
	}
	m.NDifferentAntigens = CountBolleanArray(AntigenExistence)
	return
}
