#!/usr/bin/perl

# (c) 2001, Paul de Lacy.  Not for resale or public distribution.  Licensed to GLSA Publications Only.
# The original code has been modified by Youri Zabbal.  All modifications (c) 2004 GLSA Publications.

# The purpose of this script is to list a set of publications.
# The script takes three parameters: TYPE OF PUBLICATION, START, and NUMBER
# For example, list.pl?DISS%ALDE%3 will list three dissertations starting with John Alderete's (ALDE).
# The script accesses the appropriate database (DISS, UMOP, NELS, OTHER, ALL)
# It then generates an HTML page.
# and it gives two buttons at the bottom: NEXT and PREVIOUS.
# It also gives a drop-down combobox that allows the user to choose how many publications to
# view at once.

# TO DO!!!
# Need to add stuff to allow for other fields: Shipping, Special Notes, etc.
# Give correct URLs for ABSTRACTs, and IMAGES (background + others)



# ================================================
# (1) Initialize the HTML page.
# ================================================

print "Content-type:text/html\n\n";


# ================================================
# (2) Get the commandline parameters
#
# They are four:
#
# (i) the publication type (DISS, UMOP, NELS, OTHER),
#
# (ii) the START uniqueID (e.g. BECK, UMOP24, NELS25, and the NUM number to list.
# IMPORTANT: Note that the START value "BEGIN" will start at the beginning of the list.
#
# (iii) The NUMBER of publications viewed at one time on the screen.
#
# (iv) Whether you want to see Out of Print books or not.
# The OutofPrint parameter has three values: N(o), Y(es), and O(nly).
# Only shows _only_ out of print books.
# ================================================


@params = split(/%/,$ENV{'QUERY_STRING'});


# Check to see if all the parameters are filled.  If not, assign defaults.

if ($params[0] eq "")
        {
        $params[0] = "DISS";
        }

if ($params[1] eq "")
        {
        $params[1] = "BEGIN";
        }

if ($params[2] eq "")
        {
        $params[2] = 5;
        }

if ($params[3] eq "")
        {
        $params[3] = "N";
        }



# ================================================
# (3) OPEN THE DATABASE
#
# The publication type determines which database is opened.  The database name is in $params[0]
# If the parameter does not match DISS, UMOP, NELS, or OTHER, open all DBs.
# ================================================

if ($params[0] eq "DISS" ||$params[0] eq "NELS" ||$params[0] eq "SULA" || $params[0] eq "UMOP" || $params[0] eq "OTHER")
        {
        open(INF, "database/$params[0].TXT");
        @db_glsa = <INF>;
        close(INF);
        }
        else
        {
        # Open all databases
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
        }



# ================================================
# (4) SORT THE DATABASE
#
# IMPORTANT!!!!  The database is sorted by the FIRST ENTRY, which is UMOPxx for UMOPS, NELSxx for NELS',
# and DISSERTATION_CODE for dissertations.  For dissertations, then, you need to make sure that the code is an accurate
# reflection of the person's last name, so they get alphabetized correctly.
# ================================================

@db_glsa = sort(@db_glsa);   # Sorts the database by the item code parameter (which=the first 4 letters of the surname+the date)



# ================================================
# (5) DELETE EMPTY LINES
#
# If the line is empty, it will return only one partition (i.e. $mouse = 1).
# If the line is empty, the first line will be deleted, done by SHIFT.  Then $cat is set to zero, ensuring that
# the procedure will loop through again.
# If the line is not empty, the procedure will terminate.
# Note that SCALAR(@ARRAY) returns the length of an array!
# ================================================

$cat = 0;
while ($cat < 1)
        {
        $cat = 2;
        @mouse = split(/%/, $db_glsa[0]);
        $dog = scalar(@mouse);

        if ($dog < 2)
                {
                shift(@db_glsa);
                $cat = 0;
                }
        }


#count the number of records in db_glsa

$count = 0;

foreach $line (@db_glsa)
        {
        @dbs = split(/%/, $line);

        if ($params[3] eq "Y" || $params[3] eq $dbs[5] || ($params[3] eq "F" && $dbs[5] eq "N") || ($params[3] eq "N" && $dbs[5] ne "O"))
                {
                $count ++;
                }
        }



# ================================================
# (6) FIND THE RECORD MATCHING THE START PARAMETER
# ================================================

$show = $params[2];


# If the 1 parameter is "END" then go to the end-$show.

if ($params[1] eq "END")
        {
        @db_temp = reverse(@db_glsa);

        $nn = 0;

        foreach $line (@db_temp)
                {
                @dbs = split(/%/, $line);

                if ($nn < $show)
                        {
                        $params[1] = $dbs[0];
                        }


                if ($dbs[5] ne "O")
                        {
                        $nn = $nn + 1;
                        }
                }
        }




# If the 1 parameter is "BEGIN", then go to the beginning of the correct list

if ($params[1] eq "BEGIN")
        {
        $show = 0;

        @db_temp = @db_glsa;

        $nn = 0;

        foreach $line (@db_temp)
                {
                @dbs = split(/%/, $line);

                if ($nn == $show)
                        {
                        $params[1] = $dbs[0];
                        }

                if ($params[3] eq "Y" || $params[3] eq $dbs[5] || ($params[3] eq "F" && $dbs[5] eq "N") || ($params[3] eq "N" && $dbs[5] ne "O"))
                        {
                        $nn = $nn + 1;
                        }
                }

        }

$first="BEGIN";




# ================================================
# (7) Write the HTML Header, including the style sheet, and Body template.
# It assigns the values to the jumpto and jumping comboboxes when the form loads.
# So, onLoad will assign the combobox (i.e. the first element in the form) the value $param[1] and $params[2], respectively
# ================================================

print <<EndOfHTML;
<html>
<head>
<title>GLSA Publications</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">

<!-- CSS style sheet -->
<link href="../glsa.css" rel="stylesheet" type="text/css">

<script language="JavaScript">
//<![CDATA[
function winopen(url,stuff,morestuff) {
        window.open(url,stuff,morestuff).focus();
        }

//]]>
</script>


</head>

<body onLoad="document.forms['jumpto'].elements[0].value='$params[1]';document.forms['jumping'].elements[0].selectedIndex=$params[2]-1;">
<br>

<!-- Main table adds black border, white background, and cellspacing: fixed layout -->

<table width="710" border="0" align="center" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF" class="fborder" style="table-layout: fixed">
  <tr>
    <td width="710">

      <table width="710" border="0" cellpadding="0" cellspacing="5" style="table-layout: fixed">
        <tr>
              <td width="700" height="65" bgcolor="#6699CC"><img src="../images/title.gif" width="700" height="65"></td>
          </tr>
          <tr>
          <td width="700" height="25" bgcolor="#84ACD5">

                  <!-- This is the menu table: fixed layout -->
                  <table width="700" height="25" border="0" cellpadding="0" cellspacing="1" style="table-layout: fixed">
              <tr>
                <td width="90" align="center" class="menu"><a href="../index.html" target="_self" class="menu">Home</a></td>
                <td width="110" align="center" class="selected">Publications</td>
                <td width="90" align="center" class="menu"><a href="../ordering.html" target="_self" class="menu">Ordering</a></td>
                <td width="110" align="center" class="menu"><a href="../authors.html" target="_self" class="menu">For Authors</a></td>
                <td width="90" align="center" class="menu"><a href="../about.html" target="_self" class="menu">About</a></td>
                <td width="70" align="center" class="menu">&nbsp;</td>
                <td width="132" align="center" class="menu"><a href="cart2.cgi" target="cart" class="menu" onClick="winopen('','cart','width=640,height=500,scrollbars=1,resizable=1');">Shopping Cart</a></td>
              </tr>
            </table>

          </td>
          </tr>
          <tr>
              <td width="700" align="left" valign="top" bgcolor="#FFFFFF">

                <!-- This is the body table: fixed layout -->

          <table width="700" border="0" cellspacing="0" cellpadding="5" style="table-layout: fixed">
            <tr>
              <td width="690" height="25">
                <div align="center">
EndOfHTML


# These variables are just used to simplify generating the publications submenu code below

$banner="All Publications";
$submenu="";
$initshow=5;


if ($params[0] eq "ALL" && $params[3] eq "N")
        {
                $banner = "All Available Publications";
                $submenu = "$submenu [<span class=\"chosen\">All</span>] ";
        }
        else
        {
                $submenu = "$submenu [<a href=\"list.cgi?ALL%BEGIN%$initshow%N\" target=\"_self\" class=\"submenu\">All</a>] ";
        }

if ($params[0] eq "ALL" && $params[3] eq "F")
        {
                $banner = "New Publications";
                $submenu = "$submenu [<span class=\"chosen\">New</span>] ";
        }
        else
        {
                $submenu = "$submenu [<a href=\"list.cgi?ALL%BEGIN%$initshow%F\" target=\"_self\" class=\"submenu\">New</a>] ";
        }

if ($params[0] eq "DISS")
        {
                $banner = "Dissertations";
                $submenu = "$submenu [<span class=\"chosen\">Dissertations</span>] ";
        }
        else
        {
                $submenu = "$submenu [<a href=\"list.cgi?DISS%BEGIN%$initshow%N\" target=\"_self\" class=\"submenu\">Dissertations</a>] ";
        }

if ($params[0] eq "UMOP")
        {
                $banner = "UMOP Publications";
                $submenu = "$submenu [<span class=\"chosen\">UMOP</span>] ";
        }
        else
        {
                $submenu = "$submenu [<a href=\"list.cgi?UMOP%END%$initshow%N\" target=\"_self\" class=\"submenu\">UMOP</a>] ";
        }

if ($params[0] eq "NELS")
        {
                $banner = "NELS Publications";
                $submenu = "$submenu [<span class=\"chosen\">NELS</span>] ";
        }
        else
        {
                $submenu = "$submenu [<a href=\"list.cgi?NELS%END%$initshow%N\" target=\"_self\" class=\"submenu\">NELS</a>] ";
        }

if ($params[0] eq "SULA")
        {
                $banner = "SULA Publications";
                $submenu = "$submenu [<span class=\"chosen\">SULA</span>] ";
        }
        else
        {
                $submenu = "$submenu [<a href=\"list.cgi?SULA%END%$initshow%N\" target=\"_self\" class=\"submenu\">SULA</a>] ";
        }

if ($params[0] eq "OTHER")
        {
                $banner = "Other Publications";
                $submenu = "$submenu [<span class=\"chosen\">Other</span>] ";
        }
        else
        {
                $submenu = "$submenu [<a href=\"list.cgi?OTHER%BEGIN%$initshow%N\" target=\"_self\" class=\"submenu\">Other</a>] ";
        }

if ($params[0] eq "ALL" && $params[3] eq "S")
        {
                $banner = "Specials";
                $submenu = "$submenu [<span class=\"chosen\">Specials</span>] ";
        }
        else
        {
                $submenu = "$submenu [<a href=\"list.cgi?ALL%BEGIN%$initshow%S\" target=\"_self\" class=\"submenu\">Specials</a>] ";
        }

if ($params[0] eq "ALL" && $params[3] eq "O")
        {
                $banner = "Out of Print Publications";
                $submenu = "$submenu [<span class=\"chosen\">Out of Print</span>]";
        }
        else
        {
                $submenu = "$submenu [<a href=\"list.cgi?ALL%BEGIN%$initshow%O\" target=\"_self\" class=\"submenu\">Out of Print</a>]";
        }

$submenu = "$submenu [<a href=\"../search.html\" target=\"_self\" class=\"submenu\">Search</a>]";



# Print the submenu and then the banner to html

print <<EndOfHTML;
                  $submenu
                </div>
              </td>
            </tr>
            <tr>
              <td>

                <table width="690" height="20" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed">
                   <tr>
                        <td width="690" height="20" bgcolor="#C9CCED">
                        <div align="center">$banner: $count records</div>
                    </td>
                    </tr>
                </table>

                <br>

EndOfHTML



# (7.5) Put the jumpto menu in:

print <<EndOfHTML;
                <form name="jumpto" method="POST" action="">

                    <div align="center">

                  <select name="cbJumpTo" id="cbJumpTo" size="1" onChange="window.location='list.cgi?$params[0]%'+document.forms[0].elements[0].options[document.forms[0].elements[0].selectedIndex].value+'%$params[2]%$params[3]';">
EndOfHTML

# Now put in the jumpto menu's items...

foreach $line (@db_glsa)
        {
        $go = 0;
        $visible = "";

        @dbs = split(/%/, $line);
        if ($params[3] eq "Y" || $params[3] eq $dbs[5] || ($params[3] eq "F" && $dbs[5] eq "N") || ($params[3] eq "N" && $dbs[5] ne "O"))
                {
                $go = 1;
                }


        #Make sure the jump box doesn't contain an item too long to view

        $visible = substr($dbs[2],0,80);


        if ($go =~ 1)
                {
                if (index ($dbs[0], "UMOP") != -1)
                        {
                        print "<option value=\"$dbs[0]\">$visible</option>";
                        }
                        else
                        {
                        if (index ($dbs[0], "NELS") != -1)
                                {
                                print "<option value=\"$dbs[0]\">$visible</option>";
                                }
                                else
                                {
                                        if (index ($dbs[0], "SULA") != -1)
                                        {
                                        print "<option value=\"$dbs[0]\">$visible</option>";
                                        }
                                        else
                                        {
                                        print "<option value=\"$dbs[0]\">$dbs[3]</option>";
                                        }
                                }
                        }
                }
        }


# Jump menu GO button, not really necessary

print <<EndOfHTML;
                   </select>
                   <input type="button" name="Button1" value="Go" onClick="window.location='list.cgi?$params[0]%'+document.forms[0].elements[0].options[document.forms[0].elements[0].selectedIndex].value+'%$params[2]%$params[3]';">
                </div>

                </FORM>

                <div align="center">

EndOfHTML




# ================================================
# (8) THE MEAT and POTATOES: List selected publications
#
# Go through each line in the database and list only the selected publications
# ================================================

foreach $line (@db_glsa)
        {
        #split each line into its components.
        @dbs = split(/%/, $line);

        # Does this record contain the START code?

        if ($dbs[0] eq $params[1])
                {
                # It _is_ the start code...
                # So set the variable $show at 0
                $show = 0;
                }

        # The Out of Print specifier: if $params[3] is "O" then show _only_ OOP books.
        # If $params[3] is "N" then don't show them.
        # If $params[3] is "Y" then show them.
        # If $params[3] is "F" then show only New and forthcoming books.
        # If $params[3] is "S" then show only Specials!

        $ok = 0;
        if ($params[3] eq "Y" || $params[3] eq $dbs[5] || ($params[3] eq "F" && $dbs[5] eq "N") || ($params[3] eq "N" && $dbs[5] ne "O"))
                {
                $ok = 1;
                }


        # The last entry shown has been assigned to $next, so simply find $next and add one.

        if ($show == $params[2] && $ok =~ 1)
                {
                $next = $dbs[0];
                $show = $show + 1;
                }


        if ($show < $params[2] && $ok =~ 1)
                {
                # If $show is less than        NUM times, then print the record out.
                        # !!!!!!!!!! IMPORTANT !!!!!!!!!!  This is the guts of the procedure.
                        # The code is put in here!

                # Convert $dbs[3] into an author list.
                @authors = split(/&/, $dbs[3]);
                $author = join("; ", @authors);

                # $first will capture the first item shown.
                if ($first eq "BEGIN")
                        {
                        $first = $dbs[0];
                        }

                $next = $dbs[0];

                $title = "$dbs[2] ($dbs[1])";

                if ($dbs[4] > 1)
                        {
                        $title = "$title [$dbs[4] volumes]";
                        }
                if ($dbs[5] eq "O")
                        {
                        $title = "$title (Out of Print)";
                        }
                if ($dbs[5] eq "F")
                        {
                        $title = "$title (In Press)";
                        }

                        # Start Publications info
print <<EndOfHTML;
                              <table width="670" border="0" cellpadding="10" cellspacing="0" style="table-layout: fixed">
                              <tr>
                                <td width="440" align="left" valign="top" class="publications">
                                  <a href="abstract.cgi?$dbs[0]" target="abstract" onClick="winopen('','abstract','width=640,height=500,scrollbars=1,resizable=1');">$title</a>
                                  <br>
                                  $author
                                  <br>
EndOfHTML


                # Fields?
                if ($dbs[10] ne "")
                        {
                        print "Field(s): $dbs[10]<br>";
                        }

                # Special Notes?
                if ($dbs[9] ne "")
                        {
                        print "Notes: $dbs[9]<br>";
                        }


                # Counts as x for shipping
                if ($dbs[8] > 1)
                        {
                        print "Counts as $dbs[8] items for shipping purposes.<br>";
                        }

                # Keywords or BookSurge HTTP address
                $keywords = substr($dbs[11],0,(length($dbs[11])-2));

                if ($keywords ne "")
                        {
                        print "$keywords<br>";
                        }


                # End Column 1 Publications info
                print "</td>";


                # Start Column 2 Pricing and links to cart.  Embed a table.
                print "<td width=\"140\" align=\"right\" valign=\"top\">";


                # Check book and cd availability

                $bkflag = ($dbs[7] != 0 && $dbs[5] ne "O");
                $cdflag = ($dbs[6] != 0 && $dbs[5] ne "O");


                if ($bkflag == 1 || $cdflag == 1)
                        {
print <<EndOfHTML;
                          <table width="140" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed">
EndOfHTML

                        # If Book available, print price and add-to-cart link
                        if ($bkflag == 1)
                                {
print <<EndOfHTML;
                                        <tr>
                                        <td width="115" height="20" align="right" valign="top" class="publications">
                                    <a href="cart2.cgi?$dbs[0]_BK_1" target="cart" onClick="winopen('','cart','width=640,height=500,scrollbars=1,resizable=1');">Add Book: \$$dbs[7]</a>&nbsp;
                                  </td>
                                  <td width="25" height="20" align="right" valign="top" >
                                    <a href="cart2.cgi?$dbs[0]_BK_1" target="cart" onClick="winopen('','cart','width=640,height=500,scrollbars=1,resizable=1');"><img src="../images/book40.gif" border="0" width="17" height="17"></a>
                                  </td>
                                </tr>
EndOfHTML

                                }


                        # If CD available, print price and add-to-cart link
                        if ($cdflag == 1)
                                {
print <<EndOfHTML;
                                        <tr>
                                        <td width="115" height="20" align="right" valign="top" class="publications">
                                    <a href="cart2.cgi?$dbs[0]_CD_1" target="cart" onClick="winopen('','cart','width=640,height=500,scrollbars=1,resizable=1');">Add CD: \$$dbs[6]</a>&nbsp;
                                  </td>
                                  <td width="25" height="20" align="right" valign="top" >
                                    <a href="cart2.cgi?$dbs[0]_CD_1" target="cart" onClick="winopen('','cart','width=640,height=500,scrollbars=1,resizable=1');"><img src="../images/cd.jpg" border="0" width="17" height="17"></a>
                                  </td>
                                </tr>
EndOfHTML

                                }

print <<EndOfHTML;
                        <tr>
                                <td width="115" height="20" align="right" valign="top" class="publications">
                            <a href="cart2.cgi" target="cart" onClick="winopen('','cart','width=640,height=500,scrollbars=1,resizable=1');">See Cart</a>&nbsp;
                          </td>
                          <td width="25" height="20" align="right" valign="top" >
                            <a href="cart2.cgi" target="cart" onClick="winopen('','cart','width=640,height=500,scrollbars=1,resizable=1');"><img src="../images/add-cart.gif" border="0" width="17" height="17"></a>
                          </td>
                        </tr>
EndOfHTML



                        print "</table>";


                        }

                        # End Column 2 Pricing and links to cart
                        print "</td>";


print <<EndOfHTML;
                             </tr>
                           </table>

                            <img src="../images/divider.gif" height="1" width="670">

EndOfHTML


                # increment $Show
                $show = $show + 1;
                }
        }



# ================================================
# (9) Calculate Previous
#
# For the PREVIOUS button you need the START $params[1] minus $PARAMS[2].
# But we also need to not count out of print books and such.
# ================================================

$previous = $first;  #to make this the default.
$tonext = 0;

# To do this, reverse the database and add $params[2]...

@db_glsa = reverse(@db_glsa);
foreach $line (@db_glsa)
        {
        @dbs = split(/%/, $line);

        # Does this record contain the START code?
        if ($dbs[0] =~ $first)
                {
                # It _is_ the start code...
                # So start the variable $show off at 0
                $tonext = 0;
                $previous = $dbs[0];
                }

        # The Out of Print specifier: if $params[3] is "O" then show _only_ OOP books.
        # If $params[3] is "N" then don't show them.
        # If $params[3] is "Y" then show them.
        # If $params[3] is "F" then show only New and forthcoming books.
        # If $params[3] is "S" then show only Specials!

        $ok = 0;
        if ($params[3] eq "Y" || $params[3] eq $dbs[5] || ($params[3] eq "F" && $dbs[5] eq "N") || ($params[3] eq "N" && $dbs[5] ne "O"))
                {
                $ok = 1;
                }


        if ($tonext < $params[2]+1 && $ok =~ 1)
                {
                $previous = $dbs[0];
                $tonext = $tonext+1;
                }
        }



# ================================================
# (10) Jumping combobox and NEXT/PREVIOUS buttons
#
# Now we have to generate the NEXT and PREVIOUS button, with the combobox.
# ================================================

print <<EndOfHTML;
                </div>

                <br>

                <FORM name=jumping action="" method=POST>

                   <table width="690" height="20" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed">
                     <tr bgcolor="#C9DBED">
                       <td width="20" height="20">
                         <div align="center">
                           <a href="list.cgi?$params[0]%$previous%$params[2]%$params[3]"><img src="../images/previous_sm.gif" border="0"></a>
                         </div>
                       </td>
                       <td width="90" height="20">
                         <div align="left">
                           <a href="list.cgi?$params[0]%$previous%$params[2]%$params[3]">Previous</a>
                         </div>
                       </td>
                       <td width="470" height="20">
                         <div align="center">
                           <select name="cbNumber" id="cbNumber" size="1" onChange="window.location='list.cgi?$params[0]%$params[1]%'+document.forms['jumping'].elements[0].options[document.forms['jumping'].elements[0].selectedIndex].text+'%$params[3]';">
                                       <option value="1">1</option>
                                       <option value="2">2</option>
                                       <option value="3">3</option>
                                       <option value="4">4</option>
                                       <option value="5">5</option>
                                       <option value="6">6</option>
                                       <option value="7">7</option>
                                     <option value="8">8</option>
                                       <option value="9">9</option>
                                       <option value="10">10</option>
                                  </select>
                          </div>
                        </td>
                        <td width="90" height="20">
                          <div align="right">
                            <a href="list.cgi?$params[0]%$next%$params[2]%$params[3]">Next</a>
                          </div>
                        </td>
                        <td width="20" height="20">
                          <div align="center">
                            <a href="list.cgi?$params[0]%$next%$params[2]%$params[3]"><img src="../images/next_sm.gif" border="0"></a>
                          </div>
                        </td>
                      </tr>
                    </table>

                  </form>

                  <br>
                </td>
              </tr>
            </table>

        </tr>
        <tr>
          <td bgcolor="#FFFFFF">

            <table width="700" height="20" border="0" cellpadding="0" cellspacing="0" style="table-layout: fixed">
                    <tr>
                        <td width="300" class="copyright">&copy; 2003 GLSA Publications<br></td>
                        <td width="400" align="right" class="copyright">Last Updated December 17, 2006</td>
                    </tr>
            </table>

          </td>
        </tr>
      </table>

   </td>
  </tr>
</table>
</body>
</html>

EndOfHTML
