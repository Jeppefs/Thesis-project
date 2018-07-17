package main

import (
	"encoding/csv"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strconv"
	"strings"
)

// SaveToEndFile :  Saves data in the test file
// WARNING! : THERE MUST BE A LINESKIP AT END OF FILE TO REGARD THE LAST NUMBER
func SaveToEndFile(loadFileName string, saveFileName string, run int) {
	data, err := ioutil.ReadFile(loadFileName)
	check(err)
	stringData := string(data)

	var s string
	var sSum string
	var d []float64
	var q int

	for _, k := range stringData {
		s = string(k)
		if (s != "\n") && (s != " ") && (s != "\t") && (k != 13) {
			sSum += s
		}
		if s == "\n" {
			q, _ = strconv.Atoi(sSum)
			d = append(d, float64(q))
			sSum = ""
		}
	}

	file, err := os.OpenFile(path+saveFileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	check(err)
	defer file.Close()

	mean, variance := CalcMeanAndVar(d)

	fmt.Fprintf(file, "%v,%f,%f\n", run, mean, variance) // Important, must be the same order as the header.

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
	fmt.Fprintf(file, "%s,%s,%s\n", "run", "mean", "variance")
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
func CreateTimelineFile(DataFileName string) *os.File {
	file, err := os.Create(DataFileName)
	check(err)
	fmt.Fprintf(file, "%s,%s\n", "run", "infected")
	return file
}

// SaveTimeline : Save current state to timeline data
func SaveTimeline(file *os.File, run *int, NInfected *int) {
	fmt.Fprintf(file, "%v,%v\n", *run, *NInfected)
	return
}
