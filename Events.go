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

// InfectHost : Applies the strainIndex to the given host.
func (h *Host) InfectHost(strainIndex int) {
	h.NInfections++
	h.Infections = append(h.Infections, strainIndex)
	return
}

// ImmunityGained : An infected person get immunity from one strain. If that one already exist, the parasite dies.
func (m *Malaria) ImmunityGained(infectedHostIndex int) {

	hostIndex := m.InfectedHosts[infectedHostIndex]
	host := &m.Hosts[hostIndex]
	infectionIndexInHost, strainIndex := host.GetRandomStrainIndex()

	// Check if the host does not have every antibody for that strain. If the host doesn't, gain antibody and return.
	for _, antigenTarget := range m.Strains[strainIndex] {
		if host.Antibodies[antigenTarget-1] == false {
			host.Antibodies[antigenTarget-1] = true
			return
		}
	}

	// As the host has all antibodies, the host gets rid of the disease.
	host.Infections = append(host.Infections[:infectionIndexInHost], host.Infections[infectionIndexInHost+1:]...)
	host.NInfections--

	// Change the systems counts.
	m.InfectionCounter[host.NInfections]++
	m.InfectionCounter[host.NInfections+1]--
	m.StrainCounter[strainIndex]--
	if host.NInfections == 0 {
		m.NInfectedHosts--
		m.InfectedHosts = append(m.InfectedHosts[:infectedHostIndex], m.InfectedHosts[infectedHostIndex+1:]...)
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
