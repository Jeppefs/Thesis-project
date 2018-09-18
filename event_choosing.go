package main

import "math/rand"

// EventHappens : Choose and event and make it happen.
func (m *Malaria) EventHappens(param Parameters) {
	event := ChooseEvent(m, param)
	switch event {
	case 0:
		transmitter, _, _ := m.GetRandomInfectedHost()
		_, strainIndex := transmitter.GetRandomStrainIndex()
		m.Spread(rand.Intn(m.NHosts), strainIndex, param.MaxSuperInfections)
	case 1:
		m.ImmunityGained(rand.Intn(m.NInfectedHosts))
	case 2:
		m.Replace(rand.Intn(m.NHosts))
	case 3:
		_, hostIndex, _ := m.GetRandomInfectedHost()
		m.MutateParasite(hostIndex)
	}

	return
}

// ChooseEvent : Choose which event should happen with probability proportional to the rates.
func ChooseEvent(m *Malaria, param Parameters) int {

	rates := CalcRates(m, param)
	ratesTotal := SumSlice(rates)

	choice := rand.Float64()
	rProb := 0.0
	var event int
	for i := 0; i < 4; i++ {
		rProb += rates[i] / ratesTotal
		if choice < rProb {
			event = i
			break
		}
	}

	return event
}

// CalcRates : Calculates all the rates.
func CalcRates(m *Malaria, param Parameters) []float64 {
	r := make([]float64, 4)
	r[0] = param.InfectionSpeed * float64(m.NInfectedHosts)
	r[1] = param.ImmunitySpeed * float64(m.NInfectedHosts)
	r[2] = param.ReplacementSpeed * float64(m.NHosts)
	r[3] = param.MutationSpeed * float64(m.NInfectedHosts)
	return r
}
