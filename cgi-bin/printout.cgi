#!/usr/bin/perl

# (c) 2001, Paul de Lacy.  Not for resale or public distribution.  Licensed to GLSA Publications Only.
# Code modified by Andrew Lamont (2018) -- added SULA database

print "Content-type:text/html\n\n";


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

($sec,$min,$hour,$mday,$mon,$year,$wday,$yday) = gmtime(time);
$year += 1900;
$mon += 1;

# The form will be sent here.  Extract all necessary information from it.
# Get the form data and put the values into @cat.
# The form data in order:
# 0. The email recipient
# 1. The redirected address.
# 2. The Subject line
# 3. The total cost
# 4. Discount type.
# 5. Discount amount.
# 6. Shipping cost
# 7. Shipping method
# 8. Gift Cert number
# 9. Gift Cert amount
# 10-15. Destination address
# 16-18. Contact info
# 19-24: credit card info.

read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
@pairs = split(/&/, $buffer);
foreach $pair (@pairs) {
    ($name, $value) = split(/=/, $pair);
    $value =~ tr/+/ /;
    $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    $FORM{$name} = $value;
}

print <<EndOfHTML;
<html>
<head>
<title>ORDER FORM</title>
<meta name="GENERATOR" content="Microsoft FrontPage 3.0">
</head>
<body>

<p><strong><font face="Arial">GLSA Order Form</font></strong></p>

<p><small><font face="Arial">GLSA Publications<br>
South College<br>
University of Massachusetts, Amherst<br>
MA 01002<br>
U.S.A.</font></small></p>

<p><font face="Arial"><strong><small>FAX<em>: USA (413) 545-2792</em></small></strong><br>
<small>E-mail: glsa\@linguist.umass.edu<br>
</small></font></p>

<small><font face="Arial">Date: $mon/$mday/$year</font></small>
<br>

<table border="0" width="100%" cellspacing="0" bgcolor="#FFFFFF">
    <tr>
      <td width="16%" bgcolor="#D7D7D7"><font face="Arial" color="#000000"><strong><small>Author/Editor(s)</small></strong></font></td>
      <td width="16%" bgcolor="#D7D7D7"><font face="Arial" color="#000000"><strong><small>Title</small></strong></font></td>
      <td width="19%" bgcolor="#D7D7D7"><font face="Arial" color="#000000"><strong><small>Book/CD</small></strong></font></td>
      <td width="15%" bgcolor="#D7D7D7"><font face="Arial" color="#000000"><strong><small>Price
      @</small></strong></font></td>
      <td width="14%" bgcolor="#D7D7D7"><font face="Arial" color="#000000"><strong><small>Quantity</small></strong></font></td>
      <td width="20%" bgcolor="#D7D7D7"><font face="Arial" color="#000000"><strong><small>Total</small></strong></font></td>
    </tr>
EndOfHTML


# First we need to split the pieces of the cookie
$cooky2 = $FORM{'BOOKS'};

# Now we need to find the part that is the entry "BOOKS"
# Note that to do that we take the substring from 1 to 6...
# Now that we have our part of the cooky (i.e. $cooky2), we can split it at the entry
# delimiter -- i.e. %
# So, our part of the cookie ends up looking like BOOK=BECK&CD&2%ALDE&BK&1% etc.

@cooky = split(/%/, $cooky2);

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
                                $author = "$author et al.";
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


# Now show the entry...
print <<EndOfHTML;
   <tr>
      <td width="20%"><small><font face="Arial">$author[0]</font></small></td>
      <td width="49%"><small><font face="Arial">$title</font></small></td>
      <td width="10%"><small><font face="Arial">$type</font></small></td>
      <td width="7%"><small><font face="Arial">$price</font></small></td>
      <td width="7%"><small><font face="Arial">$quantity</font></small></td>
      <td width="7%"><small><font face="Arial">$total</small></font></td>
    </tr>

EndOfHTML
                        }
                }
        }

$shipmethod = $FORM{'Shipping_Method'};
$discount = $FORM{'Discount_Amount'};
$discounttype = $FORM{'Discount_Type'};
$shipping = $FORM{'Shipping_Cost'};
$total = $FORM{'Total_Amount'};
$destName = $FORM{'Destination-Name'};
$destDept = $FORM{'Destination-Department'};
$destAddress = $FORM{'Destination-Address'};
$destCity = $FORM{'Destination-City'};
$destZip = $FORM{'Destination-Zip'};
$destCountry = $FORM{'Destination-Country'};
$contactName = $FORM{'Contact-Name'};
$contactEmail = $FORM{'Contact-Email'};
$cardName = $FORM{'CreditCard-Name'};
$cardNumber = $FORM{'CreditCard-Number'};
$cardType = $FORM{'CreditCard-Type'};
$cardAddress = $FORM{'CreditCard-Address'};
$cardYear = $FORM{'CreditCard-ExpiryYear'};
$cardMonth = $FORM{'CreditCard-ExpiryMonth'};
$feedback = $FORM{'Feedback'};

print <<EndOfHTML;
</table>
<table border="0" width="100%" cellspacing="1" cellpadding="0">
  <tr>
    <td width="66%" align="left" colspan="2"><hr>
    </td>
    <td width="34%"></td>
  </tr>
  <tr>
     <td width="73%" align="left"><font face="Arial"><strong><small>Shipping</strong></small></font></td>
    <td width="20%"><font face="Arial"><strong><small>via $shipmethod</strong></small></font></td>
    <td width="7%"><font face="Arial"><small>$shipping</small></font></td>

  </tr>
  <tr>
    <td width="73%" align="left"><font face="Arial"><strong><small>Discount</strong></small></font></td>
    <td width="20%"><font face="Arial"><strong><small>$discounttype</strong></small></font></td>
    <td width="7%"><font face="Arial"><small>$discount</small></font></td>
  </tr>
  <tr>
    <td width="73%" align="left" bgcolor="#E2E2E2"></td>
    <td width="20%" bgcolor="#E2E2E2"><font face="Arial"><strong><small>Total</strong></small></font></td>
    <td width="7%" bgcolor="#E2E2E2"><font face="Arial"><strong><small>$total</strong></small></font></td>
  </tr>

</table>

<table border="0" width="100%" cellspacing="1" cellpadding="0">
<tr>
<td width="50%" align="left">
<strong>Send Order To:</strong><br>
$destName <br>
$destDept <br>
$destAddress <br>
$destCity <br>
$destZip <br>
$destCountry <br>
</td>
<td width="50%" align="left">
<strong>Contact Information:</strong><br>
<em> Name: </em> $contactName <br>
<em> E-mail/phone: </em> $contactEmail <br>
<em> Feedback: </em> $feedback <br>

</td>
</tr>
</table>
EndOfHTML

if ($cardNumber ne "")
        {
print <<EndOfHTML;
<p><strong>Credit Card Details:<br></strong>
<em>Name:</em> $cardName <br>
<em>Card Number:</em> $cardNumber <br>
<em>Expiry Date:</em> $cardMonth of $cardYear <br>
<em>Card Type:</em> $cardType <br>
<em>Billing Address:</em> $cardAddress <br>
</p>
EndOfHTML
        }
        else
        {
        print "<strong> Please make your cheque out to <em> GLSA Publications </em></strong>.";
        }

print <<EndOfHTML;
<p>&nbsp;</p>

<form method="POST" action="">
<div
  align="center"><center><p><input type="button" value="Print" name="B1"
  onClick="window.print();"><br>
  <input type="button" value="Return to Browsing" name="B2" onClick="window.location='http://glsa.hypermart.net/cgi-bin/clear.htm'"></p>
  </center></div>
</form>
</body>
</html>


EndOfHTML
