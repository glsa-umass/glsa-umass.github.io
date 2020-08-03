#!/usr/bin/perl

# (c) 2001, Paul de Lacy.  Not for resale or public distribution.  Licensed to GLSA Publications Only.
# The original code has been modified by Youri Zabbal.  All modifications (c) 2004 GLSA Publications.
# Code modified by Andrew Lamont (2018) -- added SULA database

# Get the parameters
@params = split(/%/,$ENV{'QUERY_STRING'});

# Gets POSTed two values:
# BOOKS is the book info
# $PARAMS is the parameter info:
# Params: 0=Discount type, 1=Ship_to, 2=Ship-how, 3=$Gift_ct#, 4=Gift-Cert amount
# Discount: N = none, U= Umass student, A = author.
# Ship_to: U=USA, C=Canada, O=Other.
# Ship_how: A=airmail, S=surface
# Gift-ct#: a number.
# Gift-amt: a number.

$totalquantity = 0;
$discount = 0;
$shipping = 0;
$shipItem = 3; #this is the cost per item for shipping.
$giftcert = 0;

# Open all the databases.  Assign them all to @db.

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

# parse options into an array
$options = split(/%/, $FORM{'OPTIONS'});

# Now that we have our part of the cooky (i.e. $cooky2), we can split it at the entry
# delimiter -- i.e. %
# So, our part of the cookie ends up looking like BOOK=BECK&CD&2%ALDE&BK&1% etc.

@cooky = split(/%/, $books);

# This script is the first step in the checkout process.
# The procedure:
# (1) List selected items for confirmation.
#	Also included: 	1. Discounts - choose from combobox
#			2. GiftCert-number-+amount
#			3. Shipping: 	(i) to US, Canada, Other
#					(iii) Airmail/Surface Mail
#	If not satisfied, return to shopping cart to change items/quantities, etc.
#	Have _discounts_: automatically updates the subtotal.
# (2) Destination + Contact info.
# (3) Credit Card information.
# (4) Send confirmation page!
# The key: to submit each form to the next CGI script.  That way, we don't need to 
# burden the cookie with information.

# (1) Initialize the HTML page.

print "Content-type:text/html\n\n";

print <<EndOfHTML;
<HTML>
<head>
<meta http-equiv="pragma" content="no-cache">
<script>
function calcship ()
	{
	x = document.forms[0].quant.value;
	y = document.forms[0].country.options[document.forms[0].country.selectedIndex].value;
	z = document.forms[0].shipmethod.options[document.forms[0].shipmethod.selectedIndex].value;

	if (y == "X")
		{
		document.forms[0].ValShip.value = "";
		return false;
		}


	if (x == 0)
		{
		x = 1;
		} 
	// divide by 2 for USA	
	if (y == 0)
		{
		x = Math.round(x/2);
		}
	
	// if surfacemail
	if (z == 1)
		{
		if (y == 0)
			{
			shiptotal = x * 6;
			}
		if (y == 1)
			{
			shiptotal = x * 8;
			}
		if (y == 2)
			{
			alert ('Please contact the GLSA for shipping outside the USA and Canada.');
			document.forms[0].ValShip.value = "";
			return false;
			}
		if (y == 3)
			{
			shiptotal = 0;
			}
		}

	// if airmail
	if (z == 2)
		{
		if (y == 0)
			{
		shiptotal = x * 6;
			}
		if (y == 1)
			{
			shiptotal = x * 7;
			}
		if (y == 2)
			{
			alert ('Please contact the GLSA for shipping outside the USA and Canada.');
			document.forms[0].ValShip.value = "";
			return false;
			}
		}
	document.forms[0].ValShip.value = shiptotal;

	calcTotal();

	return true;
	}


function calcDiscount ()
	{
	x = document.forms[0].discount.options[document.forms[0].discount.selectedIndex].value;
	subtot = (document.forms[0].subtotal.value * 1);
	subtot = subtot * x;

	document.forms[0].ValDiscount.value = Math.round(subtot);

	calcTotal();

	return true;
	}

function calcTotal ()
	{
	tot = (document.forms[0].ValShip.value * 1);
	tot = tot + (document.forms[0].subtotal.value * 1);
	tot = tot - (document.forms[0].ValDiscount.value * 1);
	document.forms[0].Total.value = tot;
	return true;
	}

</script>

<!-- CSS style sheet -->
<link href="../glsa.css" rel="stylesheet" type="text/css">


</head>
<body onLoad="calcship()">

<div align="center">
  <table width="600" height="100%" border="0" cellspacing="0" cellpadding="5" class="fborder">
    <tr valign="top">
      <td>	
 	<table width="590" height="70" border="0" cellspacing="0" cellpadding="0" style="table-layout: fixed">
	  <tr>
    	    <td width="590" height="40" align="center">
		<img src="../images/step1.jpg" width="35" height="33" alt="step1.jpg (1165 bytes)">
	    </td>
  	  </tr>	
	  <tr>
    	    <td width="590" height="30" align="center" bgcolor="#0B5992" class="Title">
		Review your order:
	    </td>
  	  </tr>	
	</table> 

	<form method="POST" action="https://glsa.hypermart.net/cgi-bin/ckout2.cgi">
  	  <div align="center">      
	  <table width="580" border="0" cellspacing="0" cellpadding="5" style="table-layout: fixed">
            <tr valign="top">
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

# Fill in the initial stuff.


# Format of each cookie entry:CODE&TYPE&QUANTITY
# Now find the entries in the DB and list them.

$grandtotal = 0;

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
			@author = split(/&/, $dbs[3]);
			if (scalar(@author) > 1)
				{
				$author[0] = "$author[0] et al.";
				}

			$title = $dbs[2];
			$quantity = $item[2];
			if ($item[1] eq 'BK')
				{
				$pic = "Book";
				$price = $dbs[7];
				}
				else
				{
				$pic = "CD";
				$price = $dbs[6];
				}		
			# We add the quantity of the book to the totalquantity.
			# But if the book counts as 2 for shipping, we need to multiply it as such.
			# $dbs[8] holds the number of books this counts for in terms of shipping, so
			# we simply multiply $quantity by that.
			$totalquantity = $totalquantity + ($quantity * $dbs[8]);
			
			# We need to add a note if the item counts as more than one thing for shipping.
			if ($dbs[8] > 1)
				{
				$title = "$title <span style=\"color: #FF0000\">*</span>";
				}
			$total = $price * $quantity;
			$total = sprintf "%.2f", $total;  #round the number to 2 decimal places.

			$grandtotal = $grandtotal + $total;
			$grandtotal = sprintf "%.2f", $grandtotal;

# Now show the entry...
print <<EndOfHTML;
	    <tr valign="top">
      	      <td width="90" height="20" class="publications">$author[0]</td>
      	      <td width="250" height="20" class="publications">$title</td>
      	      <td width="35" height="20" class="publications">$pic</td>
      	      <td width="35" height="20" class="publications" align="right">$price</td>
      	      <td width="50" height="20" class="publications" align="right">$quantity</td>
              <td width="60" height="20" class="publications" align="right">$total</td>
  	    </tr>

EndOfHTML
			}
		}
	}



print <<EndOfHTML;
  	    <tr>
	      <td colspan="6" width="569" height="10" align="right"><img src="../images/divider.gif" height="1" width="190"></td>
	    </tr>
	  </table>

	  <table width="580" border="0" cellspacing="0" cellpadding="5" style="table-layout: fixed">
    	    <tr>
       	      <td width="70" height="30" align="left">&nbsp</td>
      	      <td width="320" height="30" align="left">&nbsp</td>
     	      <td width="70" height="30" align="right">Total: </td>
	      <td width="80" height="30" align="right" class="publications">$grandtotal</td>

	      <input type="hidden" name="quant" value="$totalquantity">
	      <input type="hidden" name="subtotal" value="$grandtotal">
            </tr>
EndOfHTML

# HOW TO ROUND A NUMBER IN PERL.
# Perl offers no simple "Round" function.  So, we need to use the function "sprintf".  Sprintf takes a formatting command
# so here we specify that we are dealing with a floating point number by using the %f tag, and we want 2 decimal places
#, indicated by putting .2 between the % and f.

print <<EndOfHTML;
	      </td>
          </table>

	  <br>


	  <!-- This hidden values do all the work on the next page -->
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
	   <td width="80" height="20" bgcolor="#C9CCED" align="right">
	     <a href="#" onClick="document.forms[0].submit()">Continue</a>
	   </td>
	   <td width="20" height="20" bgcolor="#C9CCED" align="center">
	     <a href="#" onClick="document.forms[0].submit()"><img src="../images/next_sm.gif" border="0"></a>
	   </td>
	 </tr>
       </table>

    </td>
  </tr>
</table>

</body>
</html>

EndOfHTML

# The code above generates two buttons.
# The Continue button goes to "ckout2.pl" and sends the parameters:
# (1) Total cost
# (2) + all the parameters that this item got.



