@array = (
"Engineering Concepts & Knowledge",
"Interpretation of Problem & Analysis",
"Design/Prototype",
"Interpretation of Data & Dataset",
"Modern Tool Usage",
"Social Benefit, Safety Consideration ",
"Environment friendly",
"Ethics",
"Team work",
"Presentation skills",
"Applied Engg & Mgmt principles",
"Life long learning",
"Professional skills",
"Innovative approach"
);
$rubric = 1;
open($fw,'>','test1.html');
foreach $e (@array) {
	$line = "<p>$e: {{review.rubric$rubric}}</p>\n";
	print $fw $line;
	$rubric++;
}
