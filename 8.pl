#!/usr/bin/perl

sub cycle {
    my $loc = shift;
    my $count = 0;
    while(1) {
        foreach $dir (@directions) {
            if($dir eq "L") {
                $loc = $left{$loc};
            } else {
                $loc = $right{$loc};
            }
            $count++;
            return $count if($loc =~ /..Z/);
        }
    }
}

sub lcm {
	use integer;
	my ($x, $y) = @_;
	my ($f, $s) = @_;
	while ($f != $s) {
		($f, $s, $x, $y) = ($s, $f, $y, $x) if $f > $s;
		$f = $s / $x * $x;
		$f += $x if $f < $s;
	}
	$f
}

my @lines = `cat inputs/8`;
chomp @lines;
@directions = split(//, shift @lines);
shift @lines;
%left = %right = ();
foreach (@lines) {
    /^(...) = \((...), (...)\)$/;
    $left{$1} = $2;
    $right{$1} = $3;
}

my $part1 = &cycle("AAA");
print "Part 1: $part1\n";

my $part2 = $part1;
foreach my $loc (keys %left) {
    $part2 = &lcm($part2, &cycle($loc)) if($loc =~ /..A/);
}
print("Part 2: $part2\n");
