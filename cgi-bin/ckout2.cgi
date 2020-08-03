#!/usr/bin/perl


# (c) 2001, Paul de Lacy.  Not for resale or public distribution.  Licensed to GLSA Publications Only.
# The original code has been modified by Youri Zabbal and by Wendell Kimper.  Modifications (c) 2004, 2007 GLSA Publications.
# Code modified by Andrew Lamont (2018) -- added SULA database


# Notes on HTML:
# You'll get an error for the following
# 1. You must escape all @ and $ signs in any HTML: e.g. \$ and \@
# 2. There must be a line after the EndOfHTML statement.

# Parameters:
# 0: total cost
# 1: Discount type
# 2: Destination Country
# 3: Shipping Type
# 4: Gift Cert #
# 5: Gift Cert Amount
# 6: Shipping Cost
# 7: Discount Amount

# This script lets the user enter the destination of the order
# and the credit card number, or choose to print the form out.
# It takes several parameters

# First we need to split the pieces of the postvars
read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
@pairs = split(/&/, $buffer);
foreach $pair (@pairs) {
    ($name, $value) = split(/=/, $pair);
    $value =~ tr/+/ /;
    $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    $FORM{$name} = $value;
}

$books = $FORM{'BOOKS'};
$total = $FORM{'Total'};
$discount = $FORM{'ValDiscount'};
$shipping = $FORM{'ValShip'};
$discounttype = $FORM{'discount'};
$shipmethod = $FORM{'shipmethod'};

# we can split it at the entry
# delimiter -- i.e. %
# So, our part of the cookie ends up looking like BOOK=BECK&CD&2%ALDE&BK&1% etc.

@cooky = split(/%/, $books);

@params = split(/%/,$ENV{'QUERY_STRING'});

print "Content-type:text/html\n\n";

print <<EndOfHTML;

<html>

<head>
<title>GLSA Checkout</title>
<meta http-equiv="pragma" content="no-cache">

<script>

submitter = false;

function validate ()
	{
	if (document.forms[0].elements[8].value == '')
		{
		alert('No email address provided');
		return false;
		}
if (submitter == true)
		{
		alert('Your order has already been sent! Please wait.');
		return false;
		}
	submitter = true;
	return true;
	}
</script>

<!-- CSS style sheet -->
<link href="../glsa.css" rel="stylesheet" type="text/css">


</head>

<body>
EndOfHTML

# determine the Discount 
if ($discounttype == 0)
	{
	$discounttype = "None";
	}
if ($discounttype == 0.1)
	{
	$discounttype = "Author";
	}
if ($discounttype == 0.2)
	{
	$discounttype = "UMass student";
	}

#Determine the Shipping method
if ($shipmethod == 1)
	{
	$shipmethod = "Surface Mail";
	}
if ($shipmethod == 2)
	{
	$shipmethod = "AirMail";
	}

print <<EndOfHTML;


<div align="center">
  <table width="600" height="100%" border="0" cellspacing="0" cellpadding="5" class="fborder">
    <tr valign="top">
      <td>	
 	<table width="590" height="70" border="0" cellspacing="0" cellpadding="0" style="table-layout: fixed">
	  <tr>
    	    <td width="590" height="40" align="center">
		<img src="../images/step2.jpg" width="35" height="33" alt="step2.jpg (1215 bytes)">
	    </td>
  	  </tr>	
	  <tr>
    	    <td width="590" height="30" align="center" bgcolor="#0B5992" class="Title">
		Contact Information
	    </td>
  	  </tr>	
	</table> 

	<form method="POST" action="https://glsa.hypermart.net/cgi-bin/formmail.cgi" onSubmit="return validate();">

	  <input type="hidden" name="recipient" value="glsa\@linguist.umass.edu">
	  <input type="hidden" name="redirect" value="/cgi-bin/sentorder.cgi?$discount%$shipping%$total%$books">
	  <input type="hidden" name="subject" value="ORDER FORM">
	  <input type="hidden" name="Total_Amount" value="\$$total">
	  <input type="hidden" name="Discount_Type" value="$discounttype">
	  <input type="hidden" name="Discount_Amount" value="$discount">
	  <input type="hidden" name="Shipping_Cost" value="$shipping">
	  <input type="hidden" name="Shipping_Method" value="$shipmethod">

	  <table width="590" height="30" border="0" cellspacing="0" cellpadding="5" bgcolor="#CCCCFF" style="table-layout: fixed">
    	    <tr>
      	      <td width="30" height="30" bgcolor="#000080" align="center" class="subtitle">1</td>
      	      <td width="540" height="30" align="left"><strong>Destination:</strong> Where would you like your order to go?</td>
    	    </tr>
  	  </table>
	
  	  <table width="590" height="180" border="0" cellspacing="5" cellpadding="5" style="table-layout: fixed">
    	    <tr>
      	      <td width="160" height="30">Email Address:</td>
      	      <td width="395" height="30"><input type="text" name="Destination-Name" size="35" class="textbox"></td>
    	    </tr>
    	    <tr>
      	      <td width="160" height="30">Name (optional):</td>
      	      <td width="395" height="30"><input type="text" name="Destination-Department" size="35" class="textbox"></td>
    	    </tr>
    	    <tr>
      	      <td width="160" height="30">Department (Optional):</td>
      	      <td width="395" height="30"><input type="text" name="Destination-Address" size="35" class="textbox"></td>
    	    </tr>
EndOfHTML


if ($params[2] eq "U")
	{
	$params[2] = "USA";
	}
if ($params[2] eq "C")
	{
	$params[2] = "Canada";
	}
if ($params[2] eq "O")
	{
	$params[2] = "";
	}

print <<EndOfHTML;
	  <br>	  
  
	  <table width="590" height="30" border="0" cellspacing="0" cellpadding="5" bgcolor="#CCCCFF" style="table-layout: fixed">
     	    <tr>
      	      <td width="30" height="30" bgcolor="#000080" align="center" class="subtitle">2</td>
      	      <td width="540" height="30" align="left"><strong>Feedback:</strong></td>
    	    </tr>
  	  </table>
  
	  <table width="590" height="140" border="0" cellspacing="5" cellpadding="5" style="table-layout: fixed">
	     	<tr>
      	      <td width="160" height="60" valign="top">Anything you'd like to tell us about your order?</small></td>
      	      <td width="395" height="60"><textarea rows="3" name="Feedback" cols="35" class="textbox"></textarea></td>
    	    </tr>
   	  </table>

	  <br>	  
  
	  <table width="590" height="30" border="0" cellspacing="0" cellpadding="5" bgcolor="#CCCCFF" style="table-layout: fixed">
     	    <tr>
      	      <td width="30" height="30" bgcolor="#000080" align="center" class="subtitle">3</td>
      	      <td width="540" height="30" align="left"><strong>Submit:</strong> Confirm your order or print an order form.</td>
    	    </tr>
  	  </table>
  

	  <table width="590" height="180" border="0" cellspacing="0" cellpadding="5" style="table-layout: fixed">
     	    <tr>
	      <td width="590" height="150">	    
	    	<blockquote>
		<ul>
		  To pay online, click the `Submit Order' button below and follow the instructions on the next page.
	    	</ul>
 	      </td>
	    </tr>
	    </table>
	  <blockquote>
	    <div align="center">
  	      <input type="submit" value="Submit Order" name="Submit">
	      <br>
	    </div>
	  </blockquote>

EndOfHTML


# Now we need to dynamically create hidden fields that list the items ordered!
# First open the databases.
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

# Now find the records and create the fields.

foreach $items (@cooky)
	{
	@item = split(/&/, $items);

	foreach $line (@db)
		{
		#split each line into its components.
		@dbs = split(/%/, $line);

		# Does this record contain the START code? 

		if ($dbs[0] eq $item[0])
			{
			@author = split(/$/, $dbs[3]);
			if (scalar(@author) > 1)
				{
				$author[0] = "$author[0] et al.";
				}
			$title = $dbs[2];
			$quantity = $item[2];
			if ($item[1] eq 'BK')
				{
				$type = "Book";
				$price = $dbs[7];
				}
				else
				{
				$type = "CD";
				$price = $dbs[6];
				}		
			$total = $price * $quantity;
			$total = sprintf "%.2f", $total;  #round the number to 2 decimal places.

			# Now create the hidden fields
			print "<input type=\"hidden\" name=\"ITEM($item[0]-$type)=\" value=\"$author[0]. $title.  Quantity=$quantity, Type=$type, Price each=$price, Total=$total\">\n";
			}
		}
	}			

$userbrowser = $ENV{'HTTP_USER_AGENT'};
print "<input type=\"hidden\" name=\"Users-browser\" value=\"$userbrowser\">";

print <<EndOfHTML;

<input type="hidden" name="BOOKS" value="$books">

	</form>

     </td>
   </tr>
   <tr valign="bottom">
     <td>

       <table width="590" height="20" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed">
	 <tr>
	   <td width="20" height="20" bgcolor="#C9CCED" align="center">
	     <a href="#" onClick="window.history.back();"><img src="../images/previous_sm.gif" border="0"></a>
	   </td>
	   <td width="80" height="20" bgcolor="#C9CCED" align="left">
	     <a href="#" onClick="window.history.back();">Back</a>
	   </td>
	   <td width="390" height="20" bgcolor="#C9CCED" align="center">
	     <a href="#" onClick="window.close();">Close</a>
	   </td>
	   <td width="80" height="20" bgcolor="#C9CCED" align="right">&nbsp;</td>
	   <td width="20" height="20" bgcolor="#C9CCED" align="center">&nbsp;</td>
	 </tr>
       </table>

    </td>
  </tr>
</table>
</body>
</div>
</html>


EndOfHTML

# The PAY ONLINE button first checks all the fields to make sure they're ok. (using JScript Validate function)
# Then it brings up the order sent screen.
# The order sent screen gives a printable version of the order form for the person's records.
# The Print Order Form button provides a printable order form, and brings up the Print
# dialog box
# The Cancel button returns to the previous item.
