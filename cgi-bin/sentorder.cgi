#!/usr/bin/perl

# (c) 2001, Paul de Lacy.  Not for resale or public distribution.  Licensed to GLSA Publications Only.
# The original code has been modified by Youri Zabbal and by Wendell Kimper.  Modifications (c) 2004, 2007 GLSA Publications.
# Modified by Andrew Lamont (2019) -- added SULA database
# Andrew Lamont: formmail.cgi stopped working in 2019 -- I pushed the titles to Paypal so that it shows up in an email

# This script is called after an order is sent successfully.
# It takes one parameter: the amount spent.
# The aim is to say 1. thanks, 2. print this out as your receipt.
# and 3. clear the old order.

@params = split(/%/, $ENV{'QUERY_STRING'});

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

@db = sort(@db);

print "Content-type:text/html\n\n";

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday) = gmtime(time);
$year += 1900;
$mon += 1;


print <<EndOfHTML;
<html>
<head>
<META HTTP-EQUIV="Set-Cookie"; CONTENT="BOOKS=; domain=glsa.hypermart.net; expires=Monday, 10-Oct-10 10:10:10 GMT; path=">

<title>Your Order has been sent to GLSA!</title>

<!-- CSS style sheet -->
<link href="../glsa.css" rel="stylesheet" type="text/css">

<style>
<!--
body {background-color: #FFFFFF;}
-->
</style>



</head>

<body>


<table width="580" border="0" cellspacing="0" cellpadding="5" style="table-layout: fixed">
  <tr>
    <td width="570" align="center">
      Thank you for your order.<br>
      Please print this page as a record of your transaction.<br>
      <strong>Then click `Pay Online Securely' to pay for your order</strong</br>
      - GLSA.
    </td>
  </tr>
  <tr>
    <td width="569" height="10"><img src="../images/divider.gif" height="1" width="569"></td>
  </tr>
  <tr>
    <td width="570">
      <strong>GLSA Publications</strong><br>
      Department of Linguistics<br>
      650 North Pleasant Street<br>
      University of Massachusetts<br>
      Amherst, MA 01003-7130<br>
      U.S.A.<br>
      <br>
      glsa\@linguist.umass.edu
      <br>
    </td>
  </tr>
  <tr>
    <td width="570" height="40">Date: $mon/$mday/$year</td>
  </tr>
</table>


<table width="580" border="0" cellspacing="0" cellpadding="5" style="table-layout: fixed">
  <tr>
    <td width="90" height="20">Author/Editor</td>
    <td width="250" height="20">Title</td>
    <td width="35" height="20">Item</td>
    <td width="35" height="20" align="right">Price</td>
    <td width="50" height="20" align="right">Quantity</td>
    <td width="60" height="20" align="right"><strong>Total</strong></td>    
  </tr>
  <tr>
    <td colspan="6" width="569" height="10"><img src="../images/divider.gif" height="1" width="569"></td>
  </tr>
 

EndOfHTML

# First we need to split the pieces of the cookie
# Now that we have our part of the cooky (i.e. $cooky2), we can split it at the entry
# delimiter -- i.e. %
# So, our part of the cookie ends up looking like BOOK=BECK&CD&2%ALDE&BK&1% etc.


@cooky = @params;

$subtotal = 0;

# trying to pass titles to paypal
$titles = " "; 

foreach $items (@cooky)
	{

	if ($items =~ "&amp;") 
		{
		@item = split(/&amp;/, $items);
		}
		else
		{
		@item = split(/&/, $items);
		}
		
	$itemtotal = 0;

	foreach $line (@db)
		{
		#split each line into its components.
		@dbs = split(/%/, $line);

		# Does this record contain the START code? 

		if ($dbs[0] eq $item[0])
			{
			@author = split(/[$,&]/, $dbs[3]);
			if (scalar(@author) > 1)
				{
				$author[0] = "$author[0] et al.";
				}
			$title = $dbs[2];
                        # add title to titles
                        $titles .= $title ;
                        $titles .= " " ;
			$quantity = $item[2];
			if ($item[1] =~ 'BK')
				{
				$type = "Book";
				$price = $dbs[7];
				}
				else
				{
				$type = "CD";
				$price = $dbs[6];
				}		
			$itemtotal = $price * $quantity;
			# $itemtotal = sprintf "%.2f", $total;  #round the number to 2 decimal places.


# Now show the entry...
print <<EndOfHTML;
   <tr>
      <td width="90" align="left" valign="top">$author[0]</td>
      <td width="250" align="left" valign="top">$title</td>
      <td width="35" align="left" valign="top">$type</td>
      <td width="35" align="right" valign="top">$price</td>
      <td width="50" align="right" valign="top">$quantity</td>
      <td width="60" align="right" valign="top">$itemtotal</td>
    </tr>

EndOfHTML
			}
		}

	$subtotal = $subtotal + $itemtotal

	}

print <<EndOfHTML;
  <tr>
    <td colspan="6" width="569" height="10" align="right"><img src="../images/divider.gif" height="1" width="190"></td 
  </tr>
  <tr>
    <td colspan="5" width="510" height="30" align="right">Total:</td>
    <td width="60" height="20" align="right">\$$subtotal</td>
  </tr>
 </table>

<table width="580" border="0" cellspacing="0" cellpadding="5" style="table-layout: fixed">
  <tr>
    <td>
    	<div align="center">
<form method="POST" action="">
  <input type="button" value="Print" name="B1" onClick="window.print();">
</form>
<form method="post" action="https://www.paypal.com/us/cgi-bin/webscr">
<input type="hidden" name="cmd" value="_cart">
<input type="hidden" name="upload" value="1">
<input type="hidden" name="business" value="glsa\@linguist.umass.edu">
<input type="hidden" name="item_name_1" value="$titles">
<input type="hidden" name="currency_code" value="USD">
<input type="hidden" name="amount_1" value="$subtotal">
<input type="submit" value="Pay Online Securely">
</form>
	</div>
   </td>
 </tr>
</table>

</body>
</html>
EndOfHTML


