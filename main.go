package main

import (
	"fmt"
	"io"
	"io/ioutil"
	"os"
	"strconv"
	"time"
)

// We define a set of global constant
const path = "data/" + "mutation2DLowReplacement/"

// main
func main() {
	fmt.Println("Starting")
	PrintNotes()

	startTime := time.Now()
	InitiateRunningModel()
	endTime := time.Now()
	fmt.Println("The end. Congrats! The whole run took:", endTime.Sub(startTime), "d")
}

// PrintNotes : Print the notes in the data file.
func PrintNotes() {
	if _, err := os.Stat(path + "notes.txt"); os.IsNotExist(err) {
		fmt.Println("Notes does not exist")
	} else {
		b, err := ioutil.ReadFile(path + "notes.txt")
		if err != nil {
			panic(err)
		}
		fmt.Println(string(b))
	}
	return
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
			GetReadyToStartModelSaveAndCreateDataFiles(param, settings, i)
		}
		i++
	}
	return
}

// GetReadyToStartModelSaveAndCreateDataFiles : This is getting really confusing. So many nested functions. No idea how to change it though.
func GetReadyToStartModelSaveAndCreateDataFiles(param Parameters, settings ModelSettings, i int) {

	var run int
	var m *Malaria

	for j := 0; j < settings.Repeat; j++ {
		dataFileName := path + "timeline/" + strconv.Itoa(i) + "_" + strconv.Itoa(j+1)
		run, m = StartModel(param, settings, dataFileName)
		if settings.ShouldSaveData == true {
			SaveToEndFile(dataFileName+".csv", settings.DataFileName, run, m)
			if settings.ShouldSaveDataWhileRunning == false {
				time.Sleep(time.Second)
				err := os.Remove(dataFileName + ".csv")
				check(err)
				err = os.Remove(dataFileName + "strainCounter" + ".csv")
				check(err)
			}
		}
	}
}

// StartModel : Starts the run of the malaria model
func StartModel(param Parameters, settings ModelSettings, dataFileName string) (int, *Malaria) {
	modelTime := 0
	startTime := time.Now()

	m := ConstructMalariaStruct(param)

	m.RunBurnIn(param, settings.BurnIn)
	var run int
	if m.NInfectedHosts != 0 {
		run = m.RunModel(param, settings, dataFileName)
	} else {
		fmt.Println("Malaria died in burnin")
	}

	endTime := time.Now()

	fmt.Println("This set of Parameters, done.", "\n It had the following parameters:", param, "\n It took intime:", modelTime, "\n It took realtime:", endTime.Sub(startTime))

	return run, &m
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
func (m *Malaria) RunModel(param Parameters, setting ModelSettings, dataFileName string) int {

	file := CreateTimelineFile(dataFileName + ".csv")
	file_strainCounter := CreateStrainCounterFile(dataFileName + "strainCounter" + ".csv")

	run := 0

	for run = 0; run < setting.Runs; run++ {

		m.EventHappens(param)
		if run%setting.SkipSaving == 0 {
			SaveTimeline(file, &run, &m.NInfectedHosts)
			SaveStrainCounter(file_strainCounter, &m.StrainCounter)
			if run%5000000 == 0 {
				fmt.Println(run)
			}
		}
		if m.NInfectedHosts == 0 {
			fmt.Println("Malaria is dead in", run, "runs")
			SaveTimeline(file, &run, &m.NInfectedHosts)
			SaveStrainCounter(file_strainCounter, &m.StrainCounter)
			break
		}
	}

	file.Close()
	file_strainCounter.Close()
	time.Sleep(time.Second) // Wait a bit for the system to follow up.
	return run
}
