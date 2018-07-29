package main

import (
	"fmt"
	"io"
	"math"
	"math/rand"
	"runtime/debug"
	"sort"
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
func CreateMalariaStructsInSlice() [3]Malaria {

	malariaStructs := [3]Malaria{ConstructMalariaStruct(p1), ConstructMalariaStruct(p2), ConstructMalariaStruct(p3)}

	// Make the expressed strains and infection definitive.
	malariaStructs[1].Hosts[0].ExpressedStrain[0] = 3
	malariaStructs[1].Hosts[0].ExpressedStrain[1] = 4
	malariaStructs[1].Hosts[1].ExpressedStrain[0] = 1
	malariaStructs[1].Hosts[1].ExpressedStrain[1] = 2
	malariaStructs[1].Hosts[2].ExpressedStrain[0] = 1
	malariaStructs[1].Hosts[2].ExpressedStrain[1] = 2

	malariaStructs[1].Hosts[0].Infections[0] = 3
	malariaStructs[1].Hosts[0].Infections[1] = 4
	malariaStructs[1].Hosts[1].Infections[0] = 1
	malariaStructs[1].Hosts[1].Infections[1] = 2
	malariaStructs[1].Hosts[2].Infections[0] = 1
	malariaStructs[1].Hosts[2].Infections[1] = 2

	malariaStructs[1].CountStrains()

	return malariaStructs
}

// Checks if two values are the same, and stops the test if they are not.
func CheckIfEqual(t *testing.T, s string, a interface{}, b interface{}) {
	if cmp.Equal(a, b) {
		return
	}
	debug.PrintStack()
	t.Fatalf("Error in %s. The two values are not equal. \n Is: %v. \n Should be: %v", s, a, b)
	return
}

func TestStructCreation(t *testing.T) {
	malariaStructs := CreateMalariaStructsInSlice()

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
	malariaStructs := CreateMalariaStructsInSlice()

	r := CalcRates(&malariaStructs[0], p1)

	NEventTypes := 4
	eventCount := [4]int{0, 0, 0, 0}
	NEvents := int(math.Pow(10, 4))

	for i := 0; i < NEvents; i++ {
		event := ChooseEvent(&malariaStructs[0], p1)
		eventCount[event]++
	}

	rSum := 0.0
	for i := 0; i < NEventTypes; i++ {
		rSum += r[i]
	}
	for i := 0; i < NEventTypes; i++ {
		r[i] = r[i] * float64(NEvents) / rSum
	}

	fmt.Println(eventCount, r)

	return
}

func TestSpread(t *testing.T) {
	//malariaStructs := CreateMalariaStructsInSlice()

	return
}

func TestInfectHost(t *testing.T) {
	malariaStructs := CreateMalariaStructsInSlice()

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
	malariaStructs := CreateMalariaStructsInSlice()

	CheckIfEqual(t, "Antibodies", malariaStructs[0].Hosts[0].Antibodies[0], false)
	malariaStructs[0].ImmunityGained(0)
	CheckIfEqual(t, "Antibodies", malariaStructs[0].Hosts[0].Antibodies[0], true)

	malariaStructs[0].ImmunityGained(0)
	CheckIfEqual(t, "Number of infected", len(malariaStructs[0].InfectedHosts), 0)
	CheckIfEqual(t, "Is Infected", malariaStructs[0].Hosts[0].IsInfected, false)
	CheckIfEqual(t, "Infections", len(malariaStructs[0].Hosts[0].Infections), 0)
}

func TestHasStrain(t *testing.T) {
	m := CreateMalariaStructsInSlice()

	CheckIfEqual(t, "If infection strain is contained in target.", m[1].Hosts[0].HasStrain(&m[1].Hosts[1], 2), false)
	CheckIfEqual(t, "If infection strain is contained in target.", m[1].Hosts[1].HasStrain(&m[1].Hosts[2], 2), true)

	m[1].Hosts[0].InfectHost(&m[1].Hosts[1], 2)
	m[1].Hosts[0].ExpressedStrain[0] = 3
	m[1].Hosts[0].ExpressedStrain[1] = 4

	CheckIfEqual(t, "If infection is correct", m[1].Hosts[0].Infections, []int8{3, 4, 1, 2})

	CheckIfEqual(t, "If infection strain is contained in target.", m[1].Hosts[0].HasStrain(&m[1].Hosts[1], 2), true)
	CheckIfEqual(t, "If infection strain is contained in target.", m[1].Hosts[0].HasStrain(&m[1].Hosts[2], 2), true)
	CheckIfEqual(t, "If infection strain is contained in target.", m[1].Hosts[1].HasStrain(&m[1].Hosts[0], 2), false)

	// m[1].Hosts[0].InfectHost(&m[1].Hosts[1], 2)

	// CheckIfEqual(t, "If infection is correct. Infection to a strain already contained should not happen.", m[1].Hosts[0].Infections, []int8{3, 4, 1, 2})

}

func TestRemoveParasite(t *testing.T) {
	m := CreateMalariaStructsInSlice()

	m[1].Hosts[0].InfectHost(&m[1].Hosts[1], p2.NAntigens)

	m[1].Hosts[0].RemoveParasite(m[1].NAntigens)
	CheckIfEqual(t, "Removing the first parasite by a host infected by 2", m[1].Hosts[0].Infections, []int8{1, 2})
}

func TestReplace(t *testing.T) {
	m := CreateMalariaStructsInSlice()

	m[1].Replace(0)
	m[1].Spread(9, 1)
	m[1].Spread(8, 1)
	m[1].Replace(8)

	CheckIfEqual(t, "Decreased number of infected after replacement", m[1].NInfectedHosts, 3)
	CheckIfEqual(t, "The last index in infectedHosts", m[1].InfectedHosts[2], 9)
	CheckIfEqual(t, "Should not be infected after replacement", m[1].Hosts[8].IsInfected, false)
	CheckIfEqual(t, "Expressed strain, replacement", int(m[1].Hosts[8].ExpressedStrain[0]), 0)
	CheckIfEqual(t, "Infections, replacement", len(m[1].Hosts[8].Infections), 0)

	return
}

func TestCountStrains(t *testing.T) {
	m := CreateMalariaStructsInSlice()

	fmt.Println(m[1].StrainCounter)
	return
}

func TestFindAllStrainCombinations(t *testing.T) {
	strainLen := 1
	antigenMax := 5
	maxStrains, strainCount := FindAllStrainCombinations(strainLen, antigenMax)
	CheckIfEqual(t, "Correct number of maximum strains for strainLen 1", maxStrains, 5)
	fmt.Println(maxStrains, strainCount)

	strainLen = 2
	antigenMax = 5
	maxStrains, strainCount = FindAllStrainCombinations(strainLen, antigenMax)
	CheckIfEqual(t, "Correct number of maximum strains for strainLen 2", maxStrains, 10)
	fmt.Println(maxStrains, strainCount)

	strainLen = 3
	antigenMax = 5
	maxStrains, strainCount = FindAllStrainCombinations(strainLen, antigenMax)
	CheckIfEqual(t, "Correct number of maximum strains for strainLen 3", maxStrains, 10)
	fmt.Println(maxStrains, strainCount)
	return
}

func TestListToString(t *testing.T) {
	s1 := ListToString([]int8{1, 2, 3})
	s2 := ListToString([]int8{13})
	CheckIfEqual(t, "List to string", s1, "1,2,3")
	CheckIfEqual(t, "List to string", s2, "13")

	s := []int8{3, 2, 5, 8, 1}
	sort.Slice(s, func(i, j int) bool { return s[i] < s[j] })
	CheckIfEqual(t, "Sorting int8 slice", s, []int8{1, 2, 3, 5, 8})

	return
}

func TestCheckUniqueInt8(t *testing.T) {
	s1 := []int8{2, 6, 48, 100}
	s2 := []int8{4, 3, 98, 5, 98}

	t1 := CheckUniqueInt8(s1[0:len(s1)-1], s1[len(s1)-1])
	t2 := CheckUniqueInt8(s2[0:len(s2)-1], s2[len(s2)-1])

	CheckIfEqual(t, "End index in int8 slice is unique", t1, true)
	CheckIfEqual(t, "End index in int8 slice is unique", t2, false)

}

func TestInsertRandomInfection(t *testing.T) {
	m := CreateMalariaStructsInSlice()

	for hostIndex := 0; hostIndex < m[1].NHosts; hostIndex++ {
		m[1].Hosts[hostIndex].InsertRandomInfection(2, 2)
		CheckIfEqual(t, "Random infection all antigens unique in same strain", m[1].Hosts[hostIndex].ExpressedStrain, []int8{0, 1})
		CheckIfEqual(t, "Random infection all antigens unique in same strain", m[1].Hosts[hostIndex].Infections, []int8{0, 1})
	}

}

/*


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
