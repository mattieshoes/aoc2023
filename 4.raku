#!/usr/bin/raku

my @lines = "inputs/4".IO.lines;

my $part1 = 0;
my %sums;
for @lines -> $line {
    my @fields = split((':', '|'), $line);

    my ($card) := @fields[0] ~~ /(\d+)/;
    my @winners = split(/\s+/, @fields[1].trim);
    my @values = split(/\s+/, @fields[2].trim);
   
    my $sum = 0;
    for @winners -> $w {
        for @values -> $v {
            $sum++ if $w == $v;
        }
    }
    $part1 += 2 ** ($sum - 1) if $sum > 0;
    %sums{$card} = $sum;
}
say "Part 1: $part1";

my $part2 = 0;
my @cards = 1 xx (@lines.elems);
loop (my $i = 0; $i < @cards.elems; $i++) {
    $part2 += @cards[$i];
    loop (my $j = 1; $j <= %sums{$i}; $j++) {
       @cards[$i + $j] += @cards[$i];
    }
}
say "Part 2: $part2"
