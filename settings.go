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
	InfectionSpeed   float64 // The rate of which malaria spreads.
	ImmunitySpeed    float64 // The rate of gaining immunity to a single antigen.  Always set to 1.0
	MutationSpeed    float64 //  The rate of strains to switch a random antigen to a new random one.
	ReplacementSpeed float64 // The rate of hosts death.

	// Other setting that changes the behaviour of the system
	NHosts             int // Number of hosts
	NAntigens          int // The number of antigens each strain contains
	MaxAntigenValue    int // The maximum value a single antigen can take. In other words it decides the number of different antigens.
	InitialInfected    int // How many infected there is at start of simulation.
	MaxSuperInfections int // The maximum number of infections a single host can have
}

// ModelSettings : A structure that contains information ab	out model settings such as
type ModelSettings struct {
	Runs       int // Number of runs
	BurnIn     int // Number of runs that is not counted
	SkipSaving int // Number of runs for each saving
	Repeat     int // How many times the simulation should be repeated for each parameter.

	ShouldSaveData             bool // Should the program run with saving data?
	ShouldSaveDataWhileRunning bool // Should the program run with saving date after some number of steps
	ShouldCreateNewDataFile    bool // Should the program create a new data file og append to the data file that already exists.

	DataFileName string // The name of the files that belong to this run.
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
