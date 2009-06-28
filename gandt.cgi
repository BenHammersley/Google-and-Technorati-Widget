#!/usr/bin/perl

use warnings;
use strict;
use CGI('div');
use XML::Simple;
use SOAP::Lite;
use LWP::Simple;

my $google_dev_token = "I2ZLf3I0K07Vf1zfOeEUf/P7r4r6t0bR";
my $technorati_dev_token = "7d302f9d84682ce12e9d10d0e2da3707";

my $cgi = CGI::new();

my $name = $cgi->param('name');


print $cgi->header();
print $cgi->start_html(-title=>"Google and Technorati results for $name",
                 -style=> {-src=>'http://www.benhammersley.com/style.css'});

print $cgi->start_div({-id=>'box'});
print $cgi->start_div({-id=>'head'});
print $cgi->h1(' ');
print $cgi->end_div({-id=>'head'});
print $cgi->start_div({-id=>'weblog'});

print $cgi->p('<a href="http://www.benhammersley.com/ego/index.html">Back to more Ego Tools</a>');
print $cgi->p('This data is dynamically gathered from <a href="http://www.google.com">Google</a> and <a href="http://www.technorati.org">Technorati</a>, and so depends on those services actually working <em>right now</em>. If something seems broken, wait a few minutes and try again.'); 

print $cgi->h3("Top 5 Results from Google for $name");

my @params = ($google_dev_token, $name, 0, 5, 0, '', 0, '', 
'latin1', 'latin1');

my $result =
    SOAP::Lite
    -> service("file:GoogleSearch.wsdl")
    -> doGoogleSearch(@params);
    
     foreach my $result (@{$result->{resultElements}}) {
    
      print '<a href="'."$result->{URL}".'">'."$result->{title}".'</a>';
      print $cgi->br();
     }
    


print $cgi->h3('Results from Technorati');

my $technorati_result = get("http://apibeta.technorati.com/search?query=$name&key=$technorati_dev_token") or die "Could not connect to Technorati";
  my $technorati_result_xml = XMLin($technorati_result);
  
  foreach my $result (@{$technorati_result_xml->{document}->{item}}){
      print '<a href="'."$result->{weblog}->{url}".'">'.$result->{weblog}->{name}.'</a>';
      print $cgi->br();
      print "$result->{weblog}->{inboundlinks} Inbound Links";
      print $cgi->br();
      print "Post titled $result->{title}";
      print $cgi->br();
      print "Created $result->{created}";
      print $cgi->blockquote("$result->{excerpt}");
      print $cgi->br();
      print $cgi->br();
      }

  # Additional services to go right here.
  
  print $cgi->end_div({-id=>'weblog'});
  print $cgi->end_div({-id=>'box'});
  print $cgi->end_html();
