package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"math/rand"
	"reflect"
	"strings"
	"testing"
)

var s1 ModelSettings
var s2 ModelSettings
var s3 ModelSettings

var p1 Parameters
var p2 Parameters
var p3 Parameters

func init() {
	rand.Seed(1)

	// Insert the parameters from the
	r := LoadCSVFile("testing/" + "Test_param.csv")
	var header []string
	i := 0

	for {

		records, err := r.Read()

		// Error Checking
		if err == io.EOF {
			break
		}
		check(err)

		switch i {
		case 0:
			for j := 0; j < len(records); j++ {
				header = append(header, records[j])
			}
		case 1:
			p1 = InsertParameters(header, records)
		case 2:
			p2 = InsertParameters(header, records)
		case 3:
			p3 = InsertParameters(header, records)
		}
		i++
	}

}

//
func CreateMalariaStrcutsInSlice() [3]Malaria {
	malariaStructs := [3]Malaria{ConstructMalariaStruct(p1), ConstructMalariaStruct(p2), ConstructMalariaStruct(p3)}

	return malariaStructs
}

func TestStructCreation(t *testing.T) {
	malariaStructs := CreateMalariaStrcutsInSlice()
	for _, m := range malariaStructs {
		fmt.Printf("%+v\n", m, "\n")
		for _, h := range m.Hosts {
			fmt.Println(h)
		}
		fmt.Println("\n")
	}
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

	// Test that it does not infect one already with the same strain.
	var h1 Host
	var h2 Host
	h1.Infections = []int8{1, 2, 4, 2, 2, 1, 2, 3}
	h2.ExpressedStrain = []int8{1, 2}

	if h1.HasStrain(&h2, 2) == false {
		t.Fatalf("Error. Is Reinfected with same strain.")
	}

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

	fmt.Println(m.Hosts[0], m.InfectedHosts)
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

func TestSaving(t *testing.T) {
	// TODO: Make this test work under the new scheme.
	fmt.Println("\n Testing Saving")
	loadFileName := "testing/SaveInfo.txt"
	saveFileName := "testing/avgTesting.txt"

	var param Parameters

	param.InfectionSpeed = 1.0
	param.ImmunitySpeed = 1.0
	param.MutationSpeed = 0.0
	param.DeathSpeed = 2.0

	SaveToEndFile(loadFileName, saveFileName, 5)
}

func TestLoading(t *testing.T) {
	fmt.Println("\n Testing loading data")
	parameterFileName := "parameters/simplest_infectionRate_param.csv"
	//settingsFileName := "parameters/simplest_infectionRate_set.csv"

	parameterFile, err := ioutil.ReadFile(parameterFileName)
	if err != nil {
		log.Fatal(err)
	}

	r := csv.NewReader(strings.NewReader(string(parameterFile)))

	for {
		record, err := r.Read()
		if err == io.EOF {
			break
		}

		if err != nil {
			log.Fatal(err)
		}

		fmt.Println(reflect.TypeOf(record[0]))
	}

}
