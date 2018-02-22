import (
	"fmt"
	"math/rand"
)

func TestSpread() {

}

func CreateDummyMalariaStruct() {
	var m Malaria

	// Sets initial values.
	m.NHosts = 10 // Constant
	m.NInfectedHosts = 2
	m.NAntigens = 3

	m.MaxAntigenValue = 5

	// Make initial antigens

	m.Antigens = make([][]int8, m.NHosts)
	for host := 0; host < m.NHosts; host++ {
		m.Antigens[host] = make([]int8, m.NAntigens)
		for antigen := 0; antigen < m.NAntigens; antigen++ {
			if host < m.NInfectedHosts {
				m.Antigens[host][antigen] = int8(rand.Intn(m.MaxAntigenValue))
			} else {
				m.Antigens[host][antigen]--
			}
		}
	}

	// Make initial infections
	m.Infections = make([][]int8, m.NHosts)
	for host := 0; host < m.NHosts; host++ {
		m.Infections[host] = make([]int8, m.NAntigens)
		for antigen := 0; antigen < m.NAntigens; antigen++ {
			if host < m.NInfectedHosts {
				m.Infections[host][antigen] = m.Antigens[host][antigen]
			} else {
				m.Infections[host][antigen]--
			}
		}
	}
	// Make initial immunities
	m.Antibodies = make([][]bool, m.NHosts)
	for host := 0; host < m.NHosts; host++ {
		m.Antibodies[host] = make([]bool, m.MaxAntigenValue)
	}

	m.InfectedHosts = make([]int, m.NInfectedHosts)
	for host := 0; host < m.NInfectedHosts; host++ {
		m.InfectedHosts[host] = host
	}

	fmt.Println(m.Antigens, "\n", m.Infections, "\n", m.Antibodies, "\n")
	return m

}