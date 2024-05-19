import socket
import dns
import dns.resolver
import sys

subdomainList = []

d = "top100subs.txt";

try:
	with open (d,"r") as f:
		subdomainList = f.read().splitlines()
except FileNotFoundError:
	print("[-] File not exist")

hosts = {}


def ReverseDNS(ip):
	try:
		result = socket.gethostbyaddr(ip)
		return [result[0]]
	except socket.herror:
		return []

hostsbySearching = []
hostsbyReverseDNS = []
def DNSRequest(subdomain,domain):
	global hosts
	global hostsbySearching
	hostname = subdomain+domain
	try:
		result = dns.resolver.resolve(hostname)
		if result:
			for ans in result:
				ip = ans.to_text()
				hostnames = ReverseDNS(ip)
				subs = [subdomain]
				for hostname in hostnames:
					if hostname.endswith(domain):
						s = hostname.rstrip(domain)
						subs.append(s)

				if ip in hosts:
					s = hosts[ip]["subs"]
					hosts[ip] = list(dict.fromkeys(s+subs))
				else:
					hosts[ip] = list(dict.fromkeys(subs))
	except:
		return



def SubdomainSearch(domain,nums):
	successes = []
	for subdomain in subdomainList:
		DNSRequest(subdomain,domain)
		if nums:
			for i in range(0,10):
				DNSRequest(subdomain+str(i),domain)


def DNSSearch(domain,nums):
	SubdomainSearch(domain,nums)
	return hosts


if(len(sys.argv)<2):
	print(f"USAGE : python3 {sys.argv[0]} <domain name>")
	sys.exit(1)
else:
	domain = sys.argv[1]
	if(domain[0] != '.'):
		domain = '.'+domain
	hosts = DNSSearch(domain,True)

	for ip in hosts:
		hs = str(hosts[ip])
		hs = hs.replace("[","").replace("]","").replace("'","")
		print(ip,hs+domain)

