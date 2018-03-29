package main

import (
	"fmt"
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

func check(e error) {
	if e != nil {
		panic(e)
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
