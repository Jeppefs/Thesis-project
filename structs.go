package main

import (
	"math/rand"
)

// Malaria : Contains all information that is needed to run the simulation.
type Malaria struct {
	// Counts
	NHosts          int // How many potential hosts there are in the system
	NInfectedHosts  int // The number of infected hosts
	NAntigens       int // The number of antigens a single parasite consists of
	MaxAntigenValue int // The maximum number an antigen can have
	MaxStrains      int // The maximum number of possible strains in the system

	NDifferentAntigens int // The current amount of different antigens in the system.

	InfectedHosts []int // A list of hosts that are infected by one or more malaria strains

	InfectionCounter []int    // An array that keeps count of the number of infections in all hosts. 0 index is no infections.
	StrainCounter    []int    // Keeps count of all strains. Key is the specific strain (anitgens seperated by comma), and int is how many is infected by that particular strain.
	Strains          [][]int8 // The values of the strains. Each index has the antigens of that strains.

	Hosts []Host // An array which contains the host struct. Each index in the array is a single host.
}

// Host : Contains information about a host/person
type Host struct {
	NInfections int    // The number of infection a host has.
	Infections  []int  // The strain indices that are currently infecting a host.
	Antibodies  []bool // An array of the antigens that a host is immune to.
}

// ConstructMalariaStruct : Initiates a malaria struct and starts initial conditions.
func ConstructMalariaStruct(param Parameters) Malaria {
	var m Malaria

	// Sets initial values.
	m.NHosts = param.NHosts // Constant
	m.NInfectedHosts = param.InitialInfected
	m.NAntigens = param.NAntigens
	m.MaxAntigenValue = param.MaxAntigenValue

	if param.SpecificStrains == "all" {
		m.MaxStrains, m.Strains, m.StrainCounter = FindAllStrainCombinations(param.NAntigens, param.MaxAntigenValue)
	} else if param.SpecificStrains == "nonCross" {
		m.NAntigens = 2
		param.NAntigens = m.NAntigens
		m.MaxAntigenValue = 8
		param.MaxAntigenValue = m.MaxAntigenValue
		m.MaxStrains = 4
		m.Strains = [][]int8{{1, 2}, {3, 4}, {5, 6}, {7, 8}}
		m.StrainCounter = make([]int, m.MaxStrains)
	} else if param.SpecificStrains == "cross" {
		m.NAntigens = 2
		param.NAntigens = m.NAntigens
		m.MaxAntigenValue = 4
		param.MaxAntigenValue = m.MaxAntigenValue
		m.MaxStrains = 4
		m.Strains = [][]int8{{1, 2}, {2, 3}, {3, 4}, {4, 1}}
		m.StrainCounter = make([]int, m.MaxStrains)
	} else {
		panic("No specific strain option was selected")
	}

	// Create hosts - infected and nonInfected
	m.Hosts = make([]Host, m.NHosts)
	for host := 0; host < m.NHosts; host++ {
		if host < m.NInfectedHosts {
			m.Hosts[host] = MakeHost(param, true, m.MaxStrains)
		} else {
			m.Hosts[host] = MakeHost(param, false, m.MaxStrains)
		}
	}

	m.InfectedHosts = make([]int, m.NInfectedHosts)
	for host := 0; host < m.NInfectedHosts; host++ {
		m.InfectedHosts[host] = host
	}

	m.InfectionCounter = make([]int, param.MaxSuperInfections+1)
	m.InfectionCounter[0] = m.NHosts - m.NInfectedHosts
	m.InfectionCounter[1] = m.NInfectedHosts

	m.CountStrains()

	return m
}

// MakeHost : Make a host in the hoststruct
func MakeHost(param Parameters, infected bool, maxStrains int) Host {
	var h Host

	h.Infections = make([]int, 0)
	h.Antibodies = make([]bool, param.MaxAntigenValue) // TODO: Make sure that a boolean array starts at false.

	if infected {
		h.NInfections = 1
		h.Infections = append(h.Infections, rand.Intn(maxStrains))
	} else {
		h.NInfections = 0
	}

	return h
}

/*
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


*/
