package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"reflect"
	"strconv"
)

// SaveToEndFile :  Saves data in the test file
func SaveToEndFile(loadFileName string, saveFileName string, run int, param Parameters) {
	data, err := ioutil.ReadFile(loadFileName)
	check(err)

	fmt.Println(data, reflect.TypeOf(data))

	stringData := string(data)

	/*
		file, err := os.Create(saveFileName)
		check(err)
		defer file.Close()
	*/

	var s string
	var d []float64
	var q int

	for _, k := range stringData {
		s = string(k)
		if (s != "\n") && (s != " ") && (s != "\t") && (k != 13) {
			q, _ = strconv.Atoi(s)
			d = append(d, float64(q))
		}
	}

	file, err := os.OpenFile(saveFileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	check(err)
	defer file.Close()

	mean, variance := CalcMeanAndVar(d)

	fmt.Println(mean)
	fmt.Fprintf(file, "%v %f %f %f %f %f \n", run, mean, variance, param.InfectionSpeed, param.DeathSpeed, param.ImmunitySpeed)

	return
}
