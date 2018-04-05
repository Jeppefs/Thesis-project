package main

import (
	"fmt"
	"io"
	"log"
	"reflect"
	"strconv"
)

// Parameters : Sets the parameters for a particular run. These are all set before the simulation.
type Parameters struct {
	// Parameters used when calculating rates and probabilities for next event.
	InfectionSpeed float64
	ImmunitySpeed  float64
	MutationSpeed  float64
	DeathSpeed     float64

	// Other setting that changes the behaviour of the system
	NHosts          int
	NAntigens       int
	MaxAntigenValue int
}

// ModelSettings : A structure that contains information ab	out model settings such as
type ModelSettings struct {
	SingleFiles bool

	BurnIn int
	Runs   int

	Test                    bool
	AppendToCurrentDataFile bool

	MultipleInfections bool

	CurrentDataFile string
}

// InsertParameters : Insert parameters into the parameters struct given a string slice.
func InsertParameters(header []string, records []string) Parameters {
	var param Parameters

	for j := 0; j < len(records); j++ {
		v := reflect.ValueOf(&param)
		f := v.Elem().FieldByName(header[j])
		if f.IsValid() && f.CanSet() {
			if f.Kind() == reflect.String {
				f.SetString(records[j])
			} else if f.Kind() == reflect.Int {
				q, _ := strconv.Atoi(records[j])
				f.SetInt(int64(q))
			} else if f.Kind() == reflect.Float64 {
				q, _ := strconv.ParseFloat(records[j], 64)
				f.SetFloat(q)
			} else if f.Kind() == reflect.Bool {
				q, _ := strconv.ParseBool(records[j])
				f.SetBool(q)
			} else {
				log.Fatalln("Was not any of the four types")
			}
		} else {
			fmt.Println("This key is not valid", header[j])
		}
	}

	return param
}

// InsertSettings : Inserts the settings in a setting struct. It does so dynamically to the name in the header. If the name in the header does not correspond to the name in the struct, it will return an error message
func InsertSettings(fileName string) ModelSettings {

	var setting ModelSettings
	r := LoadCSVFile(fileName)

	i := 0
	var header []string

	for {
		records, err := r.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			log.Fatal(err)
		}

		if i == 0 {
			for j := 0; j < len(records); j++ {
				header = append(header, records[j])
			}
		} else {
			for j := 0; j < len(records); j++ {
				v := reflect.ValueOf(&setting)
				f := v.Elem().FieldByName(header[j])
				if f.IsValid() && f.CanSet() {
					if f.Kind() == reflect.String {
						f.SetString(records[j])
					} else if f.Kind() == reflect.Int {
						q, _ := strconv.Atoi(records[j])
						f.SetInt(int64(q))
					} else if f.Kind() == reflect.Float64 {
						q, _ := strconv.ParseFloat(records[j], 64)
						f.SetFloat(q)
					} else if f.Kind() == reflect.Bool {
						q, _ := strconv.ParseBool(records[j])
						f.SetBool(q)
					} else {
						log.Fatalln("Was not any of the four types")
					}
				} else {
					log.Fatalln("This key is not valid while inserting settings: ", header[j])
				}
			}
		}

		i++
	}
	return setting

}

/*
// MakeModelSetting : Constructs the ModelSettings struct, which sets how the data should be saved, if a burnin should exist and so on.
func MakeModelSetting() ModelSettings {

	var setting ModelSettings

	setting.Runs = 25000000 // Usually 5000000
	setting.BurnIn = 0      // Usually 5000000

	setting.Test = true
	setting.AppendToCurrentDataFile = true

	setting.MultipleInfections = true

	setting.CurrentDataFile = "data/avgFile3.txt"

	return setting
}

// MakeParameterGrid : Creates a parameter grid to search through. Also where settings as applied.
func MakeParameterGrid() []Parameters {
	gridsize := 100

	parameterGrid := make([]Parameters, gridsize)

	for i := 0; i < gridsize; i++ {
		parameterGrid[i].InfectionSpeed = 0.99 //+ float64(i)/1000.0
		parameterGrid[i].ImmunitySpeed = 1.0
		parameterGrid[i].MutationSpeed = 0.0
		parameterGrid[i].DeathSpeed = float64(i) / 1000

		parameterGrid[i].NHosts = 10000
		parameterGrid[i].NAntigens = 1
		parameterGrid[i].MaxAntigenValue = 1
	}

	return parameterGrid
}
*/
