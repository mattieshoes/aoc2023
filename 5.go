package main

import (
    "fmt"
    "time"
    "os"
    "strings"
    "strconv"
    "math"
)

// turns a slice of strings into a slice of ints, with error handling (non-int -> 0)
func Intify(s []string) []int64 {
    result := make([]int64, len(s))
    for i, v := range s {
        value, err := strconv.ParseInt(v, 10, 64)
        if err != nil {
            result[i] = 0
        } else {
            result[i] = value
        }
    }
    return result
}

func main() {
    start := time.Now()

    var part1 int64 = 0
    // pull input
    raw, _ := os.ReadFile("inputs/5")
    input := strings.TrimSpace(string(raw))

    // seed extraction
    parsed := strings.Split(input, "\n\n")
    seeds := Intify(strings.Split(parsed[0], " ")[1:])
    parsed = parsed[1:]

    // mapping extraction
    mapping := make([][][]int64, 0)
    for i, m := range parsed {
        mapping = append(mapping, make([][]int64, 0))
        lines := strings.Split(m, "\n")[1:]
        for j, r := range lines {
            mapping[i] = append(mapping[i], make([]int64, 0))
            fields := Intify(strings.Split(r, " "))
            // convert dest, source, range to start, end, shift amount
            fields[0], fields[1], fields[2] = fields[1], 
                                              fields[1] + fields[2], 
                                              fields[0] - fields[1]
            mapping[i][j] = fields
        }
    }

    // Part 1 -- just map all the seeds through to locations
    part1 = math.MaxInt64
    for _, val := range seeds {
        for _, m := range mapping {
            for _, r := range m {
                if val >= r[0] && val < r[1] {
                    val += r[2]
                    break;
                }
            }
        }
        if val < part1 {
            part1 = val
        }
    }
    fmt.Println("Part 1: ", part1)
    duration := time.Since(start)
    fmt.Println(duration)
    
    start = time.Now()

    // convert seeds to intervals
    intervals := make([][]int64, 0)
    for i := 0; i < len(seeds); i += 2 {
        intervals = append(intervals, []int64{seeds[i], seeds[i]+seeds[i + 1]})
    }

    // iterate through maps
    for _, m := range mapping {
        //fmt.Println(intervals)
        //fmt.Println("Mapping ", a, m)
        // iterate through rules, splitting on rule-start intersections
        for _, r := range m {
            //fmt.Println("\tRule ", b, r)
            for i := 0; i < len(intervals); i++ {
                //fmt.Println("\t\tRule start", r[0], "Interval", intervals[i])
                if r[0] > intervals[i][0] && r[0] < intervals[i][1] {
                        //fmt.Print("\t\t\tSplit on start ")
                        intervals = append(intervals, []int64{r[0], intervals[i][1]})
                        intervals[i][1] = r[0]
                        //fmt.Println(intervals[i], intervals[len(intervals) - 1])
                }
            }
        }
        // iterate through rules a second time splitting on rule-end intersections
        for _, r := range m {
            //fmt.Println("\tRule ", b, r)
            for i := 0; i < len(intervals); i++ {
                //fmt.Println("\t\tRule end", r[1], "Interval", intervals[i])
                if r[1] > intervals[i][0] && r[1] < intervals[i][1] {
                        //fmt.Print("\t\t\tSplit on end ")
                        intervals = append(intervals, []int64{r[1], intervals[i][1]})
                        intervals[i][1] = r[1]
                        //fmt.Println(intervals[i], intervals[len(intervals) - 1])
                }
            }
        }
        // iterate through intervals (which now don't intersect), applying mappings
        //fmt.Println(intervals)
        for i := 0; i < len(intervals); i++ {
            // apply any relevant mappings
            for _, r := range m {
                if intervals[i][0] >= r[0] && intervals[i][0] < r[1] {
                    //fmt.Print("\t", intervals[i])
                    intervals[i][0] += r[2]
                    intervals[i][1] += r[2]
                    //fmt.Println(" ->", intervals[i], "based on rule", r)
                    break
                }
            }
        }
        // theoretically stitch together intervals at this point, but eff that
    }
    //fmt.Println(intervals)
    var part2 int64 = math.MaxInt64
    for _, x := range(intervals) {
        if x[0] < part2 {
            part2 = x[0]
        }
    }
    fmt.Println("Part 2: ", part2)

    duration = time.Since(start)
    fmt.Println(duration)
}
