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

	malariaStructs[1].Hosts[0].Infections[0] = 7 // [3, 4]
	malariaStructs[1].Hosts[1].Infections[0] = 0 // [1, 2]
	malariaStructs[1].Hosts[2].Infections[0] = 0

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

	CheckIfEqual(t, "IsInfected", malariaStructs[0].Hosts[0].NInfections, 1)
	CheckIfEqual(t, "IsInfected", malariaStructs[1].Hosts[2].NInfections, 1)
	CheckIfEqual(t, "IsInfected", malariaStructs[0].Hosts[5].NInfections, 0)
	CheckIfEqual(t, "IsInfected", malariaStructs[0].Hosts[1].NInfections, 0)

	CheckIfEqual(t, "Infections", malariaStructs[0].Hosts[0].Infections, []int{0})
	CheckIfEqual(t, "Number of infections", len(malariaStructs[1].Hosts[0].Infections), 1)
	CheckIfEqual(t, "Number of antigens in a strains", len(malariaStructs[1].Strains[malariaStructs[1].Hosts[0].Infections[0]]), 2)

	CheckIfEqual(t, "Is healthy host empty", len(malariaStructs[0].Hosts[4].Infections), 0)
	CheckIfEqual(t, "Is healthy host empty", len(malariaStructs[0].Hosts[0].Infections), 1)
	CheckIfEqual(t, "Is healthy host empty", len(malariaStructs[1].Hosts[2].Infections), 1)

	CheckIfEqual(t, "Has correct strain", malariaStructs[1].Strains[malariaStructs[1].Hosts[0].Infections[0]], []int8{3, 4})
	CheckIfEqual(t, "Has correct strain", malariaStructs[1].Strains[malariaStructs[1].Hosts[1].Infections[0]], []int8{1, 2})
	CheckIfEqual(t, "Has correct strain", malariaStructs[1].Strains[malariaStructs[1].Hosts[2].Infections[0]], []int8{1, 2})
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
	m := CreateMalariaStructsInSlice()

	m[1].Spread(3, m[1].Hosts[0].Infections[0], 5)
	CheckIfEqual(t, "NInfected after infection", m[1].NInfectedHosts, 4)
	CheckIfEqual(t, "NInfected after infection", m[1].NInfectedHosts, 4)
	CheckIfEqual(t, "StrainCounter after infections", m[1].StrainCounter[m[1].Hosts[0].Infections[0]], 2)
	CheckIfEqual(t, "StrainCounter after infections", m[1].StrainCounter[0], 2)
	CheckIfEqual(t, "StrainCounter after infections", m[1].StrainCounter[1], 0)

	m[1].Spread(3, m[1].Hosts[1].Infections[0], 5)
	CheckIfEqual(t, "NInfected after infection", m[1].NInfectedHosts, 4)
	CheckIfEqual(t, "StrainCounter after infections", m[1].StrainCounter[m[1].Hosts[0].Infections[0]], 2)
	CheckIfEqual(t, "StrainCounter after infections", m[1].StrainCounter[0], 3)
	CheckIfEqual(t, "StrainCounter after infections", m[1].StrainCounter[1], 0)

	// Testing whether it denies another infection of the the same strain it already has.
	m[1].Spread(3, m[1].Hosts[1].Infections[0], 5)
	CheckIfEqual(t, "whether a host becomes infected by the same strain", m[1].NInfectedHosts, 4)
	CheckIfEqual(t, "whether a host becomes infected by the same strain", m[1].Hosts[3].Infections, []int{7, 0})
	CheckIfEqual(t, "whether a host becomes infected by the same strain", m[1].StrainCounter[m[1].Hosts[1].Infections[0]], 3)

	return
}

func TestInfectHost(t *testing.T) {
	m := CreateMalariaStructsInSlice()

	m[0].Hosts[4].InfectHost(m[0].Hosts[0].Infections[0])
	CheckIfEqual(t, "Newly infected has same infections", m[0].Hosts[4].Infections, m[0].Hosts[0].Infections)

	m[0].Hosts[1].InfectHost(m[0].Hosts[0].Infections[0])
	m[0].Hosts[1].InfectHost(m[0].Hosts[0].Infections[0])
	CheckIfEqual(t, "Newly infected has same infections", m[0].Hosts[1].Infections, []int{m[0].Hosts[0].Infections[0], m[0].Hosts[0].Infections[0]}) // Is [0, 0]. This should happen when using the InfectHost method, but not the spread method.

	m[1].Hosts[5].InfectHost(m[1].Hosts[0].Infections[0])
	m[1].Hosts[5].InfectHost(m[1].Hosts[1].Infections[0])

	CheckIfEqual(t, "Super Infection with same strain", m[1].Hosts[5].Infections, []int{m[1].Hosts[0].Infections[0], m[1].Hosts[1].Infections[0]})
	return

}

func TestCombineParasite(t *testing.T) {

	return
}

func TestImmunity(t *testing.T) {
	fmt.Println("\n Testing immunity")
	m := CreateMalariaStructsInSlice()

	CheckIfEqual(t, "Antibodies", m[0].Hosts[0].Antibodies[0], false)
	m[0].ImmunityGained(0)
	m[0].ImmunityGained(0)
	CheckIfEqual(t, "Antibodies", m[0].Hosts[0].Antibodies[0], true)
	CheckIfEqual(t, "Number of infected", len(m[0].InfectedHosts), 0)
	CheckIfEqual(t, "Is Infected", m[0].Hosts[0].NInfections, 0)
	CheckIfEqual(t, "Infections", len(m[0].Hosts[0].Infections), 0)

	m[1].ImmunityGained(0)
	m[1].ImmunityGained(0)
	m[1].ImmunityGained(0)
	CheckIfEqual(t, "Is Infected", m[1].Hosts[0].NInfections, 0)
	CheckIfEqual(t, "Infections", len(m[1].Hosts[0].Infections), 0)
	CheckIfEqual(t, "StrainCounter after immunity", m[1].StrainCounter[7], 0)

}

func TestHasStrain(t *testing.T) {
	m := CreateMalariaStructsInSlice()

	CheckIfEqual(t, "If infection strain is contained in target.", m[1].Hosts[0].HasStrain(m[1].Hosts[1].Infections[0]), false)
	CheckIfEqual(t, "If infection strain is contained in target.", m[1].Hosts[1].HasStrain(m[1].Hosts[2].Infections[0]), true)

}

func TestReplace(t *testing.T) {
	m := CreateMalariaStructsInSlice()

	strain_1_2 := m[1].Hosts[1].Infections[0]
	strain_3_4 := m[1].Hosts[0].Infections[0]

	m[1].Spread(9, strain_1_2, 5)
	m[1].Spread(8, strain_1_2, 5)
	m[1].Spread(8, strain_3_4, 5)

	m[1].Replace(0)
	m[1].Replace(8)

	CheckIfEqual(t, "Decreased number of infected after replacement", m[1].NInfectedHosts, 3)
	CheckIfEqual(t, "The last index in infectedHosts", m[1].InfectedHosts[2], 9)
	CheckIfEqual(t, "Should not be infected after replacement", m[1].Hosts[8].NInfections, 0)
	CheckIfEqual(t, "Infections, replacement", len(m[1].Hosts[8].Infections), 0)
	CheckIfEqual(t, "StrainCounter replacement", m[1].StrainCounter[strain_1_2], 3)
	CheckIfEqual(t, "StrainCounter replacement", m[1].StrainCounter[strain_3_4], 0)

	return
}

func TestCountStrains(t *testing.T) {
	m := CreateMalariaStructsInSlice()

	fmt.Println(m[1].StrainCounter)
	return
}

func TestFindAllStrainCombinations(t *testing.T) {
	fmt.Println("Testing strain combinations")
	strainLen := 1
	antigenMax := 5
	maxStrains, strainAntigens, strainCount := FindAllStrainCombinations(strainLen, antigenMax)
	fmt.Println(maxStrains, strainCount)
	CheckIfEqual(t, "Correct number of maximum strains for strainLen 1", maxStrains, 5)
	CheckIfEqual(t, "Strain keys for strainLen 1", strainAntigens, [][]int8{{1}, {2}, {3}, {4}, {5}})

	strainLen = 2
	antigenMax = 5
	maxStrains, strainAntigens, strainCount = FindAllStrainCombinations(strainLen, antigenMax)
	fmt.Println(maxStrains, strainCount)
	CheckIfEqual(t, "Correct number of maximum strains for strainLen 2", maxStrains, 10)
	CheckIfEqual(t, "Strain keys for strainLen 2", strainAntigens, [][]int8{{1, 2}, {1, 3}, {1, 4}, {1, 5}, {2, 3}, {2, 4}, {2, 5}, {3, 4}, {3, 5}, {4, 5}})

	strainLen = 3
	antigenMax = 5
	maxStrains, strainAntigens, strainCount = FindAllStrainCombinations(strainLen, antigenMax)
	fmt.Println(maxStrains, strainCount)
	CheckIfEqual(t, "Correct number of maximum strains for strainLen 3", maxStrains, 10)
	CheckIfEqual(t, "Strain keys for strainLen 1", strainAntigens, [][]int8{{1, 2, 3}, {1, 2, 4}, {1, 2, 5}, {1, 3, 4}, {1, 3, 5}, {1, 4, 5}, {2, 3, 4}, {2, 3, 5}, {2, 4, 5}, {3, 4, 5}})

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

func TestCalcMeanAndVar(t *testing.T) {
	data := []float64{1.0, 2.0, 3.0, 4.0, 5.0}
	mean, variance := CalcMeanAndVar(data)
	if mean != 3.0 {
		t.Fatalf("Mean incorrect")
	}
	if variance != 2.0 {
		t.Fatalf("variance incorrect. Is: %f. Should be: %f", variance, 2.0)
	}
	return
}
