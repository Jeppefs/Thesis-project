package main

import (
	"fmt"
	"math/rand"
	"sort"
)

// Malaria : Contains all information that is needed to run the simulation.
type Malaria struct {
	// Counts
	NHosts          int // How many potential hosts there are in the system
	NInfectedHosts  int // The number of infected hosts
	NAntigens       int // The number of antigens a single parasite consists of
	MaxAntigenValue int // The maximum number an antigen can have

	NDifferentAntigens int // The current amount of different antigens in the system.

	InfectedHosts []int // A list of hosts that are infected by one or more malaria strains

	Hosts []Host // An array which contains the host struct. Each index in the array is a single host.

	SuperInfectionCounter []int          // An array that keeps count of the number of infections in all hosts. 0 is the how no infected there is.
	StrainCounter         map[string]int // Keeps count of all strains. Key is the specific strain (anitgens seperated by comma), and int is how many is infected by that particular strain. NOTE, it keeps count of the expressed strain, not the number of infected.
	StrainKeys            []string       // An ordered set of keys for StrainCounter. Used when saving.
}

// Host : Contains information about a host/person
type Host struct {
	IsAlive    bool
	IsInfected bool

	ExpressedStrain []int8 // The strain which another person will be infected with.
	Infections      []int8 // The strains that are currently infecting a host.
	Antibodies      []bool // An array of the antigens that a host is immune to.
}

// ConstructMalariaStruct : Initiates a malaria struct and starts initial conditions.
func ConstructMalariaStruct(param Parameters, settings ModelSettings) Malaria {
	var m Malaria

	// Sets initial values.
	m.NHosts = param.NHosts // Constant
	m.NInfectedHosts = param.InitialInfected
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

	m.SuperInfectionCounter = make([]int, param.MaxSuperInfections+1)
	m.SuperInfectionCounter[0] = m.NHosts - m.NInfectedHosts
	m.SuperInfectionCounter[1] = m.NInfectedHosts

	if settings.SpecificStrains == "All" {
		_, m.StrainKeys, m.StrainCounter = FindAllStrainCombinations(param.NAntigens, param.MaxAntigenValue)
	} else {
		m.StrainKeys = []string{"1,2", "3,4", "5,6", "7,8"}
		m.StrainCounter = map[string]int{"1,2": 0, "3,4": 0, "5,6": 0, "7,8": 0}
	}
	m.CountStrains()

	fmt.Println(m.StrainCounter)

	//fmt.Println(m.Antigens, "\n", m.Infections, "\n", m.Antibodies, "\n")
	return m
}

// MakeHost : Make a host in the hoststruct
func MakeHost(infected bool, NAntigens int, MaxAntigenValue int) Host {
	var h Host

	h.IsAlive = true
	h.ExpressedStrain = make([]int8, NAntigens)
	h.Antibodies = make([]bool, MaxAntigenValue)

	if infected {

		h.IsInfected = true
		h.Infections = make([]int8, NAntigens)
		h.InsertRandomInfection(NAntigens, MaxAntigenValue)
	} else {
		h.IsInfected = false
	}

	return h
}

// InsertRandomInfection : A host becomes infected by a random strain.
func (h *Host) InsertRandomInfection(NAntigens int, MaxAntigenValue int) {

	for antigen := 0; antigen < NAntigens; antigen++ {
		h.ExpressedStrain[antigen] = int8(rand.Intn(MaxAntigenValue)) + 1
		h.Infections[antigen] = h.ExpressedStrain[antigen]
		if antigen > 0 {
			if CheckUniqueInt8(h.ExpressedStrain[0:antigen], h.ExpressedStrain[antigen]) == false {
				antigen--
			}
		}
	}
	sort.Slice(h.ExpressedStrain, func(i, j int) bool { return h.ExpressedStrain[i] < h.ExpressedStrain[j] })
	sort.Slice(h.Infections, func(i, j int) bool { return h.Infections[i] < h.Infections[j] })
	return
}
