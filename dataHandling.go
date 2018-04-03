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

// LoadParametersAndSettings :
func LoadParametersAndSettings(fileName string) (Reader, Reader) {
	parameterFileName := "parameters/" + fileName + ".csv"
	settingFileName := "parameters/" + fileName + ".csv"

	parameterFile, err := ioutil.ReadFile(parameterFileName)
	if err != nil {
		log.Fatal(err)
	}
	settingFile, err := ioutil.ReadFile(parameterFileName)
	if err != nil {
		log.Fatal(err)
	}

	r := csv.NewReader(strings.NewReader(string(parameterFile)))

	for {
		record, err := r.Read()
		if err == io.EOF {
			break
		}

		if err != nil {
			log.Fatal(err)
		}

		fmt.Println(reflect.TypeOf(record[0]))
	}
	return nil, r
}

func insertParameters() {

}
