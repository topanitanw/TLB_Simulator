#!/usr/bin/perl

# Change to /bin/perl on paul.

use strict;

my $NUM_PROCESSES = 1;
my $AVG_NUM_ACCESSES_PER_CONTEXT_SWITCH = 1000;
my $AVG_FOOTPRINT = 500;
my $MAX_TRACE_LENGTH = 200;
my $ALPHA = 0.6;
my $READ_DOMINANCE = 3; # 4-1 reads to writes.

my $proc;
my $num_accesses = 0;

die "footprint can't be bigger than 4gb\n" if (($AVG_FOOTPRINT/2)>4096*1024*1024);

sub random
{
    my ($min, $max) = @_;
    return int( rand( $max-$min+1 ) ) + $min;
}

sub pareto 
{
    my ($b, $alpha) = @_;
    return ($b/((1.0-rand(1.0))**(1.0/$alpha)));
}

my %footprint = (); #random(0, 2*$AVG_FOOTPRINT);
my %num_pages = ();
my %num_accesses = ();

my $last_proc = 0;
while(1)
{
    my $proc_id;
    my $page_id;
    my $rw;
    my $acc;
    my $i;
    my $addr;
    # choose process

    $proc_id = random(0, $NUM_PROCESSES);
    $acc=random(0, 2*$AVG_NUM_ACCESSES_PER_CONTEXT_SWITCH);
    for ($i=0; $i<$acc; $i++)
    {
        if (!exists $footprint{$proc_id})
        {
            $footprint{$proc_id} = random(1, 2*$AVG_FOOTPRINT);
            $num_pages{$proc_id} = 0;
        }
        
        $page_id = int(pareto(1.0, $ALPHA));
        next if ($page_id > $footprint{$proc_id});
        $addr = $page_id*4096 + random(0, 4095);
        $addr &= 0xFFFFFFFC; # word aligned.
        $rw = random(0, $READ_DOMINANCE);
        if ($rw>0)
        {
            $rw = "R"
        }
        else
        {
            $rw = "W";
        }
        print("$proc_id, $rw, ");
        # print("($page_id) ");
        printf("0x%08lx\n", $addr);
        $num_accesses++;
        exit if ($num_accesses >= $MAX_TRACE_LENGTH);
    }
}

