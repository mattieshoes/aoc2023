#!/usr/bin/perl

sub calc($$) {
    my $time = shift;
    my $distance = shift;
    my $sum = 0;
    for(my $hold = 0; $hold < $time; $hold++) {
        $sum++ if(($time - $hold) * $hold > $distance );
    }
    return $sum;
}

my @lines = `cat inputs/6`;
chomp @lines;
my @times = split(/\s+/, $lines[0]);
my @distances = split(/\s+/, $lines[1]);
shift @times;
shift @distances;

$part1 = 1;
for($race = 0; $race <= $#times; $race++) {
    $part1 *= &calc($times[$race], $distances[$race]);
}
print("Part 1: $part1\n");

$part2 = &calc(join("", @times), join("", @distances));
print("Part 2: $part2\n");
