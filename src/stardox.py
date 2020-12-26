# Importing modules
import sys
import os
import colors
import Logo
import argparse

# Getting the name of the repository.
def getting_header(soup_text):
    title = soup_text.title.get_text()

    start = title.find('/')
    stop = title.find(':')
    return title[start + 1: stop]


# Function to make sure all the Url passed is made in particualr format.
def format_url(url):
    if url.startswith('http://'):
        url = url.replace('http', 'https')
    elif url.startswith('www.'):
        url = url.replace('www.', 'https://')
    elif url.startswith('https://') or url.startswith('https://www.'):
        pass
    else:
        colors.error("Enter the repositories url in given format"
                     "[ https://github.com/username/repository_name ]")
        sys.exit(1)
    return url


# Function to verify that the page URL given
# is pointing to some repository or not.
def verify_url(page_data):
    data = str(page_data)
    if "Popular repositories" in data:
        return False
    elif "Page not found" in data:
        return False
    else:
        return True


# Function returning email of the stargazer
def get_latest_commit(repo_name, username):
    email = ""
    commit_data = requests.get(
                "https://github.com"
                "/{}/{}/commits?author={}".format(
                                                 username,
                                                 repo_name,
                                                 username)).text
    soup = BeautifulSoup(commit_data, "lxml")
    a_tags = soup.findAll("a")
    for a_tag in a_tags:
        URL = a_tag.get("href")
        if URL.startswith("/{}/{}/commit/".format(username, repo_name)):
            label = str(a_tag.get("aria-label"))
            if "Merge" not in label and label != "None":
                patch_data = requests.get("https://github.com{}{}".format(
                            URL, ".patch")).text
                try:
                    start = patch_data.index("<")
                    stop = patch_data.index(">")
                    email = patch_data[start + 1: stop]
                except ValueError:
                    return "Not enough information."
                break
    if email != "":
        return email
    else:
        return "Not enough information."


def email(repository_link,ver):
    try:
        import data
    except ImportError:
        colors.error('Error importing data module')
        sys.exit(1)

    try:
        # Getting HTML page of repository
        html = requests.get(repository_link, timeout=8).text
    except (requests.exceptions.RequestException,
            requests.exceptions.HTTPError):
        colors.error(
            "Enter the repositories url in given format "
            "[ https://github.com/username/repository_name ]")
        sys.exit(1)
    # Checking if the url given is of a repository or not.
    result = verify_url(html)
    if result:
        colors.success("Got the repository data ", verbose)
    else:
        colors.error("Please enter the correct URL ")
        sys.exit(0)
    # Parsing the html data using BeautifulSoup
    soup1 = BeautifulSoup(html, "lxml")
    title = getting_header(soup1)  # Getting the title of the page
    data.header = title  # Storing title of the page as Project Title
    colors.success("Repository Title : " + title, verbose)
    colors.process("Doxing started ...\n", verbose)
    stargazer_link = repository_link + "/stargazers"

    page = 1

    while (stargazer_link is not None):
        stargazer_html = requests.get(stargazer_link).text
        soup2 = BeautifulSoup(stargazer_html, "lxml")
        a_next = soup2.findAll("a")
        for a in a_next:
            if a.get_text() == "Next":
                page += 1
                print('page:', page)
                stargazer_link = a.get('href')
                break
            else:
                stargazer_link = None
        follow_names = soup2.findAll("h3", {"class": "follow-list-name"})
        for name in follow_names:
            a_tag = name.findAll("a")
            username = a_tag[0].get("href")
            data.username_list.append(username[1:])
    count = 1
    pos = 0


    fields = ['Username', 'Email']
    csv_file = data.header + '.csv'  # Name of csv file
    file_path = os.path.join(os.environ["HOME"], csv_file)

    csvfile = open(file_path, 'w+')

    while(count <= len(data.username_list)):
        print(count, data.username_list[pos])
        repo_data = requests.get(
            "https://github.com/{}?tab=repositories&type=source"
            .format(data.username_list[pos])).text
        repo_soup = BeautifulSoup(repo_data, "lxml")
        a_tags = repo_soup.findAll("a")
        repositories_list = []
        for a_tag in a_tags:
            if a_tag.get("itemprop") == "name codeRepository":
                repositories_list.append(a_tag.get_text().strip())
        if len(repositories_list) > 0:
            email = get_latest_commit(
                    repositories_list[0],
                    data.username_list[pos])  # Getting stargazer's email
            data.email_list.append(str(email))
            csvfile.write(data.username_list[pos] + ',' + email + '\n')
            csvfile.flush()
        else:
            data.email_list.append("Not enough information.")
        count += 1
        pos += 1

    csvfile.close()
    colors.success("Saved the data into " + file_path, True)
    print("\n", colors.green + "{0}".format("-") * 75,
          colors.green, end="\n\n")

if __name__ == '__main__':
    try:
        Logo.header()  # For Displaying Logo

        parser = argparse.ArgumentParser()
        parser.add_argument('-r', '--rURL', help=" Path to repository.",
                            required=False, default=False)
        parser.add_argument('-v', '--verbose', help="Verbose",
                            required=False, default=True,
                            action='store_false')

        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError:
            colors.error('Error importing requests module.')

        args = parser.parse_args()
        repository_link = args.rURL
        verbose = args.verbose


        if args.rURL == False:
            repository_link = input(
                        "\033[37mEnter the repository address :: \x1b[0m")
            print(repository_link)

        repository_link = format_url(repository_link)

        email(repository_link,verbose)

    except KeyboardInterrupt:
        print("\n\nYou're Great..!\nThanks for using :)")
        sys.exit(0)
