import pdb
import time
import re
import argparse
import jwt
from playwright.sync_api import sync_playwright

# Adversis, LLC
#
# https://playwright.dev/python/docs/debug
# use `pdb.set_trace()` for debugging
# or `PWDEBUG=console playwrigh open example.com` for a playwright object in Dev Tools (>playwright.$('text=docs'))
# or `playwright codegen example.com` for tracing actions
#

class PostmanTeam:
    def __init__(self, id):
        self.id = id
        self.name = None
        self.collections = None
        self.workspaces = None
        self.tokens = {}

class PostmanRequests:
    def __init__(self, term):
        self.term = term
        self.workspaces = None
        self.collections = None
        self.teams = None
        self.requests = []

global args

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
TIMEOUT = 6000 #ms
SLOWMO = 0 #ms

def get_name_from_id(id):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=args.headless,
            slow_mo=SLOWMO
        )
        context = browser.new_context(
            user_agent=UA
        )
        context.set_default_timeout(TIMEOUT)
        page = context.new_page()

        page.goto(f"https://www.postman.com/{id}")

        page.wait_for_load_state("domcontentloaded")
        page.wait_for_load_state()
        time.sleep(1)

        name = page.query_selector(".user-profile__sidebar-info--name")
        if name is None: name = page.query_selector(".user-profile__sidebar-info--name-heading")
        if name:
            print(f"{id}:{name.inner_text()}")
        else:
            print(f"{id}:[not found]")


def get_team_names(term):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=args.headless,
            slow_mo=SLOWMO
        )
        context = browser.new_context(
            user_agent=UA
        )
        context.set_default_timeout(TIMEOUT)
        page = context.new_page()
    
        page.goto(f"https://www.postman.com/search?q={term}&type=team")

        time.sleep(2)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_load_state()

        teams = page.get_by_role("strong")
        for l in teams.all():
            name = l.inner_text()
            l.click()
            print(f"{name}: {page.url}")
            page.go_back()

def get_team_members(team_name):   
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=args.headless,
            slow_mo=SLOWMO
        )
        context = browser.new_context(
            user_agent=UA
        )
        context.set_default_timeout(TIMEOUT)
        page = context.new_page()
    
        page.goto(f"https://www.postman.com/{team_name}")

        time.sleep(2)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_load_state()


        team_members = page.get_by_role("button", name="View all members")
        if team_members.count() > 0:
            team_members.click()
            page.wait_for_load_state()
            users = page.query_selector(".team-profile--members-list-in-modal").inner_text()
            uniq_users = set()
            for user in users.split("\n"):
                id = ""
                try:
                    page.get_by_test_id("aether-modal").get_by_text(user, exact=True).hover()
                    page.wait_for_selector('.tippy-box', state='visible')
                    time.sleep(0.5)
                    id = page.query_selector(".tippy-box").inner_text()
                    id = re.findall(r"@.*", id)
                    id = id[0] if id else ''
                    print(f"{user}:{id}")
                except:
                    print(f"{user}:")
                    page.mouse.move(100, 0)
                    time.sleep(0.1)
                    continue
                page.mouse.move(100, 0)
                time.sleep(0.1)
        else:
            users = page.query_selector_all('img[src*="user_profile"]') 
            uniq_users = set()
            for user in users:
                name = user.get_attribute('alt') 
                uniq_users.add(name)
                if name in uniq_users: continue
            for user in uniq_users:
                id = ""
                try:
                    page.get_by_text(user).nth(3).hover()
                    page.wait_for_selector('.tippy-box', state='visible')
                    time.sleep(.5)
                    id = page.query_selector(".tippy-box").inner_text()
                    id = re.findall(r"@.*", id)  
                    id = id[0] if id else ''
                    print(f"{user}:{id}")
                except:
                    print(f"{user}:")
                    page.mouse.move(100, 0)
                    time.sleep(0.1)
                    continue
                page.mouse.move(100, 0)
                time.sleep(0.1)
        page.go_back()

def search_requests(term):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=args.headless,
            slow_mo=SLOWMO
        )
        context = browser.new_context(
            user_agent=UA
        )
        context.set_default_timeout(TIMEOUT)
        page = context.new_page()
            
        req = PostmanRequests(term=term)

        page.goto(f"https://www.postman.com/search?q={term}&type=request")
        time.sleep(2)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_load_state()
        
        all_links = []

        for i in range(5):
            links = page.get_by_role("link").filter(has_text="http")
            for l in links.all():
                #eval_on_selector("a[href]", "elements => elements.map(element => element.href)") 
                link = l.inner_text()
                all_links.append(link)
            i += 1
            #pdb.set_trace()
            page.mouse.wheel(0, 2048) #TODO - not scrolling page
            page.wait_for_load_state("domcontentloaded")
            time.sleep(1)

        req.requests = set(all_links)
        for l in req.requests:
            print(l)

        
        browser.close()

def search_collections(teamname):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=args.headless,
            slow_mo=SLOWMO
        )
        context = browser.new_context(
            user_agent=UA
        )
        context.set_default_timeout(TIMEOUT)
        page = context.new_page()

        u = PostmanTeam(id=teamname)
        page.goto(f"https://www.postman.com/{teamname}")
        time.sleep(2)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_load_state()
        
        # Get name
        try:
            if page.get_by_role("heading", level=1).count() > 0:
                name = page.get_by_role("heading", level=1).inner_text()
                u.name = name
        except:
            print(f"{teamname} Name not found")

        # Get Workspace info
        try:
            if page.get_by_role("button").filter(has_text="Workspaces").count() > 0:
                workspace = page.get_by_role("button").filter(has_text="Workspaces").inner_text()
                workspaces = page.get_by_role("button", name=workspace).click()
                page.wait_for_load_state('domcontentloaded')
                time.sleep(1)
                workspaces = page.get_by_test_id("entity-heading-link")
                workspaces = [w.inner_text() for w in workspaces.all()]
                u.workspaces = workspaces
        except:
            print(f"{teamname} Workspaces: 0")

        # Search collections
        try:
            if page.get_by_role("button").filter(has_text="Collections").count() > 0:
                collections = page.get_by_role("button").filter(has_text="Collections").inner_text()
                page.get_by_role("button", name=collections).click()
                page.wait_for_load_state()
                time.sleep(1)
                colls = page.get_by_test_id("entity-heading-link")
                colls = set([c.inner_text() for c in colls.all()])
                u.collections = colls
                page.get_by_test_id("entity-heading-link").first.click()
                page.wait_for_load_state()
                time.sleep(3)
                try:
                    # get all containers
                    container = page.get_by_test_id("sidebar-item")
                    container = [c.inner_text() for c in container.all()]
                    if args.verbose: print(f"Searching through {len(set(container))} containers")
                    for ctr in set(container):
                        try:
                            #if ctr == coll: continue
                            if re.match(r"^(GET|POST|DEL|PATCH)", ctr): continue
                            if args.verbose: print(f"\t{ctr}/")
                            page.get_by_title(ctr).first.click()
                            time.sleep(1)

                            # get container folders
                            folders = page.query_selector_all('.collection-virtualized-list-item__folder')
                            f = ''
                            for f in set(folders):
                                f = f.inner_text()
                                if args.verbose: print(f"\tOpening {f}/")
                                page.get_by_title(f, exact=True).first.click()
                                click_through_requests(page, u, ctr, f)
                                
                                # close folder
                                d = page.get_by_title(f, exact=True).get_by_test_id("base-button")
                                if d.count() > 1:
                                    d.first.click() 
                                else:
                                    d.click()
                            
                            # click through requests even if there are no folders
                            if len(folders) == 0:
                                click_through_requests(page, u, ctr, f)

                            # close container
                            d = page.get_by_role("button", name=f"dropdown toggle button {ctr}").get_by_test_id("base-button")
                            if d.count() > 1:
                                d.first.click()
                            else:
                                d.click()
                        except Exception as e:
                            if args.verbose: print(e)
                            pass
                except Exception as e:
                    if args.verbose: print(e)
                    d = page.get_by_role("button", name=f"dropdown toggle button {ctr}").get_by_test_id("base-button")
                    if d.count() > 1:
                        d.first.click()
                    else:
                        d.click()
                    pass
        except Exception as e:
            if args.verbose: print(e)
            pass
        
        if u.tokens:
            print(vars(u))
        else:
            if args.verbose: print(vars(u))
        
        browser.close()

def click_through_requests(page, u, ctr, f):
    # click all the requests
    requests = page.get_by_test_id("sidebar-item")
    requests = [c.inner_text() for c in requests.all()]
    for r in requests:
        if r == ctr: continue
        if re.match(r"^(GET|POST|DEL|PATCH)", r):
            r = re.sub(r'^.+\n', "", r)
            if args.verbose: print(f"\t\t{r}")
            try:
                page.get_by_title(r).first.click()
                time.sleep(1)
                params = page.query_selector_all(".request-editor-tabs-badge")
                headers = page.query_selector_all(".request-editor-tabs-count")
                if len(headers) > 0: [params.append(h) for h in headers]
                for p in params:
                    p.click()
                    time.sleep(1)
                    #pdb.set_trace()
                    rows = page.query_selector_all(".key-value-form-row") 
                    auth = page.query_selector(".auth-bearer-token-container")
                    rows.append(auth)
                    body = page.query_selector(".request-body-editors")
                    if body is not None and is_interesting_val(body.inner_text()):
                        body_val = body.inner_text()
                        if '{' in body_val: body_val = body_val.split('{')[1:]
                        bv = body_val.replace("\n", ",")
                        out = f'"{ctr}/{f}": ["{bv}"]'
                        if args.verbose: print(f'\t\t{out}')
                        u.tokens.setdefault(out)
                    for r in rows:
                        if r is None: continue
                        line = r.inner_text()
                        try:    
                            k = line.split("\n")[0]
                            v = line.split("\n")[1]
                            if is_interesting_val(k):
                                if v.lower() == "value": continue
                                if re.findall(r'{{.*(access|token|key|password|secret|authorization).*}}', v, re.IGNORECASE): continue
                                out = f'"{ctr}/{f}": ["{k}":"{v}"]'
                                if args.verbose: print(f'\t\t"{out}"]') 
                                u.tokens.setdefault(out)
                        except:
                            continue
            except:
                pass

def is_interesting_val(val):
    for s in ["admin", "key", "token", "cred", "bearer", "basic", "secret", "cookie", "auth", "ssws", "negotiate", "email", "password", "access", "session", "refresh", "crypt"]:
        if re.search(s, val, re.IGNORECASE):
            return True
    return False

def main():
    global args
    parser = argparse.ArgumentParser(description="A proof of concept Postman search tool")

    # Add flags
    parser.add_argument("--id-lookup", dest="id_lookup", type=str, help="Gets team names from id")
    parser.add_argument("--team-search", dest="team_search", type=str, help="Gets team names with search term")
    parser.add_argument("--team-members", dest="team_members", type=str, help="Gets team members")
    parser.add_argument("--search-requests", dest="requests", type=str, help="Searches all requests with term")
    parser.add_argument("--search-truffles", dest="team_truffle", type=str, help="Searches interesting values in a user or teams's collection requests")
    parser.add_argument("--verbose", dest="verbose", default=False, action='store_true', help="Print verbose output")
    parser.add_argument("--unheadless", dest="headless", default=True, action='store_false', help="Run visible browser")

    args = parser.parse_args()
    if args.team_search is not None:
        get_team_names(args.team_search)
    if args.team_members is not None:
        get_team_members(args.team_members)
    if args.requests is not None:
        search_requests(args.requests)
    if args.team_truffle is not None:
        search_collections(args.team_truffle)
    if args.id_lookup is not None:
        get_name_from_id(args.id_lookup)     

if __name__ == "__main__":
    main()
