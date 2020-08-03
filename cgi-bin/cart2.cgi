#!/usr/bin/perl

# (c) 2001, Paul de Lacy.  Not for resale or public distribution.  Licensed to GLSA Publications Only.
# Code modified by Andrew Lamont (2018) -- added SULA database

# 1. Forms call this page.
# Each element in the form is a Name=Value pair s.t.
# the name is the bookid_type.  The value is the quantity.
# if quantity is 0, then increment by 1.
# if quantity is blank, then automatically deletes.
# First thing is to go through the items of the form and create entries for each item of the type
# ID&TYPE&QUANTITY
# Then string them together with %
# Then make them into a cookie.
# Then spell them out.

# 1. Parse current cookie
@cooky = split(/;/, $ENV{'HTTP_COOKIE'});
foreach $line (@cooky)
        {
        @line2 = split(/=/, $line);
        if ($line2[0] eq "GLSA")
                {
                $cooky2 = $line2[1];
                }
        }
@OLDCOOKY = split(/%/, $cooky2);

# 2. Now $cooky2 contains the GLSA-relevant stuff.

# 1. READ THE POSTVARS
# 2. PUT ALL into an array called @ITEMS.  Each item is format ID_TYPE_QUANTITY

$cookie = "";

push (@ITEMS, $ENV{'QUERY_STRING'});

# Add OLDCOOKY to ITEMS.
# If an item is in OLDCOOKY, then don't add it.

for ($i = 0; $i < scalar(@OLDCOOKY); $i++)
        {
        $k = "no";
        for ($j = 0;  $j < scalar(@ITEMS); $j++)
                {
                # Need to split each ITEMS and OLDCOOKY at "_" and compare
                @tmpItem = split (/_/, @ITEMS[$j]);
                @tmpOld = split(/_/, @OLDCOOKY[$i]);
                $tmpx = @tmpItem[0] . @tmpItem[1];
                $tmpy = @tmpOld[0]. @tmpOld[1];

                if ($tmpx eq $tmpy)
                        {
                        $k = "yes";
                        }
                }
        if ($k eq "no")
                 {
                # Check consistency of cookie item
                @item = split(/_/, @OLDCOOKY[$i]);
                if (($item[2] ne "") && ($item[2] > 0) && (($item[1] eq "CD") || ($item[1] eq "BK")))
                        {
                        push (@ITEMS, @OLDCOOKY[$i]);
                        }
                }
        }

#For each item, concatenate to cookie;
for ($i = 0; $i < scalar(@ITEMS); $i++)
        {
        # Check to see if the itemvalue is >0
        @item = split(/_/, @ITEMS[$i]);
        if (($item[2] ne "") && ($item[2] > 0) && (($item[1] eq "CD") || ($item[1] eq "BK")))
                {
                $cookie = $cookie . "%" . @ITEMS[$i];
                }
        }



# Create Cookie

$domain = "glsa.hypermart.net";
$path = "/";
$expdate = "";

$cooky = "Set-Cookie: GLSA=$cookie; path\=$path; domain\=$domain\n";
print $cooky;


print "Content-type:text/html\n\n";

print <<EndOfHTML;
<html>
<head>
<title>GLSA Publications</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">


<!-- CSS style sheet -->
<link href="../glsa.css" rel="stylesheet" type="text/css">

<style type="text/css">
<!--
body {
        background-color: #87A58D;
}

-->
</style>

</head>

<body>
<div align="center">
  <table width="600" height="100%" border="0" cellspacing="0" cellpadding="5" class="fborder">
    <tr valign="top">
      <td>
        <table width="590" height="30" border="0" cellspacing="0" cellpadding="0" style="table-layout: fixed">
              <tr>
                  <td width="590" height="30" align="center" bgcolor="#0B5992" class="Title">Shopping Cart</td>
              </tr>
        </table>

        <p>&nbsp;<p>

        <FORM Name="purchase" METHOD="POST" action="">
          <div align="center">
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


# Now find the items in the database
# Step 1: Load all the databases for reading.

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

$totalprice = 0;
$element = -1;

# Step 2: first sort the cooky
@ITEMS = sort(@ITEMS);

# Step 3: Go through each cookie element and find it in the databases.
foreach $line (@ITEMS)
{
@item = split(/_/, $line);

foreach $entry (@db)
        {
        @entry2 = split(/%/, $entry);

        # Reduce the number of visible authors
        @author = split(/&/, $entry2[3]);
        if (scalar(@author) > 1)
                {
                $author[0] = "$author[0] et al.";
                }


        # If the item has the same ID as the one in the database
        # print $entry2[0] . " cc " . $item[0] . "<BR>";

        if (($entry2[0] eq $item[0]) && ($item[2] > 0) && (($item[1] eq "BK") || ($item[1] eq "CD") ) )
                {
                print " <tr valign=\"top\">";
                print "<td width=\"90\" class=\"publications\">" . $author[0] . "</td>";
                print "<td width=\"250\" class=\"publications\">" . $entry2[2] . "</td>";

                if ($item[1] eq "CD")
                        {
                        $price = $entry2[6];
                        $total = $price * $item[2];
                              print "<td width=\"35\" class=\"publications\">CD</td>";

                        }
                        else
                        {
                        $item[1] = "BK";
                        $price = $entry2[7];
                        $total = $price * $item[2];
                              print "<td width=\"35\" class=\"publications\">Book</td>";
                        }

                        $itemid = $item[0] . "_" . $item[1];

                print "<td width=\"35\" align=\"right\" class=\"publications\">\$$price</td>";

                print "<td width=\"50\" align=\"right\" class=\"publications\">";
                print "<select name=\"$itemid\" size=1 class=\"publications\" onChange=\"window.location='cart2.cgi?$itemid\_'+document.forms['purchase'].elements['$itemid'].selectedIndex;\";>";
                for ($m = 0; $m < 20; $m++)
                        {
                        print "<option ";
                        if ($m == $item[2]) { print "selected ";}
                        print "value=$m>$m</option>";
                        }
                print "</select></td>";

                print "<td width=\"60\"  align=\"right\" class=\"publications\">\$$total</td>";

                }
        }
}

print "</tr>";

for ($i = 0; $i < scalar(@ITEMS); $i++)
        {
        @tmpItem = split(/_/, @ITEMS[$i]);
        }



print <<EndOfHTML;
            <tr>
                <td colspan="6" width="569" height="10"><img src="../images/divider.gif" height="1" width="569"></td>
            </tr>

          </table>
          </div>
        </form>
EndOfHTML


# Checkout button if cookie not empty

if ($cookie ne "")
        {
        $cookie =~ tr/_/&/;

print <<EndOfHTML;

        <div align="center" class="body">
          To remove a book, set its quantity to &quot;0&quot;

          <p>&nbsp;</p>

          <form name="Ckout" method="POST" action="https://glsa.hypermart.net/cgi-bin/ckout1.cgi">
            <input type="submit" name="GO" value="Checkout">
            <input type="hidden" name="BOOKS" value="$cookie">
          </form>
        </div>

EndOfHTML
        }
        else
        {
        print "<div align=\"center\" class=\"publications\">Your shopping cart is currently empty</div>";
        }


print <<EndOfHTML;

         </td>
        </tr>
         <tr valign="bottom">
        <td>

         <table width="590" height="20" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed">
           <tr>
             <td width="590" height="20" bgcolor="#C9CCED" align="center">
               <a href="#" onClick="window.close();">Close</a>
             </td>
           </tr>
         </table>

      </td>
    </tr>
  </table>

</div>

</BODY>
</HTML>
EndOfHTML

