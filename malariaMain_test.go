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
	m := CreateDummyMalariaStruct()
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
	loadFileName := "testing/SaveInfo"
	saveFileName := "testing/avgTesting"

	CalcMeanVarAndSave(loadFileName, saveFileName)
}

func CreateDummyMalariaStruct() Malaria {
	var m Malaria

	// Sets initial values.
	m.NHosts = 10 // Constant
	m.NInfectedHosts = 2
	m.NAntigens = 3
	m.NStrains = 1

	m.MaxAntigenValue = 5

	// Make initial antigens

	m.Antigens = make([][]int8, m.NHosts)
	for host := 0; host < m.NInfectedHosts; host++ {
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
