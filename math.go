package main

import (
	"fmt"
	"log"
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
			fmt.Println("Warning", m.Hosts[host].Infections, host, m.Hosts[host].IsInfected, len(m.InfectedHosts), m.NInfectedHosts)
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
func (h *Host) HasStrain(strain []int8, NAntigens int, MaxSuperInfection int) bool {
	NInfections := len(h.Infections) / NAntigens
	var correctCount int

	for infectionNumber := 0; infectionNumber < MaxSuperInfection; infectionNumber++ {
		correctCount = 0
		for antigenIndex, antigen := range strain {
			if h.Infections[infectionNumber][antigenIndex] == antigen {
				correctCount++
				if correctCount == NAntigens {
					return true
				}
			} else {
				break
			}
		}
	}

	return false
}

// CountNumberOfUniqueAntigens : Counts the number of unique antigens an all hosts. s
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

// FindAllStrainCombinations :
func FindAllStrainCombinations(strainLen int, antigenMax int) (int, []string, map[string]int) {

	if strainLen > antigenMax {
		panic("Strain length is greater than the maximum possible antigen value")
	}

	var strains [][]int8
	var strainCounter []int
	maxStrains := 0

	if strainLen == 1 {
		for i := 1; i < antigenMax+1; i++ {
			strains = append(strains, []int8{i})
			strainCounter = append(strainCounter, 0)
			maxStrains++
		}

	} else if strainLen == 2 {

		for i := 1; i < antigenMax; i++ {
			for j := i + 1; j < antigenMax+1; j++ {
				strains = append(strains, [][]int8{i, j})
				strainCounter = append(strainCounter, 0)
				maxStrains++
			}
		}

	} else if strainLen == 3 {
		for i := 1; i < antigenMax-1; i++ {
			for j := i + 1; j < antigenMax; j++ {
				for k := j + 1; k < antigenMax+1; k++ {
					strains = append(strains, [][]int8{i, j, k})
					strainCounter = append(strainCounter, 0)
					maxStrains++
				}
			}
		}
	}

	return maxStrains, strainKeys, strainCount
}

// CountStrains : Count the strains and change StrainCounter variable in malaria struct.
func (m *Malaria) CountStrains() {

	for key := range m.StrainCounter {
		m.StrainCounter[key] = 0
	}

	for i := 0; i < m.NHosts; i++ {
		if m.Hosts[i].IsInfected {
			nInfections := CountInfections(m.Hosts[i].Infections, m.NAntigens)
			for j := 0; j < nInfections; j++ {
				m.StrainCounter[ListToString(m.Hosts[i].Infections[j*m.NAntigens:j*m.NAntigens+m.NAntigens])]++
			}
		}
	}
	return
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

// CountInfections : Counts the number of infection of a int8 slice
func CountInfections(infections []int8, NAntigens int) int {
	return int(len(infections) / NAntigens)
}

// 1, 4, 3+2+1 2+1 1, 20
