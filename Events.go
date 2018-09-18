package main

import (
	"math/rand"
)

// Spread : Another person gets infected.
func (m *Malaria) Spread(recieverHostIndex int, strainIndex int, maxSuperInfections int) {

	// If the host can't contain more strain, do nothing.
	if m.Hosts[recieverHostIndex].NInfections >= maxSuperInfections {
		return
	}

	if m.Hosts[recieverHostIndex].NInfections != 0 {
		// Checks if the new host already has the strain in question. This also makes sure that a host cannot infect itself.
		if m.Hosts[recieverHostIndex].HasStrain(strainIndex) == true {
			return
		}
		m.Hosts[recieverHostIndex].InfectHost(strainIndex)
	} else {
		// If the target is not currently infected put him on the infected list, add to the number of incfected and append the disease to him.
		m.NInfectedHosts++
		m.InfectedHosts = append(m.InfectedHosts, recieverHostIndex)
		m.Hosts[recieverHostIndex].InfectHost(strainIndex)
	}

	// Change the counters accordingly.
	m.StrainCounter[strainIndex]++
	m.InfectionCounter[m.Hosts[recieverHostIndex].NInfections-1]--
	m.InfectionCounter[m.Hosts[recieverHostIndex].NInfections]++

	return
}

// GetSpreadToAndSpreadFrom : Finds a host to spread to and the antigens which malaria is spread from.
func (m *Malaria) GetSpreadToAndSpreadFrom() (int, int) {
	spreadTo := rand.Intn(m.NHosts)
	spreadFrom := m.InfectedHosts[rand.Intn(m.NInfectedHosts)]
	return spreadTo, spreadFrom
}

func (h *Host) InfectHost(strainIndex) {
	h.NInfections++
	h.Infections = append(h.Infections, strainIndex)
	return
}

// CombineParasites : When a host becomes infected with another parasite (so it is inficted buy mulitple parasites), it has a combination
func (h *Host) CombineParasites(NAntigens int) {
	for antigen := 0; antigen < NAntigens; antigen++ {
		antigenOrNewParasiteChoice := rand.Float32()
		if antigenOrNewParasiteChoice > 0.5 { // Pick randomly new antigens in the infected host.
			h.ExpressedStrain[antigen] = h.Infections[rand.Intn(len(h.Infections))]
		}
	}
	return
}

// ImmunityGained : An infected person get immunity from one strain. If that one already exist, the parasite dies.
func (m *Malaria) ImmunityGained(infectedHostIndex int) {

	infectedHost := m.InfectedHosts[infectedHostIndex]

	nInfections := CountInfections(m.Hosts[infectedHost].Infections, m.NAntigens)
	strainTarget := rand.Intn(nInfections)
	antigenTarget := rand.Intn(m.NAntigens) + strainTarget*m.NAntigens
	m.Hosts[infectedHost].GiveHostAntibody(m.NAntigens, strainTarget, antigenTarget, &m.StrainCounter)

	if m.Hosts[infectedHost].IsInfected == false {
		m.NInfectedHosts--
		m.InfectedHosts = append(m.InfectedHosts[:infectedHostIndex], m.InfectedHosts[infectedHostIndex+1:]...)
	}

	return
}

// GiveHostAntibody : Gives the host an antibody for its current lookout in the antigens. Also send to RemoveParaiste method if removal should happen
func (h *Host) GiveHostAntibody(NAntigens int, strainTarget int, antigenTarget int, strainCounter *map[string]int) {

	if h.Antibodies[h.Infections[antigenTarget]-1] {
		(*strainCounter)[ListToString(h.Infections[strainTarget*NAntigens:NAntigens+strainTarget*NAntigens])]--
		h.RemoveParasite(NAntigens, strainTarget)
	} else {
		h.Antibodies[h.Infections[antigenTarget]-1] = true
	}
	return
}

// RemoveParasite :  Removes a parasite from a host after immunization
func (h *Host) RemoveParasite(NAntigens int, strainTarget int) {
	h.Infections = append(h.Infections[:0+strainTarget*NAntigens], h.Infections[strainTarget*NAntigens+NAntigens:]...)
	if len(h.Infections) == 0 { // If the last parasite of the host dies, then that host is not infected anymore.
		h.IsInfected = false
		for i := 0; i < NAntigens; i++ {
			h.ExpressedStrain[i] = 0
		}
	}
	return
}

// Replace : Kills a host removing it from the system and adding a new one.
func (m *Malaria) Replace(hostIndex int) {

	if m.Hosts[hostIndex].IsInfected == true {

		for i := 0; i < m.NInfectedHosts; i++ {
			if hostIndex == m.InfectedHosts[i] {
				m.InfectedHosts = append(m.InfectedHosts[:i], m.InfectedHosts[i+1:]...)
				break
			}
		}
		m.NInfectedHosts--
	}

	m.Hosts[hostIndex].Die(m.NAntigens, m.MaxAntigenValue, &m.StrainCounter)
	return
}

// Die : A host dies
func (h *Host) Die(NAntigens int, MaxAntigenValue int, strainCounter *map[string]int) {
	if h.IsInfected == true {
		nInfections := CountInfections(h.Infections, NAntigens)
		for i := 0; i < nInfections; i++ {
			(*strainCounter)[ListToString(h.Infections[i*NAntigens:NAntigens+i*NAntigens])]--
		}
		h.Infections = append(h.Infections[:0], h.Infections[len(h.Infections):]...)
		h.IsInfected = false
	}

	for antibody := 1; antibody < MaxAntigenValue+1; antibody++ {
		h.Antibodies[antibody-1] = false
	}
	return
}

// MutateParasite : Changes a single antigen in a host to a new random one.
func (m *Malaria) MutateParasite(host int) {
	randomAntigen := rand.Intn(m.NAntigens)
	m.Hosts[host].ExpressedStrain[randomAntigen] = int8(rand.Intn(m.MaxAntigenValue)) + 1
	return
}

// GetRandomInfectedHost :
func (m *Malaria) GetRandomInfectedHost() (Host, int, int) {
	infectedHostIndex := rand.Intn(m.NInfectedHosts)
	hostIndex := m.InfectedHosts[infectedHostIndex]
	host := m.Hosts[hostIndex]
	return host, hostIndex, infectedHostIndex
}
