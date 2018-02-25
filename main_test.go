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
	fmt.Println("\n Testing immunity start")
	m := CreateDummyMalariaStruct()

	host := 1
	infectedHost := 1
	fmt.Println(m.Infections)
	m.RemoveParasite(host, infectedHost)
	fmt.Println(m.Infections)

}

func TestSpread(t *testing.T) {
	fmt.Println("\n Testing spread start")
	m := CreateDummyMalariaStruct()
	m.InfectHost(2, 0)
	fmt.Println(m.Infections, "\n", m.Antigens)
	m.InfectHost(2, 1)
	fmt.Println(m.Infections, "\n", m.Antigens)

	m.CombineParasites(2)
	fmt.Println(m.Antigens)

	fmt.Println("Test was completely succesfull, congrats! :D")
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
