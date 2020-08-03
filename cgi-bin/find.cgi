#!/usr/bin/perl

# (c) 2001, Paul de Lacy.  Not for resale or public distribution.  Licensed to GLSA Publications Only.
# Code modified by Andrew Lamont (2018) -- added SULA database

# Takes the form from search.htm and looks for stuff.

# First get the form results

print "Content-type:text/html\n\n";

print <<EndOfHTML;
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>Untitled Document</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">

<!-- CSS style sheet -->
<link href="../glsa.css" rel="stylesheet" type="text/css">

</head>

<body>
<br>
<table width="712"  border="0" align="center" cellpadding="1" cellspacing="0" bgcolor="#000000">
  <tr>
    <td width="710"><table width="700"  border="0" cellpadding="0" cellspacing="0" bgcolor="#FFFFFF">
      <tr>
        <td><table  border="0" align="center" cellpadding="0" cellspacing="5">
          <tr>
            <td width="700" bgcolor="#6699CC"><img src="../images/title.gif" width="700" height="65"></td>
          </tr>
          <tr>
            <td height="25" bgcolor="#84ACD5">
                <table width="700" height="25"  border="0" cellpadding="0" cellspacing="1">
                  <tr bgcolor="#0B5992">
                    <td width="90" align="center"><a href="../index.html" target="_self" class="menu">Home</a></td>
                    <td width="110" align="center" bgcolor="#FFFFFF" class="selected">Publications</td>
                    <td width="90" align="center"><a href="../ordering.html" target="_self" class="menu">Ordering</a></td>
                    <td width="110" align="center"><a href="../authors.html" target="_self" class="menu">For Authors</a></td>
                    <td width="90" align="center"><a href="../about.html" target="_self" class="menu">About</a></td>
                    <td width="70" align="center" bgcolor="#0B5992">&nbsp;</td>
                    <td width="132" align="center" bgcolor="#0B5992"><a href="cart2.cgi" class="menu" target="_self">Shopping Cart</a></td>
                  </tr>
                </table>              </td>
          </tr>
          <tr>
            <td height="450" align="left" valign="top" bgcolor="#FFFFFF">
                <table width="700" border="0" cellpadding="5" cellspacing="0" bgcolor="#FFFFFF">
                      <tr>
                   <td height="20" align="center">
                         [<a href="list.cgi?ALL%BEGIN%3%N" target="_self" class="submenu">All</a>]  [<a href="list.cgi?ALL%BEGIN%3%F" target="_self" class="submenu">New</a>]  [<a href="list.cgi?DISS%BEGIN%3%N" target="_self" class="submenu">Dissertations</a>]  [<a href="list.cgi?UMOP%END%3%N" target="_self" class="submenu">UMOP</a>]  [<a href="list.cgi?NELS%END%3%N" target="_self" class="submenu">NELS</a>]  [<a href="list.cgi?OTHER%BEGIN%3%N" target="_self" class="submenu">Other</a>]  [<a href="list.cgi?ALL%BEGIN%3%S" target="_self" class="submenu">Specials</a>]  [<a href="list.cgi?ALL%BEGIN%3%O" target="_self" class="submenu">Out of Print</a>] [<a href="../search.html" target="_self" class="submenu">Search</a>]
                      </td>
                     </tr>
                      <tr>
                   <td>
EndOfHTML



read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
@pairs = split(/&/, $buffer);

$available = 0;
$OOP = 0;
foreach $pair (@pairs)
        {
            ($name, $value) = split(/=/, $pair);
            $value =~ tr/+/ /;
            $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
        if ($name eq "srDiss")
                {
                push(@dbs, "DISS.TXT");
                }
        if ($name eq "srUMOP")
                {
                push(@dbs, "UMOP.TXT");
                }
        if ($name eq "srSULA")
                {
                push(@dbs, "SULA.TXT");
                }
        if ($name eq "srNELS")
                {
                push(@dbs, "NELS.TXT");
                }
        if ($name eq "srOther")
                {
                push(@dbs, "OTHER.TXT");
                }
        if ($name eq "srBook")
                {
                $book = 1;
                }
                else
                {
                $book=0;
                }
        if ($name eq "srCD")
                {
                $CD = 1;
                }
                else {
                $CD=0;
                }
        if ($name eq "srAuthor")
                {
                $author=$value;
                }
        if ($name eq "srTitle")
                {
                $title=$value;
                }
        if ($name eq "srAvailable")
                {
                $available=1;
                }
        if ($name eq "srOOP")
                {
                $OOP = 1;
                }
        if ($name eq "srKeywords")
                {
                $keywords=$value;
                }
        if (index($name, "sk") != -1)
                {
                push(@field, $value);
                }

        }
# now @cat contains our values, already formatted.

# Now load all the DBs

foreach $line(@dbs)
        {
        open(INF, "database/$line");
        @db_diss = <INF>;
        close(INF);
        @db_diss = sort(@db_diss);
        push(@db, @db_diss);
        }

# Now go through each line and look for the variables.  Make a link for each one that's relevant.
# $ok is the control variable.  If a record doesn't match some entry, then $ok is set to 0.


$count = 0;

foreach $line (@db)
        {
        $ok = 1;

        @item = split(/%/, $line);
        #look for $title in the title.  The function uc() converts to uppercase, otherwise index() is case sensitive!
        if ($title ne "")
                {
                if (index(uc($item[2]), uc($title)) =~ -1)
                        {
                        $ok = 0;
                        }
                }
        #look for authors.
        if ($author ne "")
                {
                if (index(uc($item[3]), uc($author)) =~ -1)
                        {
                        $ok = 0;
                        }
                }
        #look for keywords
        if ($keywords ne "")
                {
                if (index(uc($item[11]), uc($keywords)) =~ -1)
                        {
                        $ok = 0;
                        }
                }

        # Does the current item belong to any of the fields specified?
        # If the item has no fields specified, then skip this...

        if ($ok != 0 && $item[10] ne "")
                {
                $fi = 0;
                foreach $line2 (@field)
                        {
                        if (index(uc($item[10]), uc($line2)) != -1)
                                {
                                $fi = 1;
                                }
                        if ($line2 eq "AnyField")
                                {
                                $fi = 1;
                                }
                        }
                $ok = $fi;
                }

        if ($OOP =~ 0 && $item[5] eq "O")
                {
                $ok = 0;
                }

        if ($available =~ 0 && $item[5] ne "O")
                {
                $ok = 0;
                }

        if ($ok =~ 1)
                {
                @author = split(/&/, $item[3]);
                if (scalar(@author) > 1)
                        {
                        $author[0] = "$author[0] et al.";
                        }

                push(@found, "$item[0]%$author[0]%$item[1]%$item[2]");
                $count = $count + 1;
                }
        }


print <<EndOfHTML;
                        <table width="690" border="0" cellpadding="0" cellspacing="0">
                          <tr>
                                    <td width="690" height="20" align="center" bgcolor="#C9CCED" class="selected">Search Result: $count records found</td>
                           </tr>
                        </table>
                   </td>
                     </tr>
                      <tr>
                    <td>
                        <blockquote>
EndOfHTML



@found = sort(@found);

foreach $line (@found)
        {
        @item = split(/%/, $line);

print <<EndOfHTML;

<a href="list.cgi?ALL%$item[0]%1%Y">$item[1]&nbsp; ($item[2])&nbsp;&nbsp; $item[3]</a><br>

EndOfHTML
        }

print <<EndOfHTML;
                </blockquote>
        </td>
              </tr>
            </table>
                        </td>
          </tr>
          <tr>
            <td bgcolor="#FFFFFF"><table width="700" border="0" cellspacing="0" cellpadding="0">
              <tr>
                <td class="copyright">&copy; 2003 GLSA Publications<br>
                                </td>
                <td align="right" class="copyright">Last Updated December 17, 2006</td>
              </tr>
            </table></td>
          </tr>
        </table></td>
      </tr>
    </table></td>
  </tr>
</table>
</body>
</html>


EndOfHTML
