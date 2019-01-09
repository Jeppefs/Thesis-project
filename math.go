package main

import (
	"fmt"
	"log"
	"math/rand"
	"sort"
	"strconv"
)

// SumSlice : Returns the sum a float64 slice.
func SumSlice(X []float64) float64 {
	sum := 0.0
	for _, x := range X {
		sum += x
	}
	return sum
}

func check(err error) {
	if err != nil {
		log.Fatal(err)
	}
}

// CalcMeanAndVar : Calculates mean and variance and return values. Only works for a slice of float64.
func CalcMeanAndVar(data []float64) (float64, float64) {
	mean := 0.0
	variance := 0.0
	N := float64(len(data))

	for _, dataPoint := range data {
		mean += dataPoint
	}
	mean = mean / N
	for _, dataPoint := range data {
		variance += (dataPoint - mean) * (dataPoint - mean)
	}
	variance = variance / N
	return mean, variance
}

// CheckIfAllInfectedHasInfection : Check if every host that has true in the infected value is actually infected. For testing
func (m *Malaria) CheckIfAllInfectedHasInfection(q int) {
	for _, host := range m.InfectedHosts {
		if len(m.Hosts[host].Infections) == 0 {
			fmt.Println("Warning", m.Hosts[host].Infections, host, m.Hosts[host].NInfections, len(m.InfectedHosts), m.NInfectedHosts)
			if q == 2 {
				panic(strconv.Itoa(q))
			}
		}
	}
}

// CheckIfAllIsUnique : For a given int slice, this checks if all value in the array is actually unique. Panics if it isn't
func CheckIfAllIsUnique(q []int) {
	sort.Ints(q)
	for i := 0; i <= len(q)-2; i++ {
		if q[i] == q[i+1] {
			fmt.Println(q[i])
			panic("e")
		}
	}

}

// CountBolleanArray : Takes a boolean array and return the number of true values
func CountBolleanArray(b []bool) int {
	sum := 0
	for _, val := range b {
		if val {
			sum++
		}
	}
	return sum
}

// HasStrain : Checks if the host has the expressed strain of the input host.
func (h *Host) HasStrain(strainIndex int) bool {

	for _, infection := range h.Infections {
		if infection == strainIndex {
			return true
		}
	}

	return false
}

// CountNumberOfUniqueAntigens : Counts the number of unique antigens an all hosts. s
/*
func (m *Malaria) CountNumberOfUniqueAntigens() {
	AntigenExistence := make([]bool, m.MaxAntigenValue)
	for _, host := range m.Hosts {
		for _, antigen := range host.ExpressedStrain {
			AntigenExistence[antigen] = true
		}
	}
	m.NDifferentAntigens = CountBolleanArray(AntigenExistence)
	return
}
*/

// FindAllStrainCombinations :
func FindAllStrainCombinations(strainLen int, antigenMax int) (int, [][]int8, []int) {

	if strainLen > antigenMax {
		panic("Strain length is greater than the maximum possible antigen value")
	}

	var strains [][]int8
	var strainCounter []int
	maxStrains := 0

	if strainLen == 1 {
		for i := 1; i < antigenMax+1; i++ {
			strains = append(strains, []int8{int8(i)})
			strainCounter = append(strainCounter, 0)
			maxStrains++
		}

	} else if strainLen == 2 {

		for i := 1; i < antigenMax; i++ {
			for j := i + 1; j < antigenMax+1; j++ {
				strains = append(strains, []int8{int8(i), int8(j)})
				strainCounter = append(strainCounter, 0)
				maxStrains++
			}
		}

	} else if strainLen == 3 {
		for i := 1; i < antigenMax-1; i++ {
			for j := i + 1; j < antigenMax; j++ {
				for k := j + 1; k < antigenMax+1; k++ {
					strains = append(strains, []int8{int8(i), int8(j), int8(k)})
					strainCounter = append(strainCounter, 0)
					maxStrains++
				}
			}
		}
	}

	return maxStrains, strains, strainCounter
}

// CountStrains : Count the strains and change StrainCounter variable in malaria struct.
func (m *Malaria) CountStrains() {

	for i, _ := range m.StrainCounter {
		m.StrainCounter[i] = 0
	}

	for _, host := range m.Hosts {
		for _, strainIndex := range host.Infections {
			m.StrainCounter[strainIndex]++
		}
	}
	return
}

// GetRandomStrainIndex : Retrieve a random strain index from an infected host
// Returns the index of the strain in the infection of the host and the strain index in m.Strains
func (h *Host) GetRandomStrainIndex() (int, int) {
	infectionIndexInHost := rand.Intn(h.NInfections)
	return infectionIndexInHost, h.Infections[infectionIndexInHost]
}

// ListToString : Converts a list of intergers to a string with komma seperation
func ListToString(list []int8) string {
	s := ""
	for i := 0; i < len(list); i++ {
		if i == 0 {
			s += strconv.Itoa(int(list[i]))
		} else {
			s += "," + strconv.Itoa(int(list[i]))
		}
	}

	return s
}

// CheckUniqueInt8 : Checks if a number already exist in a slice.
func CheckUniqueInt8(s []int8, v int8) bool {

	for _, val := range s {
		if val == v {
			return false
		}
	}

	return true
}

// GetRandomInfectionIndex : For a single host, get his inde of a random infection
func (h *Host) GetRandomInfectionIndex() int {
	return rand.Intn(h.NInfections)
}

// GetRandomStrain : returns a number corresponding to a random strain.
func (m *Malaria) GetRandomStrain() int {
	return rand.Intn(m.MaxStrains)
}

func CountCurrentNumberOfStrains(strainCounter []int) int {
	total := 0
	for i := 0; i < len(strainCounter); i++ {
		if strainCounter[i] > 0 {
			total++
		}
	}

	return total
}

// GetRandomInfectedHost :
func (m *Malaria) GetRandomInfectedHost() (Host, int, int) {
	infectedHostIndex := rand.Intn(m.NInfectedHosts)
	hostIndex := m.InfectedHosts[infectedHostIndex]
	host := m.Hosts[hostIndex]
	return host, hostIndex, infectedHostIndex
}

// GetMaxAndIndexIntSlice : Finds the maximum value and corresponding index of an []int
func GetMaxAndIndexIntSlice(s []int) (int, int) {
	var value int
	var index int

	for i, v := range s {
		if i == 0 || v > value {
			value = v
			index = i
		}
	}

	return value, index
}
