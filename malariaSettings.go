package main

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

// ModelSettings : A structure that contains information about model settings such as
type ModelSettings struct {
	BurnIn int
	Runs   int

	Test                    bool
	AppendToCurrentDataFile bool

	MultipleInfections bool

	CurrentDataFile string
}

// MakeModelSetting : Constructs the ModelSettings struct, which sets how the data should be saved, if a burnin should exist and so on.
func MakeModelSetting() ModelSettings {

	var setting ModelSettings

	setting.Runs = 5000000   // Usually 5000000
	setting.BurnIn = 5000000 // Usually 5000000

	setting.Test = true
	setting.AppendToCurrentDataFile = true

	setting.MultipleInfections = true

	setting.CurrentDataFile = "data/avgFile7.txt"

	return setting
}

// MakeParameterGrid : Creates a parameter grid to search through. Also where settings as applied.
func MakeParameterGrid() []Parameters {
	gridsize := 100

	parameterGrid := make([]Parameters, gridsize)

	for i := 0; i < gridsize; i++ {
		parameterGrid[i].InfectionSpeed = 0.95 + float64(i)/1000.0
		parameterGrid[i].ImmunitySpeed = 1.0
		parameterGrid[i].MutationSpeed = 0.0
		parameterGrid[i].DeathSpeed = 0.01

		parameterGrid[i].NHosts = 10000
		parameterGrid[i].NAntigens = 1
		parameterGrid[i].MaxAntigenValue = 1
	}

	return parameterGrid
}
