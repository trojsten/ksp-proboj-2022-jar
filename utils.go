package main

func GCD(a, b int) int {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

func LCM(integers ...int) int {
	if len(integers) == 1 {
		return integers[0]
	}
	if len(integers) == 0 {
		return 1
	}

	a := integers[0]
	b := integers[1]
	result := a * b / GCD(a, b)

	for i := 2; i < len(integers); i++ {
		result = LCM(result, integers[i])
	}

	return result
}
