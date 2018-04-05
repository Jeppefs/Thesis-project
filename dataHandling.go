package main

import (
	"encoding/csv"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"reflect"
	"strconv"
	"strings"
)

// SaveToEndFile :  Saves data in the test file
// WARNING! : THERE MUSTS BE AN LINESKIP AT END OF FILE TO REGARD THE LAST NUMBER
func SaveToEndFile(loadFileName string, saveFileName string, run int, param Parameters) {
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

	file, err := os.OpenFile(saveFileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	check(err)
	defer file.Close()

	mean, variance := CalcMeanAndVar(d)

	fmt.Fprintf(file, "%v %f %f %f %f %f %f %d %d \n", run, mean, variance, param.InfectionSpeed, param.DeathSpeed, param.MutationSpeed, param.ImmunitySpeed, param.NAntigens, param.MaxAntigenValue)

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

func GetParametersAndStartTheThing(fileName string, settings ModelSettings) {
	r := LoadCSVFile(fileName)

	var header []string

	i := 0

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
			param := InsertParameters(header, records)
			RunModelWithSaving(param, settings)
			// Insert running the whole fucking thing here. It is a bit contrivied putting it here, I know (as it is harder to test), but I can't find a better way to do it than putting it in the middle of the for loop.
		}
	}
}

// InsertParameters : Insert parameters into the parameters struct given a string slice.
func InsertParameters(header []string, records []string) Parameters {
	var param Parameters
	for {
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
			}
		}
	}
	return param
}

// InsertSettings : Inserts the settings in a setting struct. It does so dynamically to the name in the header. If the name in the header does not correspond to the name in the struct, it will return an error message
func (setting ModelSettings) InsertSettings(fileName string) ModelSettings {

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
				}
			}
		}

		i++
	}

	return setting

}
