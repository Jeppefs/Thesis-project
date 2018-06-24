package main

import (
	"fmt"
	"io"
	"math"
	"math/rand"
	"testing"

	"github.com/google/go-cmp/cmp"
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
	r := LoadCSVFile("data/test/parameters.csv")
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

// Checks if two values are the same, and stops the test if they are not.
func CheckIfEqual(t *testing.T, s string, a interface{}, b interface{}) {
	if cmp.Equal(a, b) {
		return
	}
	t.Fatalf("Error in %s. The two values are not equal. \n Is: %v. \n Should be: %v", s, a, b)
	return
}

func TestStructCreation(t *testing.T) {
	malariaStructs := CreateMalariaStrcutsInSlice()

	CheckIfEqual(t, "NHosts", malariaStructs[0].NHosts, 10)
	CheckIfEqual(t, "NHosts", malariaStructs[1].NHosts, 10)
	CheckIfEqual(t, "NHosts", malariaStructs[2].NHosts, 3)

	CheckIfEqual(t, "NInfectedHosts", malariaStructs[0].NInfectedHosts, 1)
	CheckIfEqual(t, "NInfectedHosts", malariaStructs[1].NInfectedHosts, 3)
	CheckIfEqual(t, "NInfectedHosts", malariaStructs[2].NInfectedHosts, 1)

	CheckIfEqual(t, "IsInfected", malariaStructs[0].Hosts[0].IsInfected, true)
	CheckIfEqual(t, "IsInfected", malariaStructs[1].Hosts[2].IsInfected, true)
	CheckIfEqual(t, "IsInfected", malariaStructs[0].Hosts[5].IsInfected, false)
	CheckIfEqual(t, "IsInfected", malariaStructs[0].Hosts[1].IsInfected, false)

	CheckIfEqual(t, "Antigens", malariaStructs[0].Hosts[0].Infections, []int8{0})
	CheckIfEqual(t, "AntigenLen", len(malariaStructs[1].Hosts[0].Infections), 2)

	CheckIfEqual(t, "Is healthy host empty", len(malariaStructs[0].Hosts[4].Infections), 0)
	CheckIfEqual(t, "Is healthy host empty", len(malariaStructs[0].Hosts[4].ExpressedStrain), 1)
	CheckIfEqual(t, "Is healthy host empty", len(malariaStructs[1].Hosts[4].ExpressedStrain), 2)

	fmt.Println("\n")
	return
}

func TestEventChoosing(t *testing.T) {
	malariaStructs := CreateMalariaStrcutsInSlice()

	r := CalcRates(&malariaStructs[0], p1)

	NEventTypes := 4
	eventCount := [4]int{0, 0, 0, 0}
	NEvents := int(math.Pow(10, 4))

	for i := 0; i < NEvents; i++ {
		event := ChooseEvent(&malariaStructs[0], p1)
		eventCount[event]++
	}

	for i := 0; i < NEventTypes; i++ {
		r[i] = r[i] * float64(NEvents)
	}

	fmt.Println(eventCount, r)

	return
}

func TestSpread(t *testing.T) {
	//malariaStructs := CreateMalariaStrcutsInSlice()

	return
}

func TestInfectHost(t *testing.T) {
	malariaStructs := CreateMalariaStrcutsInSlice()

	malariaStructs[0].Hosts[4].InfectHost(&malariaStructs[0].Hosts[0], p1.NAntigens)
	CheckIfEqual(t, "Newly infected has same infections", malariaStructs[0].Hosts[4].Infections, malariaStructs[0].Hosts[0].Infections)
	CheckIfEqual(t, "Newly infected has correct expressed strain", malariaStructs[0].Hosts[4].ExpressedStrain, malariaStructs[0].Hosts[0].ExpressedStrain)

	malariaStructs[0].Hosts[1].InfectHost(&malariaStructs[0].Hosts[0], p1.NAntigens)
	malariaStructs[0].Hosts[1].InfectHost(&malariaStructs[0].Hosts[0], p1.NAntigens)
	CheckIfEqual(t, "Newly infected has same infections", malariaStructs[0].Hosts[1].Infections, []int8{0, 0})
	CheckIfEqual(t, "Newly infected has correct expressed strain", malariaStructs[0].Hosts[1].ExpressedStrain, []int8{0})

	// This also tests that it is expressedStrain that is used to infect a new person.g
	malariaStructs[1].Hosts[0].ExpressedStrain[0] = 1
	malariaStructs[1].Hosts[0].ExpressedStrain[1] = 2
	malariaStructs[1].Hosts[5].InfectHost(&malariaStructs[1].Hosts[0], p2.NAntigens)
	malariaStructs[1].Hosts[5].InfectHost(&malariaStructs[1].Hosts[0], p2.NAntigens)

	CheckIfEqual(t, "Super Infection with same strain", malariaStructs[1].Hosts[5].Infections, []int8{1, 2, 1, 2})

	return

}

func TestCombinerParasite(t *testing.T) {

	return
}

func TestImmunity(t *testing.T) {
	fmt.Println("\n Testing immunity")
	malariaStructs := CreateMalariaStrcutsInSlice()

	fmt.Println(malariaStructs[0].Hosts[1].IsInfected)
	malariaStructs[0].ImmunityGained()
	CheckIfEqual(t, "Expressed Strain", len(malariaStructs[0].Hosts[0].ExpressedStrain), 0)
}

func TestHasStrain(t *testing.T) {
	m := CreateMalariaStrcutsInSlice()

	m[1].Hosts[0].ExpressedStrain[0] = 3
	m[1].Hosts[0].ExpressedStrain[1] = 4
	m[1].Hosts[1].ExpressedStrain[0] = 1
	m[1].Hosts[1].ExpressedStrain[1] = 2
	m[1].Hosts[2].ExpressedStrain[0] = 1
	m[1].Hosts[2].ExpressedStrain[1] = 2

	m[1].Hosts[0].Infections[0] = 3
	m[1].Hosts[0].Infections[1] = 4
	m[1].Hosts[1].Infections[0] = 1
	m[1].Hosts[1].Infections[1] = 2
	m[1].Hosts[2].Infections[0] = 1
	m[1].Hosts[2].Infections[1] = 2

	CheckIfEqual(t, "If infection strain is contained in target.", m[1].Hosts[0].HasStrain(&m[1].Hosts[1], 2), false)
	CheckIfEqual(t, "If infection strain is contained in target.", m[1].Hosts[1].HasStrain(&m[1].Hosts[2], 2), true)

	m[1].Hosts[0].InfectHost(&m[1].Hosts[1], 2)
	m[1].Hosts[0].ExpressedStrain[0] = 3
	m[1].Hosts[0].ExpressedStrain[1] = 4

	CheckIfEqual(t, "If infection is correct", m[1].Hosts[0].Infections, []int8{3, 4, 1, 2})

	CheckIfEqual(t, "If infection strain is contained in target.", m[1].Hosts[0].HasStrain(&m[1].Hosts[1], 2), true)
	CheckIfEqual(t, "If infection strain is contained in target.", m[1].Hosts[0].HasStrain(&m[1].Hosts[2], 2), true)
	CheckIfEqual(t, "If infection strain is contained in target.", m[1].Hosts[1].HasStrain(&m[1].Hosts[0], 2), false)
}

/*
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
*/
