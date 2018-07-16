package main

import (
	"fmt"
	"math/rand"
)

// Spread : Another person gets infected.
func (m *Malaria) Spread() {

	spreadTo, spreadFrom := m.GetSpreadToAndSpreadFrom()

	// If spread to is equal to spread from, do not spread.
	if spreadTo == spreadFrom {
		return
	}

	// If the host already is infected by the same strain, then don't infect.
	if m.Hosts[spreadTo].IsInfected {
		if m.Hosts[spreadTo].HasStrain(&m.Hosts[spreadFrom], m.NAntigens) == true {
			return
		}
		m.Hosts[spreadTo].InfectHost(&m.Hosts[spreadFrom], m.NAntigens)
	} else {
		// If the target is not currently infected put him on the infected list, add to the number of incfected and append the disease to him.
		m.NInfectedHosts++
		m.InfectedHosts = append(m.InfectedHosts, spreadTo)
		m.Hosts[spreadTo].IsInfected = true
		m.Hosts[spreadTo].InfectHost(&m.Hosts[spreadFrom], m.NAntigens)
	}

	return
}

// GetSpreadToAndSpreadFrom : Finds a host to spread to and the antigens which malaria is spread from.
func (m *Malaria) GetSpreadToAndSpreadFrom() (int, int) {
	spreadTo := rand.Intn(m.NHosts)
	spreadFrom := m.InfectedHosts[rand.Intn(m.NInfectedHosts)]
	return spreadTo, spreadFrom
}

// InfectHost :
func (h *Host) InfectHost(fromHost *Host, NAntigens int) {
	// Check if the person spreading to has any infections. If false make him sick. If true append the parasite.
	if h.IsInfected {
		for antigen := 0; antigen < NAntigens; antigen++ {
			h.Infections = append(h.Infections, fromHost.ExpressedStrain[antigen])
		}
		//h.CombineParasites(NAntigens)
	} else {
		for antigen := 0; antigen < NAntigens; antigen++ {
			h.Infections = append(h.Infections, fromHost.ExpressedStrain[antigen])
			h.ExpressedStrain[antigen] = fromHost.ExpressedStrain[antigen]
		}
	}
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
func (m *Malaria) ImmunityGained() {
	infectedHostIndex := rand.Intn(m.NInfectedHosts)
	infectedHost := m.InfectedHosts[infectedHostIndex]

	// Checking error stuff...
	if m.Hosts[infectedHost].IsInfected == false {
		for i := 0; i < m.NInfectedHosts; i++ {
			if m.Hosts[m.InfectedHosts[i]].IsInfected == false {
				fmt.Println("yup")
			}
		}
	}

	m.Hosts[infectedHost].GiveHostAntibody(m.NAntigens)

	if m.Hosts[infectedHost].IsInfected == false {
		m.NInfectedHosts--
		m.InfectedHosts = append(m.InfectedHosts[:infectedHostIndex], m.InfectedHosts[infectedHostIndex+1:]...)
	}

	return
}

// GiveHostAntibody : Gives the host an antibody for its current lookout in the antigens. Also send to RemoveParaiste method if removal should happen
func (h *Host) GiveHostAntibody(NAntigens int) {

	if h.Lookout > NAntigens-1 { //-1 because NAntigens is one larger than lookout because of 0 indexing
		h.RemoveParasite(NAntigens)
	} else if h.Antibodies[h.Infections[h.Lookout]] {
		h.RemoveParasite(NAntigens)
	} else {
		// If at end, make him healthy
		// Make immunity in the hosts antibody and set the lookout one up
		h.Antibodies[h.Infections[h.Lookout]] = true
		h.Lookout++
	}
	return
}

// RemoveParasite :  Removes a parasite from a host after immunization
func (h *Host) RemoveParasite(NAntigens int) {
	h.Infections = append(h.Infections[:0], h.Infections[NAntigens:]...)
	if len(h.Infections) == 0 { // If the last parasite of the host dies, then that host is not infected anymore.
		h.IsInfected = false
	}
	h.Lookout = 0
	return
}

// Death : Kills a host removing it from the system and adding a new one.
func (m *Malaria) Death() {
	//host, hostIndex := m.GetRandomInfectedHost()

	hostIndex := rand.Intn(m.NHosts)

	if m.Hosts[hostIndex].IsInfected == true {
		m.NInfectedHosts--
		for i := 0; i < m.NInfectedHosts; i++ {
			if hostIndex == m.InfectedHosts[i] {
				m.InfectedHosts = append(m.InfectedHosts[:i], m.InfectedHosts[i+1:]...)
			}
		}
		//m.InfectedHosts = append(m.InfectedHosts[:hostIndex], m.InfectedHosts[hostIndex+1:]...)
	}

	m.Hosts[hostIndex].Die(m.NAntigens, m.MaxAntigenValue)
	return
}

// Die : A host dies
func (h *Host) Die(NAntigens int, MaxAntigenValue int) {
	if h.IsInfected == true {
		h.Infections = append(h.Infections[:0], h.Infections[len(h.Infections):]...)
		h.IsInfected = false
	}
	h.Lookout = 0

	for antibody := 0; antibody < MaxAntigenValue; antibody++ {
		h.Antibodies[antibody] = false
	}

}

// MutateParasite : Changes a single antigen in a host to a new random one.
func (m *Malaria) MutateParasite(host int) {
	randomAntigen := rand.Intn(m.NAntigens)
	m.Hosts[host].ExpressedStrain[randomAntigen] = int8(rand.Intn(m.MaxAntigenValue))
	return
}

// GetRandomInfectedHost :
func (m *Malaria) GetRandomInfectedHost() (int, int) {
	infectedHostIndex := rand.Intn(m.NInfectedHosts)
	host := m.InfectedHosts[infectedHostIndex]
	return host, infectedHostIndex
}
