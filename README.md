# bgrad

`bgrab` is a multi-threaded TCP banner grabbing script written in Python.

## Input Formats

Currently only the Metasploit services CSV-output is supported:

	msf > services -r tcp -c port -o services.out.txt

More specifically the script needs a file with the following syntax:

	"127.0.0.1","1080"
	"10.15.20.30","80"
	...

Or anything like this:

	127.0.0.1,8080
	127.0.0.1,80
	"gmail-smtp-in.l.google.com","25"

Invalid lines are ignored.
