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
	m := ConstructMalariaStructDummy(ConstructParameterDummy)
	//fmt.Println("Check if the struct looks correct: \n", m.Antigens, "\n", m.Infections, "\n", m.Antibodies, "\n")
	fmt.Println("Check if the struct looks correct:", m)
}

func TestEventChoosing(t *testing.T) {
	//m := CreateDummyMalariaStruct()
}

func TestImmunity(t *testing.T) {
	fmt.Println("\n Testing immunity")
	m := CreateDummyMalariaStruct()

	host := 1
	infectedHost := 1
	m.RemoveParasite(host, infectedHost)
	if len(m.Infections[host]) != 0 {
		fmt.Println("Error in RemoveParasite")
	}
	if len(m.Antigens[host]) != 0 {
		fmt.Println("Error in RemoveParasite. Is:", len(m.Antigens[host]), "Should be:", 0)
	}
	if m.NInfectedHosts != 1 {
		fmt.Println("Error in RemoveParasite")
	}
	if len(m.InfectedHosts) != 1 {
		fmt.Println("Error in RemoveParasite")
	}

	host = 0
	infectedHost = 0

	m.ImmunityGained()
	if m.Antibodies[host][m.Antigens[host][0]] != true {
		fmt.Println("Error in ImmunityGained")
	}

}

func TestSpread(t *testing.T) {
	fmt.Println("\n Testing spread")
	m := CreateDummyMalariaStruct()
	m.InfectHost(2, 0)
	fmt.Println("Infections:", m.Infections, "Antigens \n:", m.Antigens)
	m.InfectHost(2, 1)
	fmt.Println("\n Infections:", m.Infections, "\n Antigens:", m.Antigens)

	if m.NInfectedHosts != 3 {
		fmt.Println("Error in Spread, m.NInfectedHosts incorrect. Is:", m.NInfectedHosts)
	}
	if m.InfectedHosts[2] != 2 && len(m.InfectedHosts) == 3 {
		fmt.Println("Error in Spread, m.InfectedHosts incorrect")
	}

}

func TestDeath(t *testing.T) {
	fmt.Println("\n Testing death")
	m := CreateDummyMalariaStruct()
	m.Death()
	m.Death()
	if len(m.Infections[0]) != 0 {
		t.Fatalf("Error in Infections")
	}
	if len(m.Antigens[0]) != 0 {
		t.Fatalf("Error in Antigens")
	}
	if m.NInfectedHosts != 0 {
		t.Fatalf("Error in NINfectedHosts")
	}
	for _, boolVal := range m.Antibodies[0] {
		if boolVal != false {
			t.Fatalf("Error in Antibodies. Is: %t Should be: %t", boolVal, false)
		}
	}

	fmt.Println(m.Infections)
}

func TestMutation(t *testing.T) {
	fmt.Println("\n Testing Mutation")
	m := CreateDummyMalariaStruct()
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
}

// ConstructMalariaStruct : Initiates a malaria struct and starts initial conditions.
func ConstructMalariaStructDummy(param Parameters) Malaria {
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
