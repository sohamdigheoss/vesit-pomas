open $fh,'<',$ARGV[0];
open $fw,'>',$ARGV[1];
$tag = $ARGV[2];
$attr = $ARGV[3];
while ($line=<$fh>) {
	if ($line =~ m/<$tag $attr="([a-zA-Z\.].*?)"/) {
		$line =~ s/<$tag $attr="(.*?)"/<$tag $attr="{% static '$1' %}"/;
	}
	print $fw $line;
}
close $fh;
close $fw;
