#!/usr/bin/perl

@lines = `cat inputs/5`;
chomp @lines;

$fl = shift(@lines);
shift(@lines);

@seeds = split(/ /, $fl);
shift @seeds;

$parse = 0;
$type = "";
$min = 999999999999;
$minseed = 0;

foreach $seed (@seeds) {
    $val = $seed; 
    foreach $line (@lines) {
        if($line =~ /map:/) {
            $parse = 1;
        } elsif($line =~ /^$/) {
            $parse = 0;
        } elsif($parse) {
            ($destStart, $sourceStart, $range) = split(/ /, $line);
            if($val >= $sourceStart and $val < $sourceStart + $range) {
                $val = $val - $sourceStart + $destStart;
                $parse = 0;
            }
        }
    }
    if($val < $min) {
        $min = $val;
    }
}
print("Part 1: $min\n");


@rev = reverse @lines;
sub revParse($$) {
    my $start = shift;
    my $jump = shift;
    for($loc = $start; ; $loc += $jump) {
        $val = $loc;
        $parse = 1;
        foreach $line (@rev) {
            if($line =~ /map:/) {
                $parse = 0;
            } elsif($line =~ /^$/) {
                $parse = 1;
            } elsif($parse) {
                ($destStart, $sourceStart, $range) = split(/ /, $line);
                if($val >= $destStart and $val < $destStart + $range) {
                    $val = $val - $destStart + $sourceStart;
                    $parse = 0;
                }
            }
        }
        for($i = 0; $i <= $#seeds; $i += 2) {
            if($val >= $seeds[$i] and $val < $seeds[$i]+$seeds[$i+1]) {
                return $loc;
            }
        }
    }
}

$ret = &revParse(0, 1e6);
$ret = &revParse($ret-1e6, 1000);
$ret = &revParse($ret-1e3, 1);

print("Part 2: $ret\n");
