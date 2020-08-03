#!/usr/bin/perl

print "Content-type:text/html\n\n";

print "<html><head><title>Test Page</title></head>\n";
print "<body>\n";
print "<h2>Hello, world!</h2>\n";

open(FILE, "sample.txt");
@fileinfo = <FILE>;
close(FILE);

print "Surname=", $fileinfo[1];

print "</body></html>\n";
