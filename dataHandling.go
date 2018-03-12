package main

import (
	"fmt"
	"io/ioutil"
	"reflect"
)

// SaveToEndFile :  Saves data in the test file
func SaveToEndFile(loadFileName string, saveFileName string, run int, param Parameters) {
	data, err := ioutil.ReadFile(loadFileName)
	check(err)

	fmt.Println(data, reflect.TypeOf(data))

	stringData := string(data)

	fmt.Println(string(stringData[0]))

	for i, _ := range stringData {
		fmt.Print(i)
	}

}
