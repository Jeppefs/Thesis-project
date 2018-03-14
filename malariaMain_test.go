package main

import (
	"fmt"
	"math/rand"
	"testing"
)

func init() {
	rand.Seed(1)
}

func TestStructCreation(t *testing.T) {
	m := CreateMalariaStructDummy(ConstructParameterDummy(5, 3, 5), 2)
	//fmt.Println("Check if the struct looks correct: \n", m.Antigens, "\n", m.Infections, "\n", m.Antibodies, "\n")
	fmt.Println("Check if the struct looks correct: \n", m.Hosts[0], "\n", m.Hosts[1], "\n", m.Hosts[2])
	return
}

func TestEventChoosing(t *testing.T) {
	//m := CreateMalariaStructDummy()
}

func TestInfectHost(t *testing.T) {
	fmt.Println("\n Testing spread")
	m := CreateMalariaStructDummy(ConstructParameterDummy(5, 3, 5), 2)
	m.Hosts[2].InfectHost(&m.Hosts[0], m.NAntigens)
	fmt.Println("Infections:", m.Hosts[2].Infections, "\n ExpressedStrain:", m.Hosts[2].ExpressedStrain)
	m.Hosts[1].InfectHost(&m.Hosts[0], m.NAntigens)
	fmt.Println("\n Infections:", m.Hosts[1].Infections, "\n ExpressedStrain:", m.Hosts[1].ExpressedStrain)
	m.Hosts[1].InfectHost(&m.Hosts[0], m.NAntigens)
	fmt.Println("\n Infections:", m.Hosts[1].Infections, "\n ExpressedStrain:", m.Hosts[1].ExpressedStrain)
}

func TestImmunity(t *testing.T) {
	fmt.Println("\n Testing immunity")
	m := CreateMalariaStructDummy(ConstructParameterDummy(5, 1, 1), 1)

	m.ImmunityGained()
	fmt.Println(m.Hosts[0], m.InfectedHosts)
	m.ImmunityGained()
	fmt.Println(m.Hosts[0], m.InfectedHosts)

}

func TestDeath(t *testing.T) {
	fmt.Println("\n Testing death")
	m := CreateMalariaStructDummy(ConstructParameterDummy(5, 3, 1), 1)
	m.Death()

	if len(m.Hosts[0].Infections) != 0 {
		t.Fatalf("Error in Infections. Is: %d Should be: %d", len(m.Hosts[0].Infections), 0)
	}
	if m.NInfectedHosts != 0 {
		t.Fatalf("Error in NINfectedHosts")
	}
	for _, host := range m.Hosts {
		if host.IsInfected != false {
			t.Fatalf("Error in Antibodies. Is: %t Should be: %t", host.IsInfected, false)
		}
	}

	fmt.Println(m.Hosts[0])
}

/*
func TestMutation(t *testing.T) {
	fmt.Println("\n Testing Mutation")
	m := CreateMalariaStructDummy()
	fmt.Println("Check how it looks:", m.Antigens[0])
	m.MutateParasite(0)
	fmt.Println("Check if it has changed:", m.Antigens[0])

	fmt.Println("Check how it looks:", m.Antigens[1])
	m.MutateParasite(1)
	fmt.Println("Check if it has changed:", m.Antigens[1])

	fmt.Println("Check how it looks:", m.Antigens[1])
	m.MutateParasite(1)
	fmt.Println("Check if it has changed:", m.Antigens[1])

	fmt.Println("Check how it looks:", m.Antigens[1])
	m.MutateParasite(1)
	fmt.Println("Check if it has changed:", m.Antigens[1])
}
*/
func TestCalcMeanAndVar(t *testing.T) {
	fmt.Println("Start Mean and Var test")
	data := []float64{1.0, 2.0, 3.0, 4.0, 5.0}
	mean, variance := CalcMeanAndVar(data)
	if mean != 3.0 {
		t.Fatalf("Mean incorrect")
	}
	if variance != 2.0 {
		t.Fatalf("variance incorrect. Is: %f. Should be: %f", variance, 2.0)
	}

}

/*
func TestSaving(t *testing.T) {
	fmt.Println("\n Testing Saving")
	loadFileName := "testing/SaveInfo.txt"
	saveFileName := "testing/avgTesting.txt"

	var param Parameters

	param.InfectionSpeed = 1.0
	param.ImmunitySpeed = 1.0
	param.MutationSpeed = 0.0
	param.DeathSpeed = 2.0

	SaveToEndFile(loadFileName, saveFileName, 5, param)

}
*/
// ConstructParameterDummy :
func ConstructParameterDummy(NHosts int, NAntigens int, MaxAntigenValue int) Parameters {
	var param Parameters

	// Parameters used when calculating rates and probabilities for next event.
	param.InfectionSpeed = 1.0
	param.ImmunitySpeed = 1.0
	param.MutationSpeed = 1.0
	param.DeathSpeed = 1.0

	// Other setting that changes the behaviour of the system
	param.NHosts = NHosts
	param.NAntigens = NAntigens
	param.MaxAntigenValue = MaxAntigenValue

	return param
}

// ConstructMalariaStruct : Initiates a malaria struct and starts initial conditions.
func CreateMalariaStructDummy(param Parameters, NInfectedHosts int) Malaria {
	var m Malaria

	// Sets initial values.
	m.NHosts = param.NHosts // Constant
	m.NInfectedHosts = NInfectedHosts
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
