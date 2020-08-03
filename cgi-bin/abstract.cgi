#!/usr/bin/perl
# Code modified by Andrew Lamont (2018) -- added SULA database

# Takes one parameter: the abstract name.

print "Content-type:text/html\n\n";



@params = split(/%/,$ENV{'QUERY_STRING'});


# Get abstract file corresponding to the id of the publication

open(INF, "abstracts/$params[0].TXT");
@abstract = <INF>;
close(INF);


# Find title corresponding to the id of publication by stepping through the database

$title = "";

# Open all the databases

open(INF, "database/DISS.TXT");
@db_diss = <INF>;
close(INF);
@db_diss = sort(@db_diss);
	
open(INF, "database/UMOP.TXT");
@db_umop = <INF>;
close(INF);
@db_umop = sort(@db_umop);

open(INF, "database/NELS.TXT");
@db_nels = <INF>;
close(INF);
@db_nels = sort(@db_nels);

open(INF, "database/SULA.TXT");
@db_sula = <INF>;
close(INF);
@db_sula = sort(@db_sula);

open(INF, "database/OTHER.TXT");
@db_other = <INF>;
close(INF);
@db_other = sort(@db_other);

# now concatenate all the databases:

@db = @db_diss;
push(@db, @db_umop);
push(@db, @db_nels);
push(@db, @db_sula);
push(@db, @db_other);

@db_glsa = sort(@db);

foreach $line (@db_glsa)
	{
	@dbs = split(/%/, $line);

	if ($params[0] eq $dbs[0])
		{
		$title = "$dbs[2]";
		}
	}


print <<EndOfHTML;
<html>

<head>
<title>GLSA Abstract</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">

<!-- CSS style sheet -->
<link href="../glsa.css" rel="stylesheet" type="text/css">

<style type="text/css">
<!--

body {
	background-color: #FFFFFF;
	background-image: url(images/bg2.jpg);
}
	
-->
</style>

</head>


<body>

<table width="600" height="100%" border="0" cellspacing="0" cellpadding="0">
    <tr>
      <td valign="top">
	<table width="600" border="0" cellspacing="0" cellpadding="0">
    	  <tr>
	    <td width="600" height="30" align="center" bgcolor="#0B5992" class="Title">GLSA ABSTRACT</td>
    	  </tr>
   	  <tr>
      	    <td height="30">&nbsp;</td>
    	  </tr>
 	  <tr>
	    <td>
	      <blockquote>
EndOfHTML

print "<div class=\"abTitle\">$title</div>";

foreach $line (@abstract)
	{
	# clean-up line: remove leading and trailing spaces from line
	$line =~ s/^\s+//;
	$line =~ s/\s+$//;

	# clean-up line: remove leading and trailing spaces from title
	$title =~ s/^\s+//;
	$title =~ s/\s+$//;

	# lowercase dummy alias for line
	$cline = $line;
	$cline =~ tr/A-Z/a-z/;

	# lowercase dummy alias for title
	$ctitle = $title;
	$ctitle =~ tr/A-Z/a-z/;

	# compare line to _abstract_ and _title_: print only different
	if ($cline ne "abstract" && $cline ne $ctitle)
		{
		print "<br>$line";
		}
	}

print <<EndOfHTML;
	</blockquote>
      </td>
    </tr>
  </table>
</td>
</tr>
<tr>
  <td valign="bottom">
    <table width="600" height="20" border="0" cellpadding="0" cellspacing="0">
	<tr>
		<td width="100%" height="20" bgcolor="#C9CCED" align="center">
			<a href="#" onClick="window.close();">Close</a>
		</td>
  	</tr>
    </table>
  </td>
</tr>
</table>

</body>
</html>
EndOfHTML



