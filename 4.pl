#!/usr/bin/env perl

@lines = `cat inputs/4`;
chomp @lines;

$part1 = 0, $part2 = 0, $card = 0;
%cards = {};

foreach $line (@lines) {
    @fields = split(/[:|]\s+/, $line);
    @winners = split(/\s+/, $fields[1]);
    @values = split(/\s+/, $fields[2]);
    $sum = 0;
    
    $fields[0] =~ /Card\s+(\d+)/;
    $card = $1;

    foreach $winner (@winners) {
        foreach $value (@values) {
            if($winner == $value) {
                $sum++;
            }
        }
    }
    if($sum > 0) {
        $part1 += 2 ** ($sum - 1);
    }
    $cards{$card} = $sum;
}
print("Part 1: $part1\n");

@tot = (0, (1) x $card);
for($i = 1; $i <= $card; $i++) {
    $part2 += $tot[$i];
    for($j = 1; $j <= $cards{$i}; $j++) {
        $tot[$i + $j] += $tot[$i];
    }
}
print("Part 2: " . $part2 . "\n");
