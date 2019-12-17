import data


def plotdata(stars, pos, count):

    if count == 1:
        print("\033[34m    {}   ".format(data.header))
        print("\033[1;37m¯¯¯¯{}¯¯¯¯".format('¯' * len(data.header)), end="\n")
        print(
            '''\033[1;37m{}
\033[1;37m|-----\033[1;32m{} (@{})
\033[1;37m|  |
\033[1;37m|  |--\033[1;32mTotal Repsitories :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mTotal Stars       :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mTotal Followers   :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mTotal Following   :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mUser Email        :: \033[1;37m{}
\033[1;37m|'''.format("|", data.name_list[pos], data.username_list[pos],
                      data.repo_list[pos].strip(),
                      data.star_list[pos].strip(),
                      data.followers_list[pos].strip(),
                      data.following_list[pos].strip(),
                      data.email_list[pos].strip()))

    elif(count > 1 and count < stars):
        print(
            '''\033[1;37m{}
\033[1;37m|-----\033[1;32m{} (@{})
\033[1;37m|  |
\033[1;37m|  |--\033[1;32mTotal Repsitories :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mTotal Stars       :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mTotal Followers   :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mTotal Following   :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mUser Email        :: \033[1;37m{}
\033[1;37m|'''.format("|", data.name_list[pos], data.username_list[pos],
                      data.repo_list[pos].strip(),
                      data.star_list[pos].strip(),
                      data.followers_list[pos].strip(),
                      data.following_list[pos].strip(),
                      data.email_list[pos].strip()))

    elif count == stars:
        print('''{}
\033[1;37m|-----\033[1;32m{} (@{})
\033[1;37m|  |
\033[1;37m|  |--\033[1;32mTotal Repsitories :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mTotal Stars       :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mTotal Followers   :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mTotal Following   :: \033[1;37m{}
\033[1;37m|  |--\033[1;32mUser Email        :: \033[1;37m{}
'''.format("|",
           data.name_list[pos], data.username_list[pos],
           data.repo_list[pos].strip(), data.star_list[pos].strip(),
           data.followers_list[pos].strip(),
           data.following_list[pos].strip(),
           data.email_list[pos].strip()))
