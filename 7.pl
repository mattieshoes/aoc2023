#!/usr/bin/perl

%cardValue = ('2', 0, '3', 1, '4', 2, '5', 3, '6', 4, '7', 5, '8', 6, '9', 7, 'T', 8, 'J', 9, 'Q', 10, 'K', 11, 'A', 12);

sub sortHand($) {
    my $hand = shift;
    my @hand = sort split(//, $hand);
    return join("", @hand);
}

sub scoreHand($) {
    my $hand = shift;
    my $newHand = $hand;
    my $joker;
    if($#_ != -1) {
        $joker = shift;
        $newHand =~ s/J/$joker/g;
    }
    my $sorted = &sortHand($newHand);
    my $score;

    if($sorted =~ /(.)\1{4}/) { # five of a kind
        $score = 7;
    } elsif($sorted =~ /(.)\1{3}/) { # four of a kind
        $score = 6;
    } elsif($sorted =~ /(.)\1{2}(.)\2/ or $sorted =~ /(.)\1(.)\2{2}/) { # full house
        $score = 5;
    } elsif($sorted =~ /(.)\1{2}/) { #three of kind
        $score = 4;
    } elsif($sorted =~ /(.)\1(.)\2/ or $sorted =~ /(.)\1.(.)\2/) { # two pair
        $score = 3;
    } elsif($sorted =~ /(.)\1/) { # pair
        $score = 2;
    } else { # high card
        $score = 1;
    }

    my @cards = split(//, $hand);
    foreach my $card (@cards) {
        $score = $score * 14 + $cardValue{$card};
    }
    return $score;
}

sub part2ScoreHand($) {
    my $hand = shift;
    if($hand =~ /[^J]{5}/) {
        return &scoreHand($hand);
    }
    my $max = 0;
    foreach my $jokerValue (@jokerValues) {
        my $score = &scoreHand($hand, $jokerValue);
        if($score > $max) {
            $max = $score;
        }
    }
    return $max;
}

my @lines = `cat inputs/7`;
chomp @lines;

my %hands = ();
foreach my $line (@lines) {
    my ($hand, $bet) = split(/ /, $line);
    $hands{$hand} = $bet;
}

$part1 = 0;
my @sorted = sort {&scoreHand($a) <=> &scoreHand($b)} keys %hands;
for(my $rank = 0; $rank <= $#sorted; $rank++) {
    $part1 += ($rank + 1) * $hands{$sorted[$rank]};
}
print("Part 1: $part1\n");

$part2 = 0;
%cardValue = ('2', 1, '3', 2, '4', 3, '5', 4, '6', 5, '7', 6, '8', 7, '9', 8, 'T', 9, 'J', 0, 'Q', 10, 'K', 11,  'A', 12);
@jokerValues = qw(2 3 4 5 6 7 8 9 T Q K A);
@sorted = sort {&part2ScoreHand($a) <=> &part2ScoreHand($b)} keys %hands;
for(my $rank = 0; $rank <= $#sorted; $rank++) {
    $part2 += ($rank + 1) * $hands{$sorted[$rank]};
}
print("Part 2: $part2\n");
