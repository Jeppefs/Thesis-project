/*
	TODO:
	- Make better tests for Immunity and Spread.
*/

package main

import (
	"fmt"
	"io"
	"os"
	"strconv"
	"time"
)

// We define a set of global constant - mostly
const path = "data/" + "VaryAntigen/"

// main
func main() {
	fmt.Println("Starting")
	startTime := time.Now()
	InitiateRunningModel()
	endTime := time.Now()
	fmt.Println("The end. Congrats! The whole run took:", endTime.Sub(startTime), "d")
}

// InitiateRunningModel : Starts the whole simulation and sets the parameter-grid.
func InitiateRunningModel() {

	settings := InsertSettings(path + "settings.csv")

	CheckToCreateNedEndDataFileAndDoSoIfTrue(&settings)

	GetParametersAndStartTheThing(settings)

	return
}

// GetParametersAndStartTheThing : Gets the parameters given in the file, and start the model using the parameters gotten.
func GetParametersAndStartTheThing(settings ModelSettings) {
	r := LoadCSVFile(path + "parameters.csv")

	var run int
	var header []string

	i := 0

	for {

		records, err := r.Read()
		if err == io.EOF {
			break
		}
		check(err)

		if i == 0 {
			for j := 0; j < len(records); j++ {
				header = append(header, records[j])
			}
		} else {
			param := InsertParameters(header, records)
			for j := 0; j < settings.Repeat; j++ {
				run = StartModel(param, settings)
				if settings.ShouldSaveData {
					SaveToEndFile("temp.txt", settings.DataFileName, run)
					if settings.ShouldSaveDataWhileRunning {
						os.Rename(path+"temp.txt", path+"xDataSim_"+strconv.Itoa(i)+"_"+strconv.Itoa(j)+".csv")
					}
				}
			}
		}
		i++
	}
	return
}

// StartModel : Starts the run of the malaria model
func StartModel(param Parameters, settings ModelSettings) int {
	modelTime := 0
	startTime := time.Now()
	m := ConstructMalariaStruct(param)

	m.RunBurnIn(param, settings.BurnIn)
	var run int
	if m.NInfectedHosts != 0 {
		run = m.RunModel(param, settings)
	}

	endTime := time.Now()

	fmt.Println("This set of Parameters, done.", "\n It had the following parameters:", param, "\n It took intime:", modelTime, "\n It took realtime:", endTime.Sub(startTime))

	return run
}

// RunBurnIn : Runs the model N times given by the burnin settings. None of the data will be saved.
func (m *Malaria) RunBurnIn(param Parameters, burnIn int) {
	for run := 0; run < burnIn; run++ {
		m.EventHappens(param)
		if m.NInfectedHosts == 0 {
			fmt.Println("Malaria is dead in", burnIn, "runs. This Happened in burnin")
			return
		}
	}
	return
}

// RunModel :
func (m *Malaria) RunModel(param Parameters, setting ModelSettings) int {

	fileName := "temp"
	file, err := os.Create(path + fileName + ".txt")
	check(err)
	defer file.Close()

	run := 0

	for run = 0; run < setting.Runs; run++ {

		m.EventHappens(param)
		if run%100 == 0 {
			fmt.Fprintf(file, "%v \n", m.NInfectedHosts)
			if run%2000000 == 0 {
				fmt.Println(run)
			}
		}
		if m.NInfectedHosts == 0 {
			fmt.Println("Malaria is dead in", run, "runs")
			fmt.Fprintf(file, "%v \n", m.NInfectedHosts)
			break
		}
	}
	return run
}
