# README

Proof of concept tool to save some manual effort clicking through Postman collections for truffles.


### Setup
```sh
> pip install -r requirements.txt
> playwright install
> playwright install-deps
```

### Usage
```txt
> python postdigger.py -h
usage: postdigger.py [-h] [--id-lookup ID_LOOKUP] [--team-search TEAM_SEARCH] [--team-members TEAM_MEMBERS]                                  [--search-requests REQUESTS] [--search-truffles TEAM_TRUFFLE] [--verbose] [--unheadless]                                                                                                                                   A proof of concept Postman search tool                                                                                                                                                                                                          optional arguments:                                                                                                       -h, --help            show this help message and exit                                                                   --id-lookup ID_LOOKUP                                                                                                                         Gets team names from id                                                                           --team-search TEAM_SEARCH                                                                                                                     Gets team names with search term                                                                  --team-members TEAM_MEMBERS                                                                                                                   Gets team members                                                                                 --search-requests REQUESTS                                                                                                                    Searches all requests with term                                                                   --search-truffles TEAM_TRUFFLE                                                                                                                Searches interesting values in a user or teams's collection requests                              --verbose             Print verbose output                                                                              --unheadless          Run visible browser
```

### Examples

```sh
% python postdigger.py --search-requests vzw.com
POST https://amservicesvzwqa3.sdc.vzwcorp.com/igservices/2fa/deviceverification
POST https://vip-sqa1.vzwcorp.com/eai/vipm2msvc/VzwWSAdapter

% python postdigger.py --team-search verizon
Verizon: https://www.postman.com/martian-firefly-575143
Verizon: https://www.postman.com/antonverizon
Verizon: https://www.postman.com/api-postmancollection
Verizon: https://www.postman.com/verizon-
Verizone: https://www.postman.com/universal-sunset-962066
verizon-gl: https://www.postman.com/universal-space-733069
Nerdery Verizon: https://www.postman.com/nerdery-verizon
uniphore-verizon: https://www.postman.com/uniphore-verizon
ArubaAtVerizon: https://www.postman.com/dark-rocket-27878
Verizon-Digital Activity Twin: https://www.postman.com/cloudy-sunset-712183
MVD: https://www.postman.com/lunar-resonance-985513

% python postdigger.py --team-members verizon-
Rahul:@rahuldubey8
Nick Kulikaev:@nkulikaev83
vzmason:@vzmason
Alexander (Alex) Childs:@descent-module-observer-58132517
Matthew Logick:@descent-module-cosmonaut-90628208
Matt Ball:@matt@postman.com
Gagan Maheshwari:@aviation-astronomer-42491040
Nathaniel Sandberg:@nathanielsandbergverizon

% python postdigger.py --search-truffles cryosat-administrator-51626609
{'id': 'cryosat-administrator-51626609', 'name': 'Hung Vu', 'collections': {'Gateway API', 'Transfer Money', 'Service Management', 'Test', 'Others', 'MB AMC Identity & Access Management Service', '10- History', 'MB AMC Ticket Service', 'NuGetApi', 'Core-Service-Basic', '2-basic core services (contextpath=/basicservices)', 'Mytel-API', 'OTP', '13. Device management', '7. smart-otp-v2', '1- account-service', 'Gateway_Burma', 'AIBooks', 'HomeUI-Mobile', 'Payment API Mobile'}, 'workspaces': ['My Public Workspace'], 'tokens': {'"Service Management/": ["Token":"eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2l...": None, '"1- account-service/web": ["password":"Mytel@2021"]': None}}
```

### Known limitations

It's brittle as they come and won't survive a front end refactor by Postman.

PRs welcome. If at first you don't succeed, try again, run unheadless, use verbose.

- [ ] specify a workspace to search
- [ ] good luck using a proxy or cloud infrastructure
