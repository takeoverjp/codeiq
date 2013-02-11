package comb

type combination [2]int

func (value combination) Index(set []string, ret *[]string) {
	*ret = []string{
		set[value[0]],
		set[value[1]],
	}
}

func CombinationGenerator(length int, num int) map[combination]bool {
	ret := map[combination]bool{}

	for i := 0; i < length; i++ {
		for j := i+1; j < length; j++ {
			ret[[2]int{i,j}] = true
		}
	}

	return ret
}
