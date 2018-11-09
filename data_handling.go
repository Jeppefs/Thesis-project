package main

import (
	"bufio"
	"encoding/csv"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"strconv"
	"strings"
)

// SaveToEndFile :  Saves ending data
// WARNING! : THERE MUST BE A LINESKIP AT END OF FILE TO REGARD THE LAST NUMBER
func SaveToEndFile(loadFileName string, saveFileName string, run int, m *Malaria) {
	csvFile, errTemp := os.Open(loadFileName)
	check(errTemp)
	defer csvFile.Close()
	reader := csv.NewReader(bufio.NewReader(csvFile))
	var d []float64

	lineNumber := 0

	for {
		line, err := reader.Read()
		if err == io.EOF {
			break
		} else if err != nil {
			log.Fatal(err)
		}
		if lineNumber > 0 {
			floatTemp, _ := strconv.ParseFloat(line[1], 64)
			d = append(d, floatTemp)
		}
		lineNumber++
	}

	file, err := os.OpenFile(path+saveFileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	check(err)
	defer file.Close()

	//mean, variance := CalcMeanAndVar(d)
	halfMean, halfVariance := CalcMeanAndVar(d[len(d)/2 : len(d)])

	fmt.Fprintf(file, "%v,%f,%f,%f,%v\n", run, halfMean, halfVariance, CountAverageResistances(m), CountCurrentNumberOfStrains(m.StrainCounter)) // Important, must be the same order as the header.

	return
}

// CheckToCreateNedEndDataFileAndDoSoIfTrue : Creates new end data file if it does not exist, or if we want a clean run.
func CheckToCreateNedEndDataFileAndDoSoIfTrue(settings *ModelSettings) {
	// This creates a new data file if it does not alrady exist or we simply want a clean run (no appending).
	if _, err := os.Stat(path + settings.DataFileName); err == nil {
		if settings.ShouldCreateNewDataFile {
			CreateAvgDataFile(path + settings.DataFileName)
		}
	} else {
		CreateAvgDataFile(path + settings.DataFileName)
	}
	return
}

// CreateAvgDataFile : Creates the data file to save run mean and variance. Also inserts the header.
func CreateAvgDataFile(fileName string) {
	file, err := os.Create(fileName)
	check(err)
	fmt.Fprintf(file, "%s,%s,%s,%s,%s\n", "run", "mean", "variance", "avgResistances", "strains")
	file.Close()
	return
}

// LoadCSVFile :
func LoadCSVFile(fileName string) *csv.Reader {

	file, err := ioutil.ReadFile(fileName)

	if err != nil {
		log.Fatal(err)
	}
	r := csv.NewReader(strings.NewReader(string(file)))

	return r
}

// CreateTimelineFile : Creates the header for timeline daa
func CreateTimelineFile(dataFileName string) *os.File {
	file, err := os.Create(dataFileName)
	check(err)
	fmt.Fprintf(file, "%s,%s\n", "run", "infected")
	return file
}

// CreateStrainCounterFile : Creates the file that saves the strains.
func CreateStrainCounterFile(dataFileName string) *os.File {
	file, err := os.Create(dataFileName)
	check(err)
	return file
}

// SaveTimeline : Save current state to timeline data
func SaveTimeline(file *os.File, run *int, NInfected *int) {
	fmt.Fprintf(file, "%v,%v\n", *run, *NInfected)
	return
}

// SaveStrainCounter : Save strainCounter
func SaveStrainCounter(file *os.File, strainCounter *[]int) {
	for i, count := range *strainCounter {
		if i == len(*strainCounter) {
			fmt.Fprintf(file, "%v", count)
		} else {
			fmt.Fprintf(file, "%v,", count)
		}
	}
	fmt.Fprintf(file, "\n")
	return
}

// CountAverageResistances : Counts the number of total resistances among the whole population
func CountAverageResistances(m *Malaria) float64 {

	resistanceCount := 0

	for hostIndex := 0; hostIndex < m.NHosts; hostIndex++ {
		for _, resistance := range m.Hosts[hostIndex].Antibodies {
			if resistance {
				resistanceCount++
			}
		}
	}

	return float64(resistanceCount) / float64(m.NHosts)
}
